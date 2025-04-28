import asyncio
import attrs
import json
import logging
import numpy as np
import typing as tp

from NaviNIBS_Cobot.Devices.CobotConnector import (
    cobotTargetingServerHostname,
    cobotTargetingServerPubPort,
    cobotTargetingServerCmdPort,
    TargetingState,
    ContactMode,
    TargetChangeRetractMode,
    TargetChangeContactMode,
)

from NaviNIBS_Cobot.Devices.CobotConnector.CobotActionSequence import CobotActionSequence, CobotAction

from NaviNIBS.util import exceptionToStr
from NaviNIBS.util.Asyncio import asyncTryAndLogExceptionOnError
from NaviNIBS.util.Signaler import Signal
from NaviNIBS.util.ZMQConnector import ZMQConnectorClient, logger as logger_ZMQConnector

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
#logger_ZMQConnector.setLevel(logging.DEBUG)

_novalue = object()


@attrs.define(kw_only=True)
class CobotConnectorClient:
    _connector: ZMQConnectorClient = attrs.field(init=False, repr=False)

    sigConnectedChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigEnabledChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigControlIsLockedChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigPoweredChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigHomedChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigAlignMotionInProgressChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigAlignMotionAbortedChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigInToleranceToDestinationChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigContactChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigServoingChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigFreedriveButtonPressedChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigAxesMovingChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigEstopped: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigFreedrivingChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigInProtectiveStopChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigInWorkspaceChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigTargetLabelChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigTargetAccessibleChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigMeasuredForceChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigRawCoilIDValueChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigRawForceValueChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigSensitivityChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigStateChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigContactModeChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigAirgapOffsetFromContactChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigAirgapOffsetFromScalpChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigAirgapOffsetFromTargetChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigDistantTargetChangeRetractModeChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigDistantTargetChangeContactModeChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigNearTargetChangeRetractModeChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigNearTargetChangeContactModeChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigTargetChangeDistanceThresholdChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigTargetChangeAngleThresholdChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigTryingToContactChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigHasCalibratedContactDepthForCurrentTargetChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigRealignThresholdsChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigAlignedThresholdsChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigActionSequenceStackChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigIsApproximatelyAlignedChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigCobotCoilToolChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigCoilToolChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigJointPositionsChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    sigJointPositionLimitsChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)

    __isConnectedToServer: bool = attrs.field(init=False, default=False)
    sigConnectedToServerChanged: Signal = attrs.field(init=False, factory=Signal, repr=False)
    connectedToServerEvent: asyncio.Event = attrs.field(init=False, factory=asyncio.Event)

    _cachedState: TargetingState | None = attrs.field(init=False, default=None)
    _cachedActionSequenceProgressAndLabels: tp.Any | None = attrs.field(init=False, default=None)
    _cachedJointPositions: dict | None = attrs.field(init=False, default=None)
    _cachedJointPositionLimits: dict | None = attrs.field(init=False, default=None)

    _proc_monitorConnection: asyncio.Task = attrs.field(init=False, repr=False)

    def __attrs_post_init__(self):
        self._connector = ZMQConnectorClient(
            connAddr=cobotTargetingServerHostname,
            pubSubPort=cobotTargetingServerPubPort,
            reqRepPort=cobotTargetingServerCmdPort,
            onMessagePublished=self._onConnectorMessagePublished,
            allowAsyncCalls=True
        )

        self._proc_monitorConnection = asyncio.create_task(asyncTryAndLogExceptionOnError(self._monitorConnection))

        self.sigStateChanged.connect(lambda: setattr(self, '_cachedState', None), priority=10)
        self.sigJointPositionsChanged.connect(lambda: setattr(self, '_cachedJointPositions', None), priority=10)
        self.sigJointPositionLimitsChanged.connect(lambda: setattr(self, '_cachedJointPositionLimits', None), priority=10)

    def _getRemoteClientAttr(self, item: str):
        logger.debug(f'Getting remoteClientAttr {item}')
        return self._connector.call('getClientAttr', item=item)

    async def getRemoteClientAttr_async(self, item: str):
        logger.debug(f'Async getting remoteClientAttr {item}')
        return await self._connector.call_async('getClientAttr', item=item)

    async def _callRemoteClientMethodAsync_async(self, clientMethod: str, **kwargs):
        logger.debug(f'Async calling remoteClientMethodAsync {clientMethod}')
        return await self._connector.callAsync_async(method='callClientMethod_async', clientMethod=clientMethod, **kwargs)

    @property
    def isConnectedToServer(self):
        return self._isConnectedToServer

    @property
    def _isConnectedToServer(self):
        return self.__isConnectedToServer

    @_isConnectedToServer.setter
    def _isConnectedToServer(self, value: bool):
        if value != self.__isConnectedToServer:
            logger.debug(f'isConnectedToServer changed to {value}')
            self.__isConnectedToServer = value
            if value:
                self.connectedToServerEvent.set()
            else:
                self.connectedToServerEvent.clear()
            self.sigConnectedToServerChanged.emit(value)

    @property
    def isConnected(self):
        return self._getRemoteClientAttr('isConnected')

    @property
    def isEnabled(self):
        return self._getRemoteClientAttr('isEnabled')

    @property
    def sessionHasStarted(self):
        return self._getRemoteClientAttr('sessionHasStarted')

    @property
    def isPoweredOn(self):
        return self._getRemoteClientAttr('isPoweredOn')

    @property
    def isHomed(self):
        return self._getRemoteClientAttr('isHomed')

    @property
    def controlIsLocked(self):
        return self._getRemoteClientAttr('controlIsLocked')

    @property
    def isFreedriving(self):
        return self._getRemoteClientAttr('isFreedriving')

    @property
    def isInWorkspace(self):
        return self._getRemoteClientAttr('isInWorkspace')

    @property
    def isInExtendedWorkspace(self):
        return self._getRemoteClientAttr('isInExtendedWorkspace')

    @property
    def alignMotionInProgress(self):
        return self._getRemoteClientAttr('alignMotionInProgress')

    @property
    def alignMotionAborted(self):
        return self._getRemoteClientAttr('alignMotionAborted')

    @property
    def isMoving(self):
        return self._getRemoteClientAttr('isMoving')

    @property
    def isInContact(self):
        return self._getRemoteClientAttr('isInContact')

    @property
    def isServoing(self):
        return self._getRemoteClientAttr('isServoing')

    @property
    def isRetracting(self):
        return self._getRemoteClientAttr('isRetracting')

    @property
    def isRetracted(self):
        return self._getRemoteClientAttr('isRetracted')

    @property
    def freedriveButtonIsPressed(self):
        return self._getRemoteClientAttr('freedriveButtonIsPressed')

    @property
    def isInToleranceToDestination(self):
        return self._getRemoteClientAttr('isInToleranceToDestination')

    @property
    def isInProtectiveStop(self):
        return self._getRemoteClientAttr('isInProtectiveStop')

    @property
    def cobotProtocolVersion(self):
        return self._getRemoteClientAttr('protocolVersion')

    @property
    def cobotControllerVersion(self):
        return self._getRemoteClientAttr('controllerVersion')

    @property
    def cobotVersion(self):
        return self._getRemoteClientAttr('robotVersion')

    @property
    def targetLabel(self):
        return self._connector.get('targetLabel')

    @property
    def targetIsAccessible(self):
        return self._connector.get('targetIsAccessible')

    @property
    def lastMeasuredForce(self) -> float | None:
        return self._connector.get('lastMeasuredForce')

    @property
    def lastRawCoilIDValue(self):
        return self._connector.get('lastRawCoilIDValue')

    @property
    def lastRawForceValue(self):
        return self._connector.get('lastRawForceValue')

    @property
    def sensitivity(self) -> float | None:
        return self._connector.get('sensitivity')

    async def getSensitivity(self) -> float:
        return await self._connector.callAsync_async('getSensitivity')

    async def setSensitivity(self, sensitivity: float):
        await self._connector.callAsync_async('setSensitivity', sensitivity)

    @property
    def isSimulated(self):
        return self._getRemoteClientAttr('isSimulated')

    @property
    def state(self):
        return TargetingState(self._connector.get('state'))

    @property
    def cachedState(self):
        """
        Note: there are some race conditions where this cached value may be out of date, so should
        only be used by non-critical callers (e.g. GUI indicators)
        """
        if self._cachedState is None:
            self._cachedState = self.state
        return self._cachedState

    @property
    def contactMode(self):
        return ContactMode(self._connector.get('contactMode'))

    @property
    def nearTargetChangeRetractMode(self):
        return TargetChangeRetractMode(self._connector.get('nearTargetChangeRetractMode'))

    @property
    def distantTargetChangeRetractMode(self):
        return TargetChangeRetractMode(self._connector.get('distantTargetChangeRetractMode'))

    @property
    def nearTargetChangeContactMode(self):
        return TargetChangeContactMode(self._connector.get('nearTargetChangeContactMode'))

    @property
    def distantTargetChangeContactMode(self):
        return TargetChangeContactMode(self._connector.get('distantTargetChangeContactMode'))

    @property
    def airgapOffsetFromContact(self) -> float:
        return self._connector.get('airgapOffsetFromContact')

    @property
    def airgapOffsetFromScalp(self) -> float:
        return self._connector.get('airgapOffsetFromScalp')

    @property
    def airgapOffsetFromTarget(self) -> float:
        return self._connector.get('airgapOffsetFromTarget')

    @property
    def isTryingToContact(self):
        return self._connector.get('isTryingToContact')

    @property
    def hasCalibratedContactDepthForCurrentTarget(self):
        return self._connector.get('hasCalibratedContactDepthForCurrentTarget')

    @property
    def realignWhenDistErrorExceeds(self):
        return self._connector.get('realignWhenDistErrorExceeds')

    @property
    def realignWhenZAngleErrorExceeds(self):
        return self._connector.get('realignWhenZAngleErrorExceeds')

    @property
    def realignWhenHorizAngleErrorExceeds(self):
        return self._connector.get('realignWhenHorizAngleErrorExceeds')

    @property
    def moveWhenZDistErrorExceeds(self):
        return self._connector.get('moveWhenZDistErrorExceeds')

    @property
    def alignedWhenDistErrorUnder(self):
        return self._connector.get('alignedWhenDistErrorUnder')

    @property
    def alignedWhenZAngleErrorUnder(self):
        return self._connector.get('alignedWhenZAngleErrorUnder')

    @property
    def alignedWhenHorizAngleErrorUnder(self):
        return self._connector.get('alignedWhenHorizAngleErrorUnder')

    @property
    def doneMovingWhenZDistErrorUnder(self):
        return self._connector.get('doneMovingWhenZDistErrorUnder')

    @property
    def isApproximatelyAligned(self):
        return self._connector.get('isApproximatelyAligned')

    @property
    def cobotCoilToolToTrackerTransf(self) -> np.ndarray | None:
        transf = self._connector.call('getCobotCoilToolToTrackerTransf')
        if transf is not None:
            transf = np.array(transf)
        return transf

    @property
    def latestJointPositions(self) -> dict[str, list[float]]:
        if self._cachedJointPositions is None:
            self._cachedJointPositions = self._connector.get('latestJointPositions')
        return self._cachedJointPositions

    @property
    def latestJointPositionLimits(self) -> dict[str, list[float]]:
        if self._cachedJointPositionLimits is None:
            self._cachedJointPositionLimits = self._connector.get('latestJointPositionLimits')
        return self._cachedJointPositionLimits

    async def startSession(self, **kwargs):
        await self._connector.callAsync_async('startSession', **kwargs)

    async def endSession(self):
        await self._callRemoteClientMethodAsync_async('endSession')

    async def startHoming(self):
        await self._callRemoteClientMethodAsync_async('startHoming')

    async def clearHoming(self):
        await self._callRemoteClientMethodAsync_async('clearHoming')

    async def powerOn(self):
        await self._callRemoteClientMethodAsync_async('powerOn')

    async def powerOff(self):
        await self._callRemoteClientMethodAsync_async('powerOff')

    async def stop(self):
        await self._callRemoteClientMethodAsync_async('stop')

    async def estop(self):
        await self._callRemoteClientMethodAsync_async('estop')

    async def startFreedrive(self):
        await self._callRemoteClientMethodAsync_async('startFreedrive')

    async def stopFreedrive(self):
        await self._callRemoteClientMethodAsync_async('stopFreedrive')

    async def startMovingToPark(self):
        await self._callRemoteClientMethodAsync_async('startMovingToPark')

    async def startMovingToWelcome(self, **kwargs):
        await self._callRemoteClientMethodAsync_async('startMovingToWelcome', **kwargs)

    async def startContact(self):
        await self._connector.callAsync_async('startContact')

    async def stopContact(self):
        await self._connector.callAsync_async('stopContact')

    async def startContact_lowLevel(self):
        await self._callRemoteClientMethodAsync_async('startContact')

    async def stopContact_lowLevel(self):
        await self._callRemoteClientMethodAsync_async('stopContact')

    async def connectCobotClient(self):
        await self._callRemoteClientMethodAsync_async('connect')

    async def disconnectCobotClient(self):
        await self._callRemoteClientMethodAsync_async('disconnect')

    async def connectToCobotAndInitialize(self):
        await self._connector.callAsync_async('connectToCobotAndInitialize')

    async def setSimulatedForceValue(self, force: int):
        """
        Note: only valid for simulated Cobot.

        May conflict (or be nearly immediately overriden by) head-contact based force simulation.
        """
        await self._callRemoteClientMethodAsync_async('setSimulatedForceValue', force=force)

    async def getActionSequenceProgressAndLabels(self) -> tuple[tuple[int | None, int, tuple[str,...]], ...]:
        """
        Returns a tuple of (currentActionIndex, totalNumActions, (actionSequenceLabel, action0Label, action1Label,...))
         for each action sequence in the stack, with the "currently executing" (or about to be executed) action
         sequence last.
        """
        return await self._connector.call_async('getActionSequenceProgressAndLabels')

    async def setSubjectRegistration(self, subjectTrackerToMRITransf: np.ndarray | None):
        await self._connector.set_async(
            'subjectTrackerToMRITransf',
            subjectTrackerToMRITransf.tolist() if subjectTrackerToMRITransf is not None else None)

    async def setSubjectTrackerKey(self, subjectTrackerKey: str | None):
        await self._connector.set_async(
            'subjectTrackerKey', subjectTrackerKey)

    async def setCoilTrackerKey(self, coilTrackerKey: str | None):
        await self._connector.set_async(
            'coilTrackerKey', coilTrackerKey)

    async def setHeadMeshPath(self, headMeshPath: str | None):
        await self._connector.set_async(
            'headMeshPath', headMeshPath)

    async def setCoilMeshPath(self, coilMeshPath: str | None):
        await self._connector.set_async(
            'coilMeshPath', coilMeshPath)

    async def setTargetingInfo(self,
                               targetLabel: str | None = _novalue,
                               targetCoilToMRITransf: np.ndarray | None = _novalue):
        kwargs = dict()
        if targetLabel is not _novalue:
            kwargs['targetLabel'] = targetLabel
        if targetCoilToMRITransf is not _novalue:
            kwargs['targetCoilToMRITransf'] = targetCoilToMRITransf.tolist() if targetCoilToMRITransf is not None else None
        await self._connector.callAsync_async('setTargetingInfo', **kwargs)

    async def setTargetLabel(self, targetLabel: str | None):
        await self._connector.set_async(
            'targetLabel', targetLabel)

    async def setTargetCoilToMRITransf(self, targetCoilToMRITransf: np.ndarray | None):
        await self._connector.set_async(
            'targetCoilToMRITransf',
            targetCoilToMRITransf.tolist() if targetCoilToMRITransf is not None else None)

    async def setCoilMeshToToolTransf(self, coilMeshToToolTransf: np.ndarray | None):
        await self._connector.set_async(
            'coilMeshToToolTransf',
            coilMeshToToolTransf.tolist() if coilMeshToToolTransf is not None else None)

    async def setCoilToolToTrackerTransf(self, coilToolToTrackerTransf: np.ndarray | None):
        await self._connector.set_async(
            'coilToolToTrackerTransf',
            coilToolToTrackerTransf.tolist() if coilToolToTrackerTransf is not None else None)

    async def startTrackingTarget(self):
        await self._connector.callAsync_async('startTrackingTarget')

    async def stopTrackingTarget(self):
        await self._connector.callAsync_async('stopTrackingTarget')

    async def startRootActionSequence(self, actionSequence: CobotActionSequence):
        await self._connector.callAsync_async('startRootActionSequence', actionSequence=actionSequence.asDict())

    async def cancelActionSequences(self):
        await self._connector.callAsync_async('cancelActionSequences')

    async def setContactMode(self, contactMode: ContactMode):
        await self._connector.callAsync_async('setContactMode', contactMode=contactMode.value)

    async def setNearTargetChangeRetractMode(self, retractMode: TargetChangeRetractMode):
        await self._connector.set_async('nearTargetChangeRetractMode', retractMode.value)

    async def setDistantTargetChangeRetractMode(self, retractMode: TargetChangeRetractMode):
        await self._connector.set_async('distantTargetChangeRetractMode', retractMode.value)

    async def setNearTargetChangeContactMode(self, contactMode: TargetChangeContactMode):
        await self._connector.set_async('nearTargetChangeContactMode', contactMode.value)

    async def setDistantTargetChangeContactMode(self, contactMode: TargetChangeContactMode):
        await self._connector.set_async('distantTargetChangeContactMode', contactMode.value)

    async def setAirgapOffsetFromContact(self, airgapOffset: float):
        await self._connector.set_async('airgapOffsetFromContact', airgapOffset)

    async def setAirgapOffsetFromScalp(self, airgapOffset: float):
        await self._connector.set_async('airgapOffsetFromScalp', airgapOffset)

    async def setAirgapOffsetFromScalp_FromContactOffsetDepth(self):
        await self._connector.callAsync_async('setAirgapOffsetFromScalp_FromContactOffsetDepth')

    async def setAirgapOffsetFromTarget(self, airgapOffset: float):
        await self._connector.set_async('airgapOffsetFromTarget', airgapOffset)

    async def resumeAfterProtectiveStop(self):
        await self._callRemoteClientMethodAsync_async('resumeAfterProtectiveStop')

    async def setRealignWhenDistErrorExceeds(self, value: float):
        await self._connector.set_async('realignWhenDistErrorExceeds', value)

    async def setRealignWhenZAngleErrorExceeds(self, value: float):
        await self._connector.set_async('realignWhenZAngleErrorExceeds', value)

    async def setRealignWhenHorizAngleErrorExceeds(self, value: float):
        await self._connector.set_async('realignWhenHorizAngleErrorExceeds', value)

    async def setMoveWhenZDistErrorExceeds(self, value: float):
        await self._connector.set_async('moveWhenZDistErrorExceeds', value)

    async def setAlignedWhenDistErrorUnder(self, value: float):
        await self._connector.set_async('alignedWhenDistErrorUnder', value)

    async def setAlignedWhenZAngleErrorUnder(self, value: float):
        await self._connector.set_async('alignedWhenZAngleErrorUnder', value)

    async def setAlignedWhenHorizAngleErrorUnder(self, value: float):
        await self._connector.set_async('alignedWhenHorizAngleErrorUnder', value)

    async def setDoneMovingWhenZDistErrorUnder(self, value: float):
        await self._connector.set_async('doneMovingWhenZDistErrorUnder', value)

    def _onConnectorMessagePublished(self, msg: list[bytes]):

        msgID = msg[0].decode()
        match msgID:
            case 'signal':
                signalKey = msg[1].decode()
                #logger.debug(f'Emitting {signalKey}')
                getattr(self, signalKey).emit()
                #logger.debug(f'Done emitting {signalKey}')
            case _:
                raise NotImplementedError(f'Unknown message ID: {msgID}')

    async def _monitorConnection(self):
        while True:
            # logger.debug('_monitorConnection')
            try:
                await self._connector.ping_async(timeout=6e3, numTries=2)
            except TimeoutError:
                isConnected = False
            except Exception as e:
                logger.warning(f'Unexpected exception during ping: {exceptionToStr(e)}')
                isConnected = False
            else:
                isConnected = True

            # logger.debug('_monitorConnection: isConnected=%s', isConnected)

            self._isConnectedToServer = isConnected

            if isConnected:
                await asyncio.sleep(10.)
            else:
                await asyncio.sleep(1.)
