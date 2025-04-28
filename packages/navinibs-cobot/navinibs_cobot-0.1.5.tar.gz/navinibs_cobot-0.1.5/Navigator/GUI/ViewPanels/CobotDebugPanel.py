from __future__ import annotations

import asyncio
import attrs
import logging
from packaging.version import Version

import qtawesome as qta
from qtpy import QtWidgets, QtGui
import typing as tp

from NaviNIBS.util.GUI.QScrollContainer import QScrollContainer
from NaviNIBS.Navigator.GUI.ViewPanels.MainViewPanelWithDockWidgets import MainViewPanelWithDockWidgets
from NaviNIBS.util.GUI.ErrorDialog import asyncTryAndRaiseDialogOnError
from NaviNIBS.util.GUI.Dock import Dock, DockArea
from NaviNIBS.util.GUI.Icons import getIcon

from NaviNIBS_Cobot.Devices.CobotTargetingController import CobotTargetingController
from NaviNIBS_Cobot.Navigator.GUI.ViewPanels import CobotWidgets as cw
from NaviNIBS_Cobot.Navigator.Model.CobotConfiguration import CobotControl


logger = logging.getLogger(__name__)


@attrs.define
class CobotStatusWidget:
    _controller: CobotTargetingController
    _wdgt: QtWidgets.QWidget = attrs.field(factory=QtWidgets.QWidget)
    _scroll: QScrollContainer = attrs.field(init=False)
    _items: dict[str, cw.CobotStatusEntry] = attrs.field(init=False, factory=dict)

    def __attrs_post_init__(self):

        layout = QtWidgets.QFormLayout()
        self._scroll = QScrollContainer(innerContainerLayout=layout)
        self._wdgt.setLayout(QtWidgets.QVBoxLayout())
        self._wdgt.layout().setContentsMargins(0, 0, 0, 0)
        self._wdgt.layout().addWidget(self._scroll.scrollArea)

        logger.debug('Initializing status entries')

        items = [
            cw.CobotStateStatusEntry(),
            cw.CobotBoolStatusEntry(
                key='isConnected',
                stateChangedSignal='sigConnectedChanged',
            ),
            cw.CobotBoolStatusEntry(
                key='isEnabled',
                stateChangedSignal='sigEnabledChanged',
            ),
            cw.CobotBoolStatusEntry(
                key='isPoweredOn',
                stateChangedSignal='sigPoweredChanged',
            ),
            cw.CobotBoolStatusEntry(
                key='isHomed',
                stateChangedSignal='sigHomedChanged',
            ),
            cw.CobotBoolStatusEntry(
                key='isMoving',
                stateChangedSignal='sigAxesMovingChanged',
            ),
            cw.CobotBoolStatusEntry(
                key='controlIsLocked',
                stateChangedSignal='sigControlIsLockedChanged',
            ),
            cw.CobotBoolStatusEntry(
                key='isInToleranceToDestination',
                stateChangedSignal='sigInToleranceToDestinationChanged',
            ),
            cw.CobotIsApproximatelyAlignedStatusEntry(),
            cw.CobotBoolStatusEntry(
                key='alignMotionInProgress',
                stateChangedSignal='sigAlignMotionInProgressChanged',
            ),
            cw.CobotInWorkspaceStatusEntry(),
            cw.CobotBoolStatusEntry(
                key='isInExtendedWorkspace',
                stateChangedSignal='sigInWorkspaceChanged',
            ),
            cw.CobotBoolStatusEntry(
                key='alignMotionAborted',
                stateChangedSignal='sigAlignMotionInProgressChanged',
            ),
            cw.CobotBoolStatusEntry(
                key='isFreedriving',
                stateChangedSignal='sigFreedrivingChanged',
            ),
            cw.CobotBoolStatusEntry(
                key='isInProtectiveStop',
                stateChangedSignal='sigInProtectiveStopChanged',
            ),
            cw.CobotBoolStatusEntry(
                key='isServoing',
                stateChangedSignal='sigServoingChanged',
            ),
            cw.CobotBoolStatusEntry(
                key='isInContact',
                stateChangedSignal='sigContactChanged',
            ),
            cw.CobotBoolStatusEntry(
                key='isRetracted',
                stateChangedSignal='sigServoingChanged',
            ),
            cw.CobotBoolStatusEntry(
                key='freedriveButtonIsPressed',
                stateChangedSignal='sigFreedriveButtonPressedChanged',
            ),
            cw.CobotForceStatusEntry(),
            cw.CobotForceLastCheckedStatusEntry(),
        ]

        if Version('.'.join(str(x) for x in self._controller.cobotClient.cobotControllerVersion)) >= Version('2.2'):
            items.extend([
                cw.CobotRawCoilIDValueStatusEntry(),
                cw.CobotRawForceValueStatusEntry(),
            ])

        items.append(
            cw.CobotSensitivityEntry()
        )

        for deviceName in ('COBOT', 'ARM'):
            for index in range(6):
                items.append(cw.CobotJointPositionStatusEntry(
                    key=f'{deviceName}J{index}',
                    deviceName=deviceName,
                    index=index,
                    label=f'{deviceName.title()} j{index+1}',
                ))

        for item in items:
            logger.debug(f'Adding item {item.key}')
            item.controller = self._controller
            layout.addRow(item.label, item.wdgt)
            self._items[item.key] = item

    @property
    def wdgt(self):
        return self._wdgt


@attrs.define
class CobotControlsWidget:
    _controller: CobotTargetingController
    _wdgt: QtWidgets.QWidget = attrs.field(factory=QtWidgets.QWidget)
    _items: dict[str, cw.CobotControlEntry] = attrs.field(init=False, factory=dict)

    def __attrs_post_init__(self):
        layout = QtWidgets.QFormLayout()
        self._wdgt.setLayout(layout)

        logger.debug('Initializing control entries')

        # TODO: rewrite below to not use class with so much embedded structure, since
        # requirements vary so much between controls in terms of enabled states, callbacks, etc.
        # (also need to update to account for async methods)

        items = []
        items.append(cw.CobotEStopControlEntry(controller=self._controller))
        items.append(cw.CobotConnectionControlEntry(controller=self._controller))
        items.append(cw.CobotSessionControlEntry(controller=self._controller))
        items.append(cw.CobotPowerControlEntry(controller=self._controller))
        items.append(cw.CobotHomingControlEntry(controller=self._controller))
        items.append(cw.CobotCheckForceControlEntry(controller=self._controller))
        items.append(cw.CobotStopControlEntry(controller=self._controller))
        items.append(cw.CobotFreedriveControlEntry(controller=self._controller))
        items.append(cw.CobotMoveToParkControlEntry(controller=self._controller))
        items.append(cw.CobotMoveToWelcomeControlEntry(controller=self._controller, positionIndex=0, key='moveToWelcome0'))
        items.append(cw.CobotMoveToWelcomeControlEntry(controller=self._controller, positionIndex=1, key='moveToWelcome1'))
        items.append(cw.CobotServoControlEntry(controller=self._controller))
        items.append(cw.CobotResumeAfterProtectiveStopControlEntry(controller=self._controller))

        for item in items:
            assert item.key not in self._items
            self._items[item.key] = item
            layout.addRow(item.label, item.wdgt)

        layout.addRow('', QtWidgets.QWidget())  # empty spacer

        items = []
        items.append(cw.CobotTrackTargetControlEntry(controller=self._controller))
        items.append(cw.CobotContactModeControlEntry(controller=self._controller))
        items.append(cw.CobotCancelActionSequencesControlEntry(controller=self._controller))
        for item in items:
            assert item.key not in self._items
            self._items[item.key] = item
            layout.addRow(item.label, item.wdgt)


@attrs.define
class CobotDebugPanel(MainViewPanelWithDockWidgets):
    _key: str = 'CobotDebug'
    _label: str = 'Cobot info'
    _icon: QtGui.QIcon = attrs.field(init=False, factory=lambda: getIcon('mdi6.robot-industrial'))

    _statusWdgt: CobotStatusWidget = attrs.field(init=False)
    _controlsWdgt: CobotControlsWidget = attrs.field(init=False)

    _controller: CobotTargetingController | None = attrs.field(init=False, default=None)

    def __attrs_post_init__(self):
        super().__attrs_post_init__()

    def canBeEnabled(self) -> tuple[bool, str | None]:
        if self.session is None:
            return False, 'No session set'
        return True, None

    def _finishInitialization(self):
        super()._finishInitialization()

        if self.session is not None:
            self._onPanelInitializedAndSessionSet()

    def _onSessionSet(self):
        super()._onSessionSet()

        if self._hasInitialized:
            self._onPanelInitializedAndSessionSet()

    def _onPanelInitializedAndSessionSet(self):
        asyncio.create_task(asyncTryAndRaiseDialogOnError(self._onPanelInitalizedAndSessionSet_async))

    async def _onPanelInitalizedAndSessionSet_async(self):
        """
        Finish setup after controller is fully ready without blocking UI while waiting for controller
        """
        assert self._controller is None
        config = self.session.addons['NaviNIBS_Cobot'].cobotControl
        assert isinstance(config, CobotControl)

        statusDock, statusContainer = self._createDockWidget(title='Cobot status')
        self._wdgt.addDock(statusDock, position='left')

        controlsDock, controlsContainer = self._createDockWidget(title='Cobot controls')

        self._wdgt.addDock(controlsDock, position='right',
                           relativeTo=statusDock)

        if config.controller is None:
            await config.initializeController(session=self.session)
            # note that this awaits until controller is actually ready

        self._controller = config.controller

        logger.debug('Initializing cobot status widget')
        self._statusWdgt = CobotStatusWidget(controller=self._controller, wdgt=statusContainer)

        logger.debug('Initializing cobot controls widget')

        self._controlsWdgt = CobotControlsWidget(controller=self._controller, wdgt=controlsContainer)

        logger.debug('Done initializing CobotDebugPanel')


