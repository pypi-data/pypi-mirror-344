from __future__ import annotations

import asyncio
import atexit
import attrs
import datetime as dt
import logging
import multiprocessing as mp
from typing import TYPE_CHECKING

from NaviNIBS_Cobot.Devices.CobotConnector.CobotConnectorClient import CobotConnectorClient
from NaviNIBS_Cobot.Devices.CobotConnector.CobotConnectorServer import CobotConnectorServer
if TYPE_CHECKING:
    from NaviNIBS_Cobot.Navigator.Model.CobotConfiguration import CobotControl

from NaviNIBS.util.Asyncio import asyncTryAndLogExceptionOnError
from NaviNIBS.util.logging import getLogFilepath
from NaviNIBS.Navigator.Model.Session import Session
from NaviNIBS.Navigator.Model.Tools import CoilTool
from NaviNIBS.util.ZMQConnector import ZMQConnectorClient
from NaviNIBS.Navigator.TargetingCoordinator import TargetingCoordinator


logger = logging.getLogger(__name__)


@attrs.define(kw_only=True)
class CobotTargetingController:
    _session: Session = attrs.field(repr=False)

    _doRunConnectorServer: bool = attrs.field(default=True)
    _connectorServerKwargs: dict = attrs.field(factory=dict)

    _targetingCoordinator: TargetingCoordinator | None = attrs.field(default=None, repr=False)

    _cobotConnectorProc: mp.Process | None = attrs.field(init=False, default=None)
    _cobotConnectorClient: CobotConnectorClient = attrs.field(init=False)

    _activeCoilTool: CoilTool | None = attrs.field(init=False, default=None, repr=False)

    def __attrs_post_init__(self):
        logger.info(f'Initializing {self.__class__.__name__}')

        self._cobotConnectorClient = CobotConnectorClient()

        if self._targetingCoordinator is None:
            logger.debug('Initializing targeting coordinator')
            self._targetingCoordinator = TargetingCoordinator.getSingleton(
                session=self._session,
            )

        if self._doRunConnectorServer:
            self._startCobotConnectorProc()

        self._session.subjectRegistration.sigTrackerToMRITransfChanged.connect(
            lambda: asyncio.create_task(asyncTryAndLogExceptionOnError(self._onSubjectRegistrationChanged)))
        self._session.tools.sigItemsChanged.connect(
            lambda *args: asyncio.create_task(asyncTryAndLogExceptionOnError(self._onSubjectTrackerKeyMaybeChanged)))

        self.session.headModel.sigFilepathChanged.connect(
            lambda: asyncio.create_task(asyncTryAndLogExceptionOnError(self._onHeadMeshPathMaybeChanged)))

        self.targetingCoordinator.sigActiveCoilKeyChanged.connect(self._onCoilToolKeyChanged)
        self._onCoilToolKeyChanged()

        asyncio.create_task(asyncTryAndLogExceptionOnError(self._onSubjectRegistrationChanged))
        asyncio.create_task(asyncTryAndLogExceptionOnError(self._onSubjectTrackerKeyMaybeChanged))
        asyncio.create_task(asyncTryAndLogExceptionOnError(self._onHeadMeshPathMaybeChanged))
        asyncio.create_task(asyncTryAndLogExceptionOnError(self._maybeDoExtraSetupForSimulatedCobot))

        atexit.register(self._atexit)

    def _startCobotConnectorProc(self):
        logger.info('Starting cobotConnectorServer process')
        kwargs = self._connectorServerKwargs.copy()
        kwargs['logFilepath'] = getLogFilepath(self.session)
        self._cobotConnectorProc = mp.Process(
            target=CobotConnectorServer.createAndRun,
            name='CobotConnector',
            kwargs=kwargs
        )
        self._cobotConnectorProc.start()

    def _stopCobotConnectorProc(self):
        if self._cobotConnectorProc is None:
            logger.warning('Cobot connector proc already stopped')
            return

        # TODO: maybe implement a message to the server to stop it gracefully

        logger.info('Stopping cobotConnectorServer process')
        self._cobotConnectorProc.kill()
        self._cobotConnectorProc = None

    @property
    def session(self):
        return self._session

    @property
    def targetingCoordinator(self):
        return self._targetingCoordinator

    @property
    def cobotClient(self):
        return self._cobotConnectorClient

    @property
    def configuration(self) -> CobotControl:
        return self._session.addons['NaviNIBS_Cobot'].cobotControl

    @property
    def needsForceCheck(self):
        config = self.configuration
        if config.forceLastCheckedAtTime is None:
            return True

        lastCheckedAtTime = dt.datetime.strptime(config.forceLastCheckedAtTime, '%y%m%d%H%M%S.%f')
        currentTime = dt.datetime.now()
        timeSinceLastCheck = currentTime - lastCheckedAtTime
        return timeSinceLastCheck > dt.timedelta(minutes=config.needsForceCheckAfterMinutes)

    async def _onSubjectRegistrationChanged(self):
        logger.debug('_onSubjectRegistrationChanged')
        await self.cobotClient.connectedToServerEvent.wait()
        subjectTrackerToMRITransf = self.session.subjectRegistration.trackerToMRITransf
        await self._cobotConnectorClient.setSubjectRegistration(subjectTrackerToMRITransf)
        logger.debug('Set registration')

    async def _onSubjectTrackerKeyMaybeChanged(self):
        logger.debug('_onSubjectTrackerKeyMaybeChanged')
        await self.cobotClient.connectedToServerEvent.wait()
        subjectTrackerKey = self.session.tools.subjectTracker.trackerKey
        logger.debug(f'Setting subject tracker key to {subjectTrackerKey}')
        await self._cobotConnectorClient.setSubjectTrackerKey(subjectTrackerKey)
        logger.debug('Set subject tracker key')

    async def _onHeadMeshPathMaybeChanged(self):
        logger.debug('_onHeadMeshPathChanged')
        await self.cobotClient.connectedToServerEvent.wait()
        headMeshPath = self.session.headModel.skinSurfPath
        await self._cobotConnectorClient.setHeadMeshPath(headMeshPath)
        logger.debug('Set head mesh path')

    def _onCoilToolKeyChanged(self):
        logger.debug('_onCoilToolKeyChanged')

        if self._activeCoilTool is not None:
            self._activeCoilTool.sigItemChanged.disconnect(self._onCoilToolChanged)

        if self.targetingCoordinator.activeCoilKey is None:
            self._activeCoilTool = None
        else:
            coilTool = self.session.tools[self.targetingCoordinator.activeCoilKey]
            coilTool.sigItemChanged.connect(self._onCoilToolChanged)
            self._onCoilToolChanged(key=coilTool.key)

    def _onCoilToolChanged(self, key: str, changedAttribs: list[str] | None = None):
        asyncio.create_task(asyncTryAndLogExceptionOnError(self._onCoilToolChanged_async, changedAttribs=changedAttribs))

    async def _onCoilToolChanged_async(self, changedAttribs: list[str] | None = None):
        logger.debug('_onCoilToolChanged')
        await self.cobotClient.connectedToServerEvent.wait()

        if self.targetingCoordinator.activeCoilKey is None:
            await self._cobotConnectorClient.setCoilTrackerKey(None)
            await self._cobotConnectorClient.setCoilMeshPath(None)
            await self._cobotConnectorClient.setCoilMeshToToolTransf(None)
            await self._cobotConnectorClient.setCoilToolToTrackerTransf(None)
        else:
            coilTool = self.session.tools[self.targetingCoordinator.activeCoilKey]

            if changedAttribs is None or 'key' in changedAttribs:
                await self._cobotConnectorClient.setCoilTrackerKey(coilTool.trackerKey)

            if changedAttribs is None or 'toolStlFilepath' in changedAttribs:
                await self._cobotConnectorClient.setCoilMeshPath(coilTool.toolStlFilepath)

            if changedAttribs is None or 'toolStlToToolTransf' in changedAttribs:
                await self._cobotConnectorClient.setCoilMeshToToolTransf(coilTool.toolStlToToolTransf)

            if changedAttribs is None or 'toolToTrackerTransf' in changedAttribs:
                await self._cobotConnectorClient.setCoilToolToTrackerTransf(coilTool.toolToTrackerTransf)

    async def _maybeDoExtraSetupForSimulatedCobot(self):
        await self.cobotClient.connectedToServerEvent.wait()
        isSimulated = await self.cobotClient.getRemoteClientAttr_async('isSimulated')
        if not isSimulated:
            return

    async def startTrackingTarget(self):
        await self._cobotConnectorClient.startTrackingTarget()

    async def stopTrackingTarget(self):
        await self._cobotConnectorClient.stopTrackingTarget()

    def _atexit(self):
        if self._cobotConnectorProc is not None:
            self._cobotConnectorProc.kill()
            self._cobotConnectorProc = None