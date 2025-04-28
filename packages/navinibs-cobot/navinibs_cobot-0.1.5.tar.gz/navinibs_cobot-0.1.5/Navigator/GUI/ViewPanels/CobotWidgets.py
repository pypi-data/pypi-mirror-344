from __future__ import annotations

from abc import ABC, abstractmethod
import asyncio
import attrs
from contextlib import contextmanager
from datetime import datetime
from enum import IntEnum
from math import ceil, floor
import logging
import typing as tp
import qtawesome as qta
from qtpy import QtWidgets, QtGui, QtCore

from NaviNIBS.util.Asyncio import asyncTryAndLogExceptionOnError
from NaviNIBS.util.GUI.ErrorDialog import raiseErrorDialog
from NaviNIBS.util.GUI.IconWidget import IconWidget
from NaviNIBS.util.GUI.QMouseWheelAdjustmentGuard import preventAnnoyingScrollBehaviour
from NaviNIBS.util.Signaler import Signal
from NaviNIBS_Cobot.Devices.CobotTargetingController import CobotTargetingController
from NaviNIBS_Cobot.Devices.CobotConnector import TargetingState, ContactMode, TargetChangeRetractMode, TargetChangeContactMode


logger = logging.getLogger(__name__)


@attrs.define(kw_only=True, slots=False)
class CobotStatusEntry(ABC):
    _key: str
    _stateChangedSignal: Signal | str | None
    _label: str | None = None
    _controller: CobotTargetingController | None = None
    _wdgt: QtWidgets.QWidget = attrs.field(init=False)

    _valueRecentlyChangedEvent: asyncio.Event = attrs.field(init=False, factory=asyncio.Event)
    _updateRateLimit: float = attrs.field(default=5)  # in Hz

    def __attrs_post_init__(self):
        if self._stateChangedSignal is not None and not isinstance(self._stateChangedSignal, str):
            self._stateChangedSignal.connect(self._onValueJustChanged)
        if self._controller is not None:
            if isinstance(self._stateChangedSignal, str):
                self._stateChangedSignal = getattr(self._controller.cobotClient, self._stateChangedSignal)
            if self._stateChangedSignal is not None:
                self._stateChangedSignal.connect(self._onValueJustChanged)
        # subclasses should call _onValueChanged() in their __attrs_post_init__()

        asyncio.create_task(asyncTryAndLogExceptionOnError(self._loop_handleUpdates))

    @property
    def key(self):
        return self._key

    @property
    def label(self):
        return self._label if self._label is not None else self._key

    @property
    def controller(self):
        return self._controller

    def _setStateChangedSignal(self):
        """
        Packaged in separate method for subclasses to optionally override. Called when controller changes, immediately
        before connecting to stateChangedSignal.
        """
        if isinstance(self._stateChangedSignal, str):
            self._stateChangedSignal = getattr(self._controller.cobotClient, self._stateChangedSignal)

    @controller.setter
    def controller(self, controller: CobotTargetingController | None):
        if controller is self._controller:
            return
        if self._controller is not None:
            raise NotImplementedError

        self._controller = controller

        self._setStateChangedSignal()
        self._stateChangedSignal.connect(self._onValueChanged)
        self._onValueChanged()

    @property
    def wdgt(self):
        return self._wdgt

    @abstractmethod
    def _onValueChanged(self):
        raise NotImplementedError()

    def _onValueJustChanged(self):
        self._valueRecentlyChangedEvent.set()

    async def _loop_handleUpdates(self):
        while True:
            await self._valueRecentlyChangedEvent.wait()
            await asyncio.sleep(1/self._updateRateLimit)
            self._valueRecentlyChangedEvent.clear()
            self._onValueChanged()


@attrs.define(kw_only=True)
class CobotBoolStatusEntry(CobotStatusEntry):
    _initialIcon: QtGui.QIcon = attrs.field(factory=lambda: qta.icon('mdi6.progress-question', color='gray'))
    _iconWhenTrue: QtGui.QIcon = attrs.field(factory=lambda: qta.icon('mdi6.checkbox-marked-circle', color='blue'))
    _iconWhenFalse: QtGui.QIcon = attrs.field(factory=lambda: qta.icon('mdi6.close-circle-outline', color='red'))

    _wdgt: IconWidget = attrs.field(init=False)

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        self._wdgt = IconWidget(icon=self._initialIcon)
        self._onValueChanged()

    def _onValueChanged(self):
        if self._controller is None:
            return
        newVal = getattr(self._controller.cobotClient, self._key)
        self._wdgt.icon = self._iconWhenTrue if newVal else self._iconWhenFalse


@attrs.define(kw_only=True)
class CobotNumericStatusEntry(CobotStatusEntry):
    _initialText: str = '---'
    _wdgt: QtWidgets.QLabel = attrs.field(init=False, factory=QtWidgets.QLabel)

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        self._wdgt.setText(self._initialText)
        self._onValueChanged()

    def _valToStr(self, val: tp.Any) -> str:
        return str(val)

    def _onValueChanged(self):
        if self._controller is None:
            self._wdgt.setText(self._initialText)
            return
        newVal = getattr(self._controller.cobotClient, self._key)
        self._wdgt.setText(self._valToStr(newVal))


@attrs.define(kw_only=True)
class CobotRawCoilIDValueStatusEntry(CobotNumericStatusEntry):
    _key: str = 'lastRawCoilIDValue'
    _stateChangedSignal: Signal | str = 'sigRawCoilIDValueChanged'

    def _valToStr(self, val: tp.Any) -> str:
        return f'{val} V'


@attrs.define(kw_only=True)
class CobotRawForceValueStatusEntry(CobotNumericStatusEntry):
    _key: str = 'lastRawForceValue'
    _stateChangedSignal: Signal | str = 'sigRawForceValueChanged'

    def _valToStr(self, val: tp.Any) -> str:
        return f'{val} V'


@attrs.define(kw_only=True)
class CobotInWorkspaceStatusEntry(CobotBoolStatusEntry):
    _key: str = 'isInWorkspace'
    _stateChangedSignal: str = 'sigInWorkspaceChanged'


@attrs.define(kw_only=True)
class CobotIsApproximatelyAlignedStatusEntry(CobotBoolStatusEntry):
    _key: str = 'isApproximatelyAligned'
    _stateChangedSignal: str = 'sigIsApproximatelyAlignedChanged'


@attrs.define(kw_only=True)
class CobotStateStatusEntry(CobotStatusEntry):
    _key: str = 'state'
    _stateChangedSignal: Signal | str = 'sigStateChanged'
    _wdgt: QtWidgets.QLabel = attrs.field(init=False, factory=QtWidgets.QLabel)
    _enumNiceNameMapping: dict[E, str] = attrs.field(init=False, factory=dict)

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        self._wdgt.setText('---')
        self._onValueChanged()

    def _onValueChanged(self):
        if self._controller is None:
            self._wdgt.setText('---')
            return

        match self._controller.cobotClient.cachedState:
            case TargetingState.PROTECTIVE_STOPPED:
                niceName = 'Protective stopped'

            case _:
                niceName = self._controller.cobotClient.cachedState.name
                niceName = niceName.replace('_', ', ').capitalize()

        logger.info(f'Setting state status to {niceName}')
        self._wdgt.setText(niceName)


@attrs.define(kw_only=True)
class CobotTargetLabelStatusEntry(CobotStatusEntry):
    _key: str = 'target'
    _stateChangedSignal: Signal | str = 'sigTargetLabelChanged'
    _wdgt: QtWidgets.QLabel = attrs.field(init=False, factory=QtWidgets.QLabel)

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        self._wdgt.setText('---')
        self._onValueChanged()

    def _onValueChanged(self):
        if self._controller is None:
            self._wdgt.setText('---')
            return
        self._wdgt.setText(self._controller.cobotClient.targetLabel)


@attrs.define(kw_only=True)
class CobotForceStatusEntry(CobotStatusEntry):
    _key: str = 'force'
    _stateChangedSignal: Signal | str = 'sigMeasuredForceChanged'
    _wdgt: QtWidgets.QWidget = attrs.field(init=False, factory=QtWidgets.QWidget)
    _numForceLevels: int = 5
    _levelWdgts: list[IconWidget] = attrs.field(init=False, factory=list)

    _icons: dict[tuple[int, int | None], QtGui.QIcon] = attrs.field(init=False, factory=dict)

    def __attrs_post_init__(self):
        super().__attrs_post_init__()

        self._wdgt.setLayout(QtWidgets.QHBoxLayout())
        self._wdgt.layout().setContentsMargins(0, 0, 0, 0)
        self._wdgt.layout().setSpacing(0)

        for level in range(self._numForceLevels):
            levelWdgt = IconWidget(icon=self._getIcon(level=level, state=None),
                                   size=QtCore.QSize(20, 20))
            self._levelWdgts.append(levelWdgt)
            self._wdgt.layout().addWidget(levelWdgt)

        self._wdgt.layout().addStretch()

        self._onValueChanged()

    @property
    def numForceLevels(self):
        return self._numForceLevels

    def _getIcon(self, level: int, state: int | None) -> QtGui.QIcon:
        key = (level, state)
        if key not in self._icons:
            if state is None:
                iconColor = 'gray'
                iconName = 'mdi6.help-box'
            else:
                if level <= state:
                    iconColor = ['gray', 'green', 'goldenrod', 'orange', 'red'][state]
                    if level == state:
                        iconName = f'mdi6.numeric-{level}-box'
                    else:
                        iconName = f'mdi6.checkbox-blank'
                else:
                    iconColor = 'gray'
                    iconName = f'mdi6.checkbox-blank-outline'

            self._icons[key] = qta.icon(iconName, color=iconColor)

        return self._icons[key]

    def _onValueChanged(self):
        if self._controller is None:
            for level in range(self._numForceLevels):
                self._levelWdgts[level].icon = self._getIcon(level=level, state=None)
            return

        force = self._controller.cobotClient.lastMeasuredForce
        for level, levelWdgt in enumerate(self._levelWdgts):
            levelWdgt.icon = self._getIcon(level=level,
                                           state=int(force) if force is not None else None)


@attrs.define(kw_only=True)
class CobotForceLastCheckedStatusEntry(CobotStatusEntry):
    _key: str = 'forceLastCheckedAtTime'
    _stateChangedSignal: Signal | str | None = None
    _wdgt: QtWidgets.QLabel = attrs.field(init=False, factory=QtWidgets.QLabel)

    def __attrs_post_init__(self):
        if self._controller is not None:
            self._setStateChangedSignal()

        super().__attrs_post_init__()
        self._wdgt.setText('---')
        self._onValueChanged()

    def _setStateChangedSignal(self):
        assert self._stateChangedSignal is None
        assert self._controller is not None
        self._stateChangedSignal = self._controller.configuration.sigConfigChanged

    def _onValueChanged(self, attribsChanged: list[str] | None = None):
        if self._controller is None:
            self._wdgt.setText('---')
            return

        if attribsChanged is not None and 'forceLastCheckedAtTime' not in attribsChanged:
            return

        timeStr = self._controller.configuration.forceLastCheckedAtTime

        if timeStr is None:
            self._wdgt.setText('None')
            return

        self._wdgt.setText(datetime.strptime(timeStr,
            '%y%m%d%H%M%S.%f').strftime('%Y-%m-%d %H:%M:%S'))


@attrs.define(kw_only=True)
class CobotControlEntry(ABC):
    _key: str
    _label: str | None = None
    _controller: CobotTargetingController | None = None
    _wdgt: QtWidgets.QWidget = attrs.field(init=False)

    def __attrs_post_init__(self):
        pass

    @property
    def key(self):
        return self._key

    @property
    def label(self):
        return self._label if self._label is not None else self._key

    @property
    def wdgt(self):
        return self._wdgt

    def _createTaskAndCatchExceptions(self, coro: tp.Awaitable):
        async def _coro():
            try:
                await coro
            except Exception as e:
                raiseErrorDialog(title='Cobot error', exception=e)

        asyncio.create_task(_coro())


@attrs.define(kw_only=True)
class CobotButtonControlEntry(CobotControlEntry):
    _wdgt: QtWidgets.QPushButton = attrs.field(init=False, factory=QtWidgets.QPushButton)

    def __attrs_post_init__(self):
        self._wdgt.clicked.connect(lambda *args: self._onButtonPressed())

    def _onButtonPressed(self):
        raise NotImplementedError()  # should be implemented by subclass


@attrs.define(kw_only=True)
class CobotConnectionControlEntry(CobotButtonControlEntry):
    _key: str = 'connect'
    _label: str | None = 'Connection'

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        self._controller.cobotClient.sigConnectedChanged.connect(self._updateText)
        self._updateText()

    def _updateText(self):
        self._wdgt.setText('Disconnect' if self._controller.cobotClient.isConnected else 'Connect')

    def _onButtonPressed(self):
        if self._controller.cobotClient.isConnected:
            self._createTaskAndCatchExceptions(self._controller.cobotClient.disconnectCobotClient())
        else:
            self._createTaskAndCatchExceptions(self._controller.cobotClient.connectCobotClient())


@attrs.define(kw_only=True)
class CobotSessionControlEntry(CobotButtonControlEntry):
    _key: str = 'session'
    _label: str | None = 'Session'

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        self._controller.cobotClient.sigConnectedChanged.connect(self._updateEnabled)
        self._controller.cobotClient.sigControlIsLockedChanged.connect(self._updateText)
        self._updateEnabled()
        self._updateText()

    def _updateEnabled(self):
        self._wdgt.setEnabled(self._controller.cobotClient.isConnected)

    def _updateText(self):
        self._wdgt.setText('End session' if self._controller.cobotClient.controlIsLocked else 'Start session')

    def _onButtonPressed(self):
        if self._controller.cobotClient.controlIsLocked:
            self._createTaskAndCatchExceptions(self._controller.cobotClient.endSession())
        else:
            self._createTaskAndCatchExceptions(self._controller.cobotClient.startSession())


@attrs.define(kw_only=True)
class CobotHomingControlEntry(CobotButtonControlEntry):
    _key: str = 'homing'
    _label: str | None = 'Homing'

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        self._controller.cobotClient.sigControlIsLockedChanged.connect(self._updateEnabled)
        self._controller.cobotClient.sigPoweredChanged.connect(self._updateEnabled)
        self._controller.cobotClient.sigHomedChanged.connect(self._updateText)
        self._updateEnabled()
        self._updateText()

    def _updateEnabled(self):
        self._wdgt.setEnabled(self._controller.cobotClient.controlIsLocked
                              and self._controller.cobotClient.isPoweredOn)

    def _updateText(self):
        self._wdgt.setText('Calibrate' if not self._controller.cobotClient.isHomed else 'Clear calibration')

    def _onButtonPressed(self):
        if not self._controller.cobotClient.isHomed:
            self._createTaskAndCatchExceptions(self._controller.cobotClient.startHoming())
        else:
            self._createTaskAndCatchExceptions(self._controller.cobotClient.clearHoming())


@attrs.define(kw_only=True)
class CobotPowerControlEntry(CobotButtonControlEntry):
    _key: str = 'powerOn'
    _label: str | None = 'Power'

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        self._controller.cobotClient.sigControlIsLockedChanged.connect(self._updateEnabled)
        self._controller.cobotClient.sigPoweredChanged.connect(self._updateText)
        self._updateEnabled()
        self._updateText()

    def _updateEnabled(self):
        self._wdgt.setEnabled(self._controller.cobotClient.controlIsLocked)

    def _updateText(self):
        self._wdgt.setText('Power off' if self._controller.cobotClient.isPoweredOn else 'Power on')

    def _onButtonPressed(self):
        if self._controller.cobotClient.isPoweredOn:
            self._createTaskAndCatchExceptions(self._controller.cobotClient.powerOff())
        else:
            self._createTaskAndCatchExceptions(self._controller.cobotClient.powerOn())


@attrs.define(kw_only=True)
class CobotConnectAndInitializeControlEntry(CobotButtonControlEntry):
    _key: str = 'connectAndInitialize'
    _label: str | None = 'Connection'

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        self._controller.cobotClient.sigStateChanged.connect(self._updateText)
        self._updateText()

    def _updateText(self):
        match self._controller.cobotClient.state:
            case TargetingState.DISCONNECTED:
                self._wdgt.setText('Connect and initialize')

            case TargetingState.UNINITIALIZED:
                self._wdgt.setText('Initialize')

            case _:
                self._wdgt.setText('Disconnect')

    def _onButtonPressed(self):
        match self._controller.cobotClient.state:
            case TargetingState.DISCONNECTED:
                self._createTaskAndCatchExceptions(self._controller.cobotClient.connectToCobotAndInitialize())

            case TargetingState.UNINITIALIZED:
                self._createTaskAndCatchExceptions(self._controller.cobotClient.connectToCobotAndInitialize())

            case _:
                self._createTaskAndCatchExceptions(self._controller.cobotClient.disconnectCobotClient())


@attrs.define(kw_only=True)
class CobotStopControlEntry(CobotButtonControlEntry):
    _key: str = 'stop'
    _label: str | None = 'Stop'

    def __attrs_post_init__(self):
        super().__attrs_post_init__()

        self._controller.cobotClient.sigStateChanged.connect(self._updateEnabled)
        self._controller.cobotClient.sigStateChanged.connect(self._updateText)

        self._updateEnabled()
        self._updateText()

    def _updateEnabled(self):
        state = self._controller.cobotClient.cachedState
        self._wdgt.setEnabled(state in (
            TargetingState.FREEDRIVING,
            TargetingState.UNALIGNED_SERVOING,
            TargetingState.UNALIGNED_CONTACTING,
            TargetingState.ALIGNED_SERVOING,
            TargetingState.ALIGNED_CONTACTING,
            TargetingState.ALIGNING_SERVOING,
            TargetingState.ALIGNING_CONTACTING,
            TargetingState.ALIGNING_RETRACTING,
            TargetingState.ALIGNING_RETRACTED,
            TargetingState.MOVING,
            TargetingState.MOVED
        ))

    def _updateText(self):
        state = self._controller.cobotClient.cachedState
        if state in (
            TargetingState.FREEDRIVING,
        ):
            self._wdgt.setText('Stop freedriving')
        elif state in (
            TargetingState.UNALIGNED_SERVOING,
            TargetingState.UNALIGNED_CONTACTING,
            TargetingState.ALIGNED_SERVOING,
            TargetingState.ALIGNED_CONTACTING,
            TargetingState.ALIGNING_SERVOING,
            TargetingState.ALIGNING_CONTACTING,
        ):
            self._wdgt.setText('Stop contact')
        elif state in (
            TargetingState.ALIGNING_RETRACTING,
            TargetingState.ALIGNING_RETRACTED,
            TargetingState.MOVING,
        ):
            self._wdgt.setText('Stop align')
        else:
            self._wdgt.setText('Stop')

    def _onButtonPressed(self):
        self._createTaskAndCatchExceptions(self._controller.cobotClient.stop())


@attrs.define(kw_only=True)
class CobotEStopControlEntry(CobotButtonControlEntry):
    _key: str = 'estop'
    _label: str | None = 'E-Stop'

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        self._wdgt.setText('Emergency stop')
        self._controller.cobotClient.sigConnectedChanged.connect(self._updateEnabled)
        self._updateEnabled()

    def _updateEnabled(self):
        self._wdgt.setEnabled(self._controller.cobotClient.isConnected)

    def _onButtonPressed(self):
        self._createTaskAndCatchExceptions(self._controller.cobotClient.estop())


@attrs.define(kw_only=True)
class CobotFreedriveControlEntry(CobotButtonControlEntry):
    _key: str = 'freedrive'
    _label: str | None = 'Freedrive'

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        self._controller.cobotClient.sigStateChanged.connect(self._updateEnabled)
        self._controller.cobotClient.sigStateChanged.connect(self._updateText)
        self._updateEnabled()
        self._updateText()

    def _updateEnabled(self):
        self._wdgt.setEnabled(self._controller.cobotClient.cachedState in (
            TargetingState.FREEDRIVING,
            TargetingState.IDLE,
        ))

    def _updateText(self):
        self._wdgt.setText('Stop freedriving' if self._controller.cobotClient.cachedState in (TargetingState.FREEDRIVING,) else 'Start freedriving')

    def _onButtonPressed(self):
        if self._controller.cobotClient.isFreedriving:
            self._createTaskAndCatchExceptions(self._controller.cobotClient.stopFreedrive())
        else:
            self._createTaskAndCatchExceptions(self._controller.cobotClient.startFreedrive())


@attrs.define(kw_only=True)
class CobotMoveToControlEntry(CobotButtonControlEntry, ABC):
    _label: str | None = 'Move to...'

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        self._controller.cobotClient.sigControlIsLockedChanged.connect(self._updateEnabled)
        self._controller.cobotClient.sigPoweredChanged.connect(self._updateEnabled)
        self._controller.cobotClient.sigHomedChanged.connect(self._updateEnabled)
        self._controller.cobotClient.sigInWorkspaceChanged.connect(self._updateEnabled)
        self._updateEnabled()

    def _updateEnabled(self):
        # TODO: update these to be more specific (e.g. cannot do one of these movement actions until after coil is retracted)
        self._wdgt.setEnabled(
            self._controller.cobotClient.controlIsLocked
            and self._controller.cobotClient.isPoweredOn
            and self._controller.cobotClient.isHomed
            and self._controller.cobotClient.isInExtendedWorkspace)


@attrs.define(kw_only=True)
class CobotMoveToParkControlEntry(CobotMoveToControlEntry):
    _key: str = 'moveToPark'

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        self._wdgt.setText('Move to park')

    def _onButtonPressed(self):
        self._createTaskAndCatchExceptions(self._controller.cobotClient.startMovingToPark())


@attrs.define(kw_only=True)
class CobotMoveToWelcomeControlEntry(CobotMoveToControlEntry):
    _positionIndex: int

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        self._wdgt.setText(f'Move to welcome {self._positionIndex}')

    def _onButtonPressed(self):
        self._createTaskAndCatchExceptions(self._controller.cobotClient.startMovingToWelcome(positionIndex=self._positionIndex))


@attrs.define(kw_only=True)
class CobotServoControlEntry(CobotButtonControlEntry):
    _key: str = 'servo'
    _label: str | None = 'Servoing'

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        self._controller.cobotClient.sigControlIsLockedChanged.connect(self._updateEnabled)
        self._controller.cobotClient.sigPoweredChanged.connect(self._updateEnabled)
        self._controller.cobotClient.sigHomedChanged.connect(self._updateEnabled)
        self._controller.cobotClient.sigInWorkspaceChanged.connect(self._updateEnabled)
        self._controller.cobotClient.sigServoingChanged.connect(self._updateText)
        self._updateEnabled()
        self._updateText()

    def _updateEnabled(self):
        self._wdgt.setEnabled(self._controller.cobotClient.controlIsLocked
                              and self._controller.cobotClient.isPoweredOn
                              and self._controller.cobotClient.isHomed
                              and self._controller.cobotClient.isInWorkspace)

    def _updateText(self):
        self._wdgt.setText('Stop contact (low level)' if self._controller.cobotClient.isServoing else 'Start contact (low level)')

    def _onButtonPressed(self):
        if self._controller.cobotClient.isServoing:
            self._createTaskAndCatchExceptions(self._controller.cobotClient.stopContact_lowLevel())
        else:
            self._createTaskAndCatchExceptions(self._controller.cobotClient.startContact_lowLevel())


@attrs.define(kw_only=True)
class CobotContactControlEntry(CobotButtonControlEntry):
    _key: str = 'contact'
    _label: str | None = 'Contact'
    _doOpenForceCheckIfTimedOut: bool = True

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        self._controller.cobotClient.sigStateChanged.connect(self._updateEnabled)
        self._controller.cobotClient.sigStateChanged.connect(self._updateText)
        self._controller.cobotClient.sigInWorkspaceChanged.connect(self._updateEnabled)
        self._updateEnabled()
        self._updateText()

    def _isTryingToContact(self):
        return self._controller.cobotClient.cachedState in (
            TargetingState.ALIGNED_SERVOING,
            TargetingState.ALIGNED_CONTACTING,
            TargetingState.ALIGNING_SERVOING,
            TargetingState.ALIGNING_CONTACTING,
            TargetingState.UNALIGNED_SERVOING,
            TargetingState.UNALIGNED_CONTACTING,
            TargetingState.MOVING,
            TargetingState.MOVED,
            TargetingState.MOVED_FROZEN
        )

    def _canTryToContact(self):
        return self._controller.cobotClient.isInWorkspace and self._controller.cobotClient.cachedState not in (
            TargetingState.FREEDRIVING,
            TargetingState.UNINITIALIZED,
            TargetingState.DISCONNECTED,
        )

    def _updateEnabled(self):
        self._wdgt.setEnabled(self._isTryingToContact() or self._canTryToContact())

    def _updateText(self):
        if self._isTryingToContact():
            self._wdgt.setText('Stop contact')
        else:
            self._wdgt.setText('Start contact')

    def _onButtonPressed(self):
        if self._isTryingToContact():
            self._createTaskAndCatchExceptions(self._controller.cobotClient.stopContact())
        else:
            if self._controller.needsForceCheck:
                self._createTaskAndCatchExceptions(self._startContactAfterForceCheck())
            else:
                self._createTaskAndCatchExceptions(self._controller.cobotClient.startContact())

    async def _startContactAfterForceCheck(self):
        from NaviNIBS_Cobot.Navigator.GUI.ViewPanels.CheckForceSensorDialog import CheckForceSensorDialog
        dialog = CheckForceSensorDialog(parent=self._wdgt, controller=self._controller)
        dialog.show()

        await dialog.dialogFinishedEvent.wait()

        if not self._controller.needsForceCheck:
            # check was successful
            await self._controller.cobotClient.startContact()


@attrs.define(kw_only=True)
class CobotSetTargetControlEntry(CobotButtonControlEntry):
    _key: str = 'setTarget'
    _label: str | None = 'Set Cobot target'

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        self._wdgt.setText('Set target')
        self._controller.cobotClient.sigControlIsLockedChanged.connect(self._updateEnabled)
        self._controller.cobotClient.sigPoweredChanged.connect(self._updateEnabled)
        self._controller.cobotClient.sigHomedChanged.connect(self._updateEnabled)
        self._controller.targetingCoordinator.sigCurrentTargetChanged.connect(self._updateEnabled)
        self._updateEnabled()

    def _updateEnabled(self):
        self._wdgt.setEnabled(self._controller.cobotClient.controlIsLocked
                              and self._controller.cobotClient.isPoweredOn
                              and self._controller.cobotClient.isHomed
                              and self._controller.targetingCoordinator.currentTarget is not None)

    def _onButtonPressed(self):
        target = self._controller.targetingCoordinator.currentTarget
        self._createTaskAndCatchExceptions(self._controller.cobotClient.setTargetingInfo(
            targetLabel=target.key,
            targetCoilToMRITransf=target.coilToMRITransf))


@attrs.define(kw_only=True)
class CobotSetTargetOrAutosetControlEntry(CobotControlEntry):
    _key: str = 'setTargetOrAutoset'
    _label: str | None = 'Set Cobot target or autoset'
    _setTargetButton: QtWidgets.QPushButton = attrs.field(init=False)
    _autosetCheckbox: QtWidgets.QCheckBox = attrs.field(init=False)
    _doAutoset: bool = True

    def __attrs_post_init__(self):
        super().__attrs_post_init__()

        self._wdgt = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self._wdgt.setLayout(layout)

        self._setTargetButton = QtWidgets.QPushButton('Set target')
        self._setTargetButton.clicked.connect(self._onSetTargetButtonPressed)
        layout.addWidget(self._setTargetButton)
        self._autosetCheckbox = QtWidgets.QCheckBox('Autoset')
        if self._doAutoset:
            self._autosetCheckbox.setChecked(True)
        self._autosetCheckbox.stateChanged.connect(self._onAutosetCheckboxStateChanged)
        layout.addWidget(self._autosetCheckbox)

        self._controller.cobotClient.sigStateChanged.connect(self._updateEnabled)
        self._controller.targetingCoordinator.sigCurrentTargetChanged.connect(self._updateEnabled)
        self._controller.targetingCoordinator.sigCurrentTargetChanged.connect(self._onCurrentTargetChanged)
        self._updateEnabled()

        if self._doAutoset:
            self._setTarget()

    @property
    def setTargetButton(self):
        return self._setTargetButton

    @property
    def autosetCheckbox(self):
        return self._autosetCheckbox

    def _updateEnabled(self):
        if self._controller.cobotClient.cachedState in (TargetingState.UNINITIALIZED,):
            self._wdgt.setEnabled(False)
        else:
            self._wdgt.setEnabled(True)

        self._setTargetButton.setEnabled(not self._doAutoset)

    def _onSetTargetButtonPressed(self):
        self._setTarget()

    def _onAutosetCheckboxStateChanged(self, state: int):
        self._doAutoset = self._autosetCheckbox.isChecked()
        self._updateEnabled()
        if self._doAutoset:
            self._setTarget()

    def _setTarget(self):
        target = self._controller.targetingCoordinator.currentTarget
        if target is None:
            return
        self._createTaskAndCatchExceptions(self._controller.cobotClient.setTargetingInfo(
            targetLabel=target.key,
            targetCoilToMRITransf=target.coilToMRITransf))

    def _onCurrentTargetChanged(self):
        if self._doAutoset:
            self._setTarget()


@attrs.define(kw_only=True)
class CobotTrackTargetControlEntry(CobotButtonControlEntry):
    _key: str = 'trackTarget'
    _label: str | None = 'Tracking'

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        self._controller.cobotClient.sigInWorkspaceChanged.connect(self._updateEnabled)
        self._controller.cobotClient.sigTargetAccessibleChanged.connect(self._updateEnabled)
        self._controller.cobotClient.sigStateChanged.connect(self._updateEnabled)
        self._controller.cobotClient.sigStateChanged.connect(self._updateText)
        self._updateEnabled()
        self._updateText()

    def _updateEnabled(self):
        enabled = False
        if self._controller.cobotClient.cachedState not in (TargetingState.UNINITIALIZED,):
            if self._controller.cobotClient.targetIsAccessible and self._controller.cobotClient.isInWorkspace:
                enabled = True
            elif self._controller.cobotClient.cachedState in (
                    TargetingState.ALIGNED_RETRACTED,
                    TargetingState.ALIGNED_SERVOING,
                    TargetingState.ALIGNED_CONTACTING,
                    TargetingState.ALIGNED_RETRACTING,
                    TargetingState.ALIGNING_RETRACTED,
                    TargetingState.ALIGNING_SERVOING,
                    TargetingState.ALIGNING_CONTACTING,
                    TargetingState.ALIGNING_RETRACTING,
                    TargetingState.MOVING):
                enabled = True

        self._wdgt.setEnabled(enabled)

    def _updateText(self):
        if self._controller.cobotClient.cachedState in (
                TargetingState.ALIGNED_RETRACTED,
                TargetingState.ALIGNED_SERVOING,
                TargetingState.ALIGNED_CONTACTING,
                TargetingState.ALIGNED_RETRACTING,
                TargetingState.ALIGNING_RETRACTED,
                TargetingState.ALIGNING_SERVOING,
                TargetingState.ALIGNING_CONTACTING,
                TargetingState.ALIGNING_RETRACTING,
        ):
            self._wdgt.setText('Stop aligning')

        elif self._controller.cobotClient.cachedState in (
                TargetingState.MOVING,
                TargetingState.MOVED):
            self._wdgt.setText('Stop moving')

        else:
            self._wdgt.setText('Start aligning')

    def _onButtonPressed(self):
        if self._controller.cobotClient.cachedState in (
                TargetingState.ALIGNED_RETRACTED,
                TargetingState.ALIGNED_SERVOING,
                TargetingState.ALIGNED_CONTACTING,
                TargetingState.ALIGNED_RETRACTING,
                TargetingState.ALIGNING_RETRACTED,
                TargetingState.ALIGNING_SERVOING,
                TargetingState.ALIGNING_CONTACTING,
                TargetingState.ALIGNING_RETRACTING,
                TargetingState.MOVING):
            self._createTaskAndCatchExceptions(self._controller.stopTrackingTarget())
        else:
            self._createTaskAndCatchExceptions(self._controller.startTrackingTarget())


@attrs.define(kw_only=True)
class CobotCheckForceControlEntry(CobotButtonControlEntry):
    _key: str = 'checkForce'
    _label: str | None = 'Force'

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        self._controller.cobotClient.sigControlIsLockedChanged.connect(self._updateEnabled)
        self._controller.cobotClient.sigPoweredChanged.connect(self._updateEnabled)
        self._controller.cobotClient.sigHomedChanged.connect(self._updateEnabled)
        self._updateEnabled()
        self._wdgt.setText('Check sensor...')

    def _updateEnabled(self):
        self._wdgt.setEnabled(self._controller.cobotClient.controlIsLocked
                              and self._controller.cobotClient.isPoweredOn
                              and self._controller.cobotClient.isHomed)

    def _onButtonPressed(self):
        from NaviNIBS_Cobot.Navigator.GUI.ViewPanels.CheckForceSensorDialog import CheckForceSensorDialog
        dialog = CheckForceSensorDialog(parent=self._wdgt, controller=self._controller)
        dialog.show()


@attrs.define(kw_only=True, slots=False)
class CobotStatusAndControlEntry(CobotControlEntry, CobotStatusEntry, ABC):
    def __attrs_post_init__(self):
        CobotControlEntry.__attrs_post_init__(self)
        CobotStatusEntry.__attrs_post_init__(self)


@attrs.define(kw_only=True)
class CobotNumericControlEntry(CobotStatusAndControlEntry):
    _wdgt: QtWidgets.QDoubleSpinBox = attrs.field(init=False, factory=QtWidgets.QDoubleSpinBox)
    _blockGUIValueChangedSignal: bool = attrs.field(init=False, default=False)

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        preventAnnoyingScrollBehaviour(self._wdgt)  # prevent scroll wheel from changing value when not focused
        self._wdgt.valueChanged.connect(self._onGUIValueChanged)
        self._onValueChanged()

    @contextmanager
    def _GUIValueChangedSignalBlocked(self):
        alreadyBlocked = self._blockGUIValueChangedSignal
        if not alreadyBlocked:
            self._blockGUIValueChangedSignal = True
        yield
        if not alreadyBlocked:
            self._blockGUIValueChangedSignal = False

    def _onValueChanged(self):
        if self._controller is None:
            return
        newVal = getattr(self._controller.cobotClient, self._key)
        with self._GUIValueChangedSignalBlocked():  # prevent initial rounding from sending value without user input
            self._wdgt.setValue(newVal)

    def _onGUIValueChanged(self, newVal):
        if self._controller is None:
            return
        if self._blockGUIValueChangedSignal:
            return
        self._createTaskAndCatchExceptions(getattr(self._controller.cobotClient, 'set' + self._key[0].upper() + self._key[1:])(newVal))


E = tp.TypeVar('E', bound=IntEnum)


@attrs.define(kw_only=True)
class _CobotEnumMode(CobotStatusAndControlEntry, ABC, tp.Generic[E]):
    _wdgt: QtWidgets.QComboBox = attrs.field(init=False, factory=QtWidgets.QComboBox)
    _Enum: tp.Type[E] = attrs.field(init=False)
    _enumNiceNameMapping: dict[E, str] = attrs.field(init=False, factory=dict)

    def __attrs_post_init__(self):
        super().__attrs_post_init__()

        self._wdgt.setMinimumContentsLength(3)
        self._wdgt.setSizeAdjustPolicy(self._wdgt.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon)

        preventAnnoyingScrollBehaviour(self._wdgt)  # prevent scroll wheel from changing value

        for val in self._Enum:
            dispText = val.name
            if val in self._enumNiceNameMapping:
                dispText = self._enumNiceNameMapping[val]
            self._wdgt.addItem(dispText, userData=val)

        self._wdgt.currentTextChanged.connect(lambda *args: self._onDropdownValueChanged())
        self._onValueChanged()

    def _getValue(self) -> E:
        raise NotImplementedError  # to be implemented by subclasses

    def _setValue(self, newVal: E):
        raise NotImplementedError  # to be implemented by subclasses

    def _onValueChanged(self):
        if self._controller is None:
            return
        newVal: E = self._getValue()
        dispText = newVal.name
        if newVal in self._enumNiceNameMapping:
            dispText = self._enumNiceNameMapping[newVal]
        self._wdgt.setCurrentText(dispText)

    def _onDropdownValueChanged(self):
        if self._controller is None:
            return
        newValName = self._wdgt.currentText()
        reverseMapping = {v: k for k, v in self._enumNiceNameMapping.items()}
        if newValName in reverseMapping:
            newVal = reverseMapping[newValName]
        else:
            newVal = self._Enum[newValName]
        self._setValue(newVal)


@attrs.define(kw_only=True)
class CobotContactModeControlEntry(_CobotEnumMode[ContactMode]):
    _key: str = 'contactMode'
    _label: str | None = 'Contact mode'
    _stateChangedSignal: Signal | str = 'sigContactModeChanged'
    _Enum: tp.Type[ContactMode] = attrs.field(init=False, default=ContactMode)

    def __attrs_post_init__(self):
        self._enumNiceNameMapping = {
            ContactMode.DEFAULT: 'Default',
            ContactMode.CONTACT_THEN_FREEZE: 'Contact then freeze',
            ContactMode.AIRGAPPED_FROM_CONTACT: 'Airgapped from contact',
            ContactMode.AIRGAPPED_FROM_SCALP: 'Airgapped from scalp',
            ContactMode.OFFSET_FROM_TARGET: 'Offset from target'
        }
        super().__attrs_post_init__()

    def _getValue(self) -> ContactMode:
        return self._controller.cobotClient.contactMode

    def _setValue(self, newVal: ContactMode):
        self._createTaskAndCatchExceptions(self._controller.cobotClient.setContactMode(newVal))


@attrs.define(kw_only=True)
class CobotTargetChangeNearRetractMode(_CobotEnumMode[TargetChangeRetractMode]):
    _key: str = 'targetChangeNearRetractMode'
    _label: str | None = 'Target change near retract mode'
    _stateChangedSignal: Signal | str = 'sigNearTargetChangeRetractModeChanged'
    _Enum: tp.Type[TargetChangeRetractMode] = attrs.field(init=False, default=TargetChangeRetractMode)

    def __attrs_post_init__(self):
        self._enumNiceNameMapping = {
            TargetChangeRetractMode.FULLY_RETRACT_THEN_ALIGN: 'Fully retract then align',
            TargetChangeRetractMode.PARTIALLY_RETRACT_AND_ALIGN: 'Partially retract and align',
            TargetChangeRetractMode.LIMITED_RETRACT_THEN_ALIGN: 'Limited retract then align',
            TargetChangeRetractMode.ALIGN_WITHOUT_RETRACT: 'Align without retract',
        }
        super().__attrs_post_init__()

    def _getValue(self) -> TargetChangeRetractMode:
        return self._controller.cobotClient.nearTargetChangeRetractMode

    def _setValue(self, newVal: TargetChangeRetractMode):
        self._createTaskAndCatchExceptions(self._controller.cobotClient.setNearTargetChangeRetractMode(newVal))


@attrs.define(kw_only=True)
class CobotTargetChangeDistantRetractMode(_CobotEnumMode[TargetChangeRetractMode]):
    _key: str = 'targetChangeDistantRetractMode'
    _label: str | None = 'Target change distant retract mode'
    _stateChangedSignal: Signal | str = 'sigDistantTargetChangeRetractModeChanged'
    _Enum: tp.Type[TargetChangeRetractMode] = attrs.field(init=False, default=TargetChangeRetractMode)

    def __attrs_post_init__(self):
        self._enumNiceNameMapping = {
            TargetChangeRetractMode.FULLY_RETRACT_THEN_ALIGN: 'Fully retract then align',
            TargetChangeRetractMode.PARTIALLY_RETRACT_AND_ALIGN: 'Partially retract and align',
            TargetChangeRetractMode.LIMITED_RETRACT_THEN_ALIGN: 'Limited retract then align',
            TargetChangeRetractMode.ALIGN_WITHOUT_RETRACT: 'Align without retract',
        }
        super().__attrs_post_init__()

    def _getValue(self) -> TargetChangeRetractMode:
        return self._controller.cobotClient.distantTargetChangeRetractMode

    def _setValue(self, newVal: TargetChangeRetractMode):
        self._createTaskAndCatchExceptions(self._controller.cobotClient.setDistantTargetChangeRetractMode(newVal))


@attrs.define(kw_only=True)
class CobotTargetChangeNearContactMode(_CobotEnumMode[TargetChangeContactMode]):
    _key: str = 'targetChangeNearContactMode'
    _label: str | None = 'Target change near contact mode'
    _stateChangedSignal: Signal | str = 'sigNearTargetChangeContactModeChanged'
    _Enum: tp.Type[TargetChangeContactMode] = attrs.field(init=False, default=TargetChangeContactMode)

    def __attrs_post_init__(self):
        self._enumNiceNameMapping = {
            TargetChangeContactMode.DO_NOT_RESUME_CONTACT: 'Do not resume contact',
            TargetChangeContactMode.RESUME_IMMEDIATELY: 'Resume immediately',
            TargetChangeContactMode.RESUME_WHEN_IN_TOLERANCE: 'Resume when in tolerance',
            TargetChangeContactMode.RESUME_WHEN_APPROXIMATELY_ALIGNED: 'Resume when approximately aligned',
            TargetChangeContactMode.RESUME_WHEN_ALIGNED: 'Resume when aligned',
            TargetChangeContactMode.INITIATE_IMMEDIATELY: 'Initiate immediately',
            TargetChangeContactMode.INITIATE_WHEN_IN_TOLERANCE: 'Initiate when in tolerance',
            TargetChangeContactMode.INITIATE_WHEN_APPROXIMATELY_ALIGNED: 'Initiate when approximately aligned',
            TargetChangeContactMode.INITIATE_WHEN_ALIGNED: 'Initiate when aligned',
        }
        super().__attrs_post_init__()

    def _getValue(self) -> TargetChangeContactMode:
        return self._controller.cobotClient.nearTargetChangeContactMode

    def _setValue(self, newVal: TargetChangeContactMode):
        self._createTaskAndCatchExceptions(self._controller.cobotClient.setNearTargetChangeContactMode(newVal))


@attrs.define(kw_only=True)
class CobotTargetChangeDistantContactMode(_CobotEnumMode[TargetChangeContactMode]):
    _key: str = 'targetChangeDistantContactMode'
    _label: str | None = 'Target change distant contact mode'
    _stateChangedSignal: Signal | str = 'sigDistantTargetChangeContactModeChanged'
    _Enum: tp.Type[TargetChangeContactMode] = attrs.field(init=False, default=TargetChangeContactMode)

    def __attrs_post_init__(self):
        self._enumNiceNameMapping = {
            TargetChangeContactMode.DO_NOT_RESUME_CONTACT: 'Do not resume contact',
            TargetChangeContactMode.RESUME_IMMEDIATELY: 'Resume immediately',
            TargetChangeContactMode.RESUME_WHEN_IN_TOLERANCE: 'Resume when in tolerance',
            TargetChangeContactMode.RESUME_WHEN_APPROXIMATELY_ALIGNED: 'Resume when approximately aligned',
            TargetChangeContactMode.RESUME_WHEN_ALIGNED: 'Resume when aligned',
            TargetChangeContactMode.INITIATE_IMMEDIATELY: 'Initiate immediately',
            TargetChangeContactMode.INITIATE_WHEN_IN_TOLERANCE: 'Initiate when in tolerance',
            TargetChangeContactMode.INITIATE_WHEN_APPROXIMATELY_ALIGNED: 'Initiate when approximately aligned',
            TargetChangeContactMode.INITIATE_WHEN_ALIGNED: 'Initiate when aligned',
        }
        super().__attrs_post_init__()

    def _getValue(self) -> TargetChangeContactMode:
        return self._controller.cobotClient.distantTargetChangeContactMode

    def _setValue(self, newVal: TargetChangeContactMode):
        self._createTaskAndCatchExceptions(self._controller.cobotClient.setDistantTargetChangeContactMode(newVal))


@attrs.define(kw_only=True)
class CobotAirgapOffsetFromContactControlEntry(CobotNumericControlEntry):
    _key: str = 'airgapOffsetFromContact'
    _label: str | None = 'Airgap contact offset'
    _stateChangedSignal: Signal | str = 'sigAirgapOffsetFromContactChanged'

    def __attrs_post_init__(self):
        super().__attrs_post_init__()

        self._controller.cobotClient.sigContactModeChanged.connect(self._updateEnabled)

        self._wdgt.setRange(0, 100)
        self._wdgt.setSingleStep(0.5)
        self._wdgt.setDecimals(1)
        self._wdgt.setSuffix(' mm')

        self._updateEnabled()

    def _updateEnabled(self):
        enabled = self._controller.cobotClient.contactMode == ContactMode.AIRGAPPED_FROM_CONTACT

        self._wdgt.setEnabled(enabled)


@attrs.define(kw_only=True)
class CobotAirgapOffsetFromScalpControlEntry(CobotNumericControlEntry):
    _key: str = 'airgapOffsetFromScalp'
    _label: str | None = 'Airgap scalp offset'
    _stateChangedSignal: Signal | str = 'sigAirgapOffsetFromScalpChanged'

    def __attrs_post_init__(self):
        super().__attrs_post_init__()

        self._controller.cobotClient.sigContactModeChanged.connect(self._updateEnabled)

        self._wdgt.setRange(0, 100)
        self._wdgt.setSingleStep(0.5)
        self._wdgt.setDecimals(1)
        self._wdgt.setSuffix(' mm')

        self._updateEnabled()

    def _updateEnabled(self):
        enabled = self._controller.cobotClient.contactMode == ContactMode.AIRGAPPED_FROM_SCALP

        self._wdgt.setEnabled(enabled)


@attrs.define(kw_only=True)
class CobotAirgapOffsetFromTargetControlEntry(CobotNumericControlEntry):
    _key: str = 'airgapOffsetFromTarget'
    _label: str | None = 'Target offset'
    _stateChangedSignal: Signal | str = 'sigAirgapOffsetFromTargetChanged'

    def __attrs_post_init__(self):
        super().__attrs_post_init__()

        self._controller.cobotClient.sigContactModeChanged.connect(self._updateEnabled)

        self._wdgt.setRange(-10, 100)
        self._wdgt.setSingleStep(0.5)
        self._wdgt.setDecimals(1)
        self._wdgt.setSuffix(' mm')

        self._updateEnabled()

    def _updateEnabled(self):
        enabled = self._controller.cobotClient.contactMode == ContactMode.OFFSET_FROM_TARGET

        self._wdgt.setEnabled(enabled)


@attrs.define(kw_only=True)
class CobotSetAirgapOffsetFromScalpFromContactOffsetControlEntry(CobotButtonControlEntry):
    _key: str = 'setAirgapOffsetFromScalpFromContactOffset'

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        self._wdgt.setText('Set scalp offset from contact offset')
        self._controller.cobotClient.sigHasCalibratedContactDepthForCurrentTargetChanged.connect(self._updateEnabled)

        self._updateEnabled()

    def _updateEnabled(self):
        enabled = self._controller.cobotClient.hasCalibratedContactDepthForCurrentTarget

        self._wdgt.setEnabled(enabled)

    def _onButtonPressed(self):
        self._createTaskAndCatchExceptions(self._controller.cobotClient.setAirgapOffsetFromScalp_FromContactOffsetDepth())


@attrs.define(kw_only=True)
class CobotSetDistanceThresholdControlEntry(CobotNumericControlEntry):
    def __attrs_post_init__(self):
        super().__attrs_post_init__()

        self._wdgt.setRange(0, 100)
        self._wdgt.setSingleStep(0.2)
        self._wdgt.setDecimals(1)
        self._wdgt.setSuffix(' mm')


@attrs.define(kw_only=True)
class CobotSetAngleThresholdControlEntry(CobotNumericControlEntry):
    def __attrs_post_init__(self):
        super().__attrs_post_init__()

        self._wdgt.setRange(0, 180)
        self._wdgt.setSingleStep(1)
        self._wdgt.setDecimals(1)
        self._wdgt.setSuffix('°')


@attrs.define(kw_only=True)
class CobotResumeAfterProtectiveStopControlEntry(CobotButtonControlEntry):
    _key: str = 'resumeAfterProtectiveStop'

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        self._wdgt.setText('Resume after protective stop')
        self._controller.cobotClient.sigStateChanged.connect(self._updateEnabled)

        self._updateEnabled()

    def _updateEnabled(self):
        enabled = self._controller.cobotClient.cachedState in (TargetingState.PROTECTIVE_STOPPED,)
        self._wdgt.setEnabled(enabled)

    def _onButtonPressed(self):
        self._createTaskAndCatchExceptions(self._controller.cobotClient.resumeAfterProtectiveStop())


@attrs.define(kw_only=True)
class CobotCancelActionSequencesControlEntry(CobotButtonControlEntry):
    _key: str = 'cancelActionSequences'
    _needsUpdate: asyncio.Event = attrs.field(init=False, factory=asyncio.Event)
    _keepUpdatingTask: asyncio.Task = attrs.field(init=False)

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        self._wdgt.setText('Cancel action sequences')
        self._controller.cobotClient.sigActionSequenceStackChanged.connect(self._updateEnabled)

        self._updateEnabled()

        self._keepUpdatingTask = asyncio.create_task(asyncTryAndLogExceptionOnError(self._keepUpdating))

    def _updateEnabled(self):
        self._needsUpdate.set()

    def _onButtonPressed(self):
        self._createTaskAndCatchExceptions(self._controller.cobotClient.cancelActionSequences())

    async def _keepUpdating(self):
        while True:
            await asyncio.sleep(0.05)  # rate limit
            await self._needsUpdate.wait()
            self._needsUpdate.clear()
            if self._controller is None:
                continue
            progressAndLabels = await self._controller.cobotClient.getActionSequenceProgressAndLabels()
            if len(progressAndLabels) > 0:
                self._wdgt.setEnabled(True)
            else:
                self._wdgt.setEnabled(False)


@attrs.define(kw_only=True)
class CobotActionSequencesTreeStatusEntry(CobotStatusEntry):
    _key: str = 'CobotActionSequencesTree'
    _stateChangedSignal: Signal | str = 'sigActionSequenceStackChanged'
    _label: str = 'Action sequences'
    _needsUpdate: asyncio.Event = attrs.field(init=False, factory=asyncio.Event)

    _wdgt: QtWidgets.QTreeWidget = attrs.field(init=False, factory=QtWidgets.QTreeWidget)
    _keepUpdatingTask: asyncio.Task = attrs.field(init=False)

    def __attrs_post_init__(self):
        super().__attrs_post_init__()

        self._wdgt.setHeaderHidden(True)
        self._wdgt.setIndentation(5)
        self._wdgt.setColumnCount(1)
        self._wdgt.setSelectionMode(self._wdgt.SelectionMode.NoSelection)
        self._wdgt.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self._onValueChanged()
        self._keepUpdatingTask = asyncio.create_task(asyncTryAndLogExceptionOnError(self._keepUpdating))

    def _onValueChanged(self):
        logger.debug('CobotActionSequencesTreeStatusEntry _onValueChanged')
        self._needsUpdate.set()

    def _createTreeWidgetItems(self, progressAndLabels: tuple[tuple[int | None, int, tuple[str,...]]],
                               parent: QtWidgets.QTreeWidgetItem | QtWidgets.QTreeWidget) -> QtWidgets.QTreeWidgetItem | None:
        logger.debug('CobotActionSequencesTreeStatusEntry _createTreeWidgetItems')
        if len(progressAndLabels) == 0:
            return None
        bottomOfStack = progressAndLabels[0]
        currentActionIndex, totalNumActions, labels = bottomOfStack
        root = QtWidgets.QTreeWidgetItem(parent)
        root.setText(0, f'{labels[0]} {currentActionIndex}/{totalNumActions}')
        root.setIcon(0, qta.icon('mdi6.menu-down-outline', color='black' if len(progressAndLabels)==1 else 'gray'))
        for iLabel, label in enumerate(labels[1:]):
            child = QtWidgets.QTreeWidgetItem(root)
            child.setText(0, label)
            # TODO: add aesthetics like arrows for active actions, highlight currently running action
            if currentActionIndex is not None and currentActionIndex == iLabel:
                grandchildren = self._createTreeWidgetItems(progressAndLabels[1:], child)
                if grandchildren is None:
                    child.setIcon(0, qta.icon('mdi6.circle-medium', color='blue'))
                    child.setSelected(True)
                else:
                    pass
                    child.setIcon(0, qta.icon('mdi6.menu-down', color='black'))
            else:
                child.setIcon(0, qta.icon('mdi6.menu-right', color='gray'))
        return root

    async def _keepUpdating(self):
        while True:
            await asyncio.sleep(0.05)  # rate limit
            await self._needsUpdate.wait()
            self._needsUpdate.clear()
            if self._controller is None:
                continue
            logger.debug('CobotActionSequencesTreeStatusEntry getActionSequenceProgressAndLabels')
            progressAndLabels = await self._controller.cobotClient.getActionSequenceProgressAndLabels()

            logger.debug(f'CobotActionSequencesTreeStatusEntry updating {progressAndLabels}')
            self._wdgt.clear()
            self._createTreeWidgetItems(progressAndLabels, self._wdgt)
            self._wdgt.expandAll()
            logger.debug(f'CobotActionSequencesTreeStatusEntry updated {progressAndLabels}')


@attrs.define(kw_only=True)
class CobotJointPositionStatusEntry(CobotStatusEntry):
    _index: int
    _deviceName: str
    _stateChangedSignal: Signal | str = 'sigJointPositionsChanged'
    _wdgt: QtWidgets.QWidget = attrs.field(init=False)
    _resolution: int = 1000

    _slider: QtWidgets.QSlider = attrs.field(init=False)
    _minLabel: QtWidgets.QLabel = attrs.field(init=False)
    _maxLabel: QtWidgets.QLabel = attrs.field(init=False)
    _valueLabel: QtWidgets.QLabel = attrs.field(init=False)

    def __attrs_post_init__(self):

        super().__attrs_post_init__()

        self._wdgt = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self._wdgt.setLayout(layout)

        self._slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self._slider.setDisabled(True)
        layout.addWidget(self._slider, 0, 0, 1, 3)

        self._minLabel = QtWidgets.QLabel()
        self._minLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self._minLabel, 1, 0)

        self._valueLabel = QtWidgets.QLabel()
        self._valueLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self._valueLabel, 1, 1)

        self._maxLabel = QtWidgets.QLabel()
        self._maxLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self._maxLabel, 1, 2)

    def _onValueChanged(self):
        jointPositions = self._controller.cobotClient.latestJointPositions
        jointPositionLimits = self._controller.cobotClient.latestJointPositionLimits

        hasPos = self._deviceName in jointPositions

        posKey = self._deviceName + '_' + 'JPOSLIM'
        negKey = self._deviceName + '_' + 'JNEGLIM'
        hasLim = posKey in jointPositionLimits and negKey in jointPositionLimits

        if not hasPos:
            self._valueLabel.setText('?')

        if not hasLim:
            self._minLabel.setText('?')
            self._maxLabel.setText('?')

        if not hasPos or not hasLim:
            # TODO: hide handle on slider
            return

        pos = jointPositions[self._deviceName][self._index]

        posLim = jointPositionLimits[posKey][self._index]
        negLim = jointPositionLimits[negKey][self._index]

        self._minLabel.setText(f'{negLim:.0f}')
        self._maxLabel.setText(f'{posLim:.0f}')
        self._valueLabel.setText(f'{pos:.0f}')

        self._slider.setMinimum(0)
        self._slider.setMaximum(self._resolution)
        self._slider.setValue((pos - negLim) / (posLim - negLim) * self._resolution)


@attrs.define(kw_only=True)
class CobotSensitivityEntry(CobotStatusAndControlEntry):
    _key: str = 'sensitivity'
    _stateChangedSignal: Signal | str = 'sigSensitivityChanged'
    _wdgt: QtWidgets.QWidget = attrs.field(init=False)
    _stepSize: float = 0.1
    _minSensitivity: float = 0.3
    _maxSensitivity: float = 3.0

    _slider: QtWidgets.QSlider = attrs.field(init=False)
    _minLabel: QtWidgets.QLabel = attrs.field(init=False)
    _maxLabel: QtWidgets.QLabel = attrs.field(init=False)
    _valueLabel: QtWidgets.QLabel = attrs.field(init=False)

    _hasTriedToGetInitialValue: bool = attrs.field(init=False, default=False)

    def __attrs_post_init__(self):

        super().__attrs_post_init__()

        self._wdgt = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self._wdgt.setLayout(layout)

        self._slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self._slider.setMinimum(int(ceil(self._minSensitivity / self._stepSize)))
        self._slider.setMaximum(int(floor(self._maxSensitivity / self._stepSize)))
        self._slider.sliderReleased.connect(self._onSliderChanged)  # use sliderReleased to avoid getting triggered by changes coming from cobot
        layout.addWidget(self._slider, 0, 0, 1, 3)

        self._minLabel = QtWidgets.QLabel()
        self._minLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)
        self._minLabel.setText(f'{self._minSensitivity}')
        layout.addWidget(self._minLabel, 1, 0)

        self._valueLabel = QtWidgets.QLabel()
        self._valueLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self._valueLabel, 1, 1)

        self._maxLabel = QtWidgets.QLabel()
        self._maxLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTop)
        self._maxLabel.setText(f'{self._maxSensitivity}')
        layout.addWidget(self._maxLabel, 1, 2)

    async def _getInitialValue(self):
        await self._controller.cobotClient.connectedToServerEvent.wait()
        connectedEvt = asyncio.Event()
        self._controller.cobotClient.sigConnectedChanged.connect(connectedEvt.set)
        while True:
            await connectedEvt.wait()
            connectedEvt.clear()
            if self._controller.cobotClient.isConnected:
                break

        await self._controller.cobotClient.getSensitivity()
        self._onValueChanged()

    def _onValueChanged(self):
        val = self._controller.cobotClient.sensitivity

        if val is None and not self._hasTriedToGetInitialValue:
            asyncio.create_task(asyncTryAndLogExceptionOnError(self._getInitialValue))
            self._hasTriedToGetInitialValue = True

        if val is None:
            self._valueLabel.setText('?')

        if val is None:
            # TODO: hide handle on slider
            return

        self._valueLabel.setText(f'{val:.1f}')

        self._slider.setValue(round(val / self._stepSize))

    def _onSliderChanged(self):
        newVal = self._slider.value() * self._stepSize
        self._createTaskAndCatchExceptions(
            self._controller.cobotClient.setSensitivity(newVal))

