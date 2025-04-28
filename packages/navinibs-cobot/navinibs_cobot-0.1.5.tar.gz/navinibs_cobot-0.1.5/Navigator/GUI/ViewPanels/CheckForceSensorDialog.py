import asyncio
import attrs
from datetime import datetime
import logging
import qtawesome as qta
from qtpy import QtWidgets, QtGui, QtCore

from NaviNIBS.util.Signaler import Signal
from NaviNIBS.util.Asyncio import asyncTryAndLogExceptionOnError
from NaviNIBS_Cobot.Devices.CobotTargetingController import CobotTargetingController
from NaviNIBS_Cobot.Navigator.GUI.ViewPanels.CobotWidgets import CobotForceStatusEntry

logger = logging.getLogger(__name__)


@attrs.define
class CobotCheckForceStatusEntry(CobotForceStatusEntry):
    _checkState: int = 0

    _icons: dict[tuple[int, int | None, int], QtGui.QIcon] = attrs.field(init=False, factory=dict)

    sigFinishedCheck: Signal[()] = attrs.field(init=False, factory=Signal)

    def __attrs_post_init__(self):
        super().__attrs_post_init__()

    @property
    def checkState(self):
        return self._checkState

    @checkState.setter
    def checkState(self, newState: int):
        if self._checkState == newState:
            return

        self._checkState = newState
        if self._checkState == 2 * self._numForceLevels - 1:
            self.sigFinishedCheck.emit()
        self._onValueChanged()

    def _onValueChanged(self):
        if self._controller is not None:
            force = self._controller.cobotClient.lastMeasuredForce
            if force is not None:
                if (self.checkState < self._numForceLevels and int(force) == self.checkState) or \
                        (self.checkState >= self._numForceLevels and int(force) == 2 * (self._numForceLevels - 1) - self.checkState):
                    logger.info(f'Force sensor check: advancing to state {self.checkState + 1}')
                    self.checkState += 1

        else:
            force = None

        for level, levelWdgt in enumerate(self._levelWdgts):
            levelWdgt.icon = self._getIcon(level=level,
                                           state=int(force) if force is not None else None)

    def _getIcon(self, level: int, state: int | None) -> QtGui.QIcon:
        key = (level, state, self._checkState)
        if key not in self._icons:
            if state is None:
                iconColor = 'gray'
                iconName = 'mdi6.help-box'
            else:
                if level <= state:
                    iconColor = ['gray', 'green', 'goldenrod', 'orange', 'red'][state]
                else:
                    iconColor = 'gray'

                if self._checkState < self._numForceLevels:
                    if level < state:
                        if level < self._checkState:
                            iconName = f'mdi6.checkbox-blank'
                        elif level == self._checkState:
                            iconName = f'mdi6.circle-box'
                        else:  # level > self._checkState
                            iconName = f'mdi6.arrow-left-bold-box'
                    elif level == state:
                        if level < self._checkState:
                            iconName = f'mdi6.arrow-right-bold-box'
                        elif level == self._checkState:
                            iconName = f'mdi6.circle-box'
                        else:  # level > self._checkState
                            iconName = f'mdi6.arrow-left-bold-box'
                    else:  # level > state
                        if level < self._checkState:
                            iconName = f'mdi6.arrow-right-bold-box-outline'
                        elif level == self._checkState:
                            iconName = f'mdi6.circle-box-outline'
                        else:  # level > self._checkState
                            iconName = f'mdi6.checkbox-blank-outline'

                elif self._checkState == 2 * self._numForceLevels - 1:
                    # done with check
                    if level <= state:
                        if level == state:
                            iconName = f'mdi6.numeric-{level}-box'
                        else:
                            iconName = f'mdi6.checkbox-blank'
                    else:
                        iconName = f'mdi6.checkbox-blank-outline'

                else:  # self._checkState >= self._numForceLevels
                    if level < state:
                        if level < 2 * (self._numForceLevels - 1) - self._checkState:
                            iconName = f'mdi6.checkbox-blank'
                        elif level == 2 * (self._numForceLevels - 1) - self._checkState:
                            iconName = f'mdi6.circle-box'
                        else:  # level > 2 * (self._numForceLevels - 1) - self._checkState
                            iconName = f'mdi6.arrow-left-bold-box'
                    elif level == state:
                        if level < 2 * (self._numForceLevels - 1) - self._checkState:
                            iconName = f'mdi6.arrow-right-bold-box'
                        elif level == 2 * (self._numForceLevels - 1) - self._checkState:
                            iconName = f'mdi6.circle-box'
                        else:  # level > 2 * (self._numForceLevels - 1) - self._checkState
                            iconName = f'mdi6.arrow-left-bold-box'
                    else:  # level > state
                        if level < 2 * (self._numForceLevels - 1) - self._checkState:
                            iconName = f'mdi6.arrow-right-bold-box-outline'
                        elif level == 2 * (self._numForceLevels - 1) - self._checkState:
                            iconName = f'mdi6.circle-box-outline'
                        else:  # level > 2 * (self._numForceLevels - 1) - self._checkState
                            iconName = f'mdi6.checkbox-blank-outline'

            self._icons[key] = qta.icon(iconName, color=iconColor)

        return self._icons[key]


@attrs.define
class CheckForceSensorDialog:
    _parent: QtWidgets.QWidget
    _controller: CobotTargetingController

    _wdgt: QtWidgets.QDialog = attrs.field(init=False)
    _readForceStatusEntry: CobotCheckForceStatusEntry = attrs.field(init=False)
    _simulateCheckBtn: QtWidgets.QPushButton | None = attrs.field(init=False, default=None)
    _btnBox: QtWidgets.QDialogButtonBox = attrs.field(init=False)

    dialogFinishedEvent: asyncio.Event = attrs.field(init=False, factory=asyncio.Event)

    def __attrs_post_init__(self):
        self._wdgt = QtWidgets.QDialog(self._parent)
        self._wdgt.setModal(True)
        self._wdgt.setWindowTitle('Check Cobot force sensor')
        self._wdgt.setWindowModality(QtGui.Qt.WindowModal)
        self._wdgt.finished.connect(self._onDlgFinished)

        self._wdgt.setLayout(QtWidgets.QVBoxLayout())

        formWdgt = QtWidgets.QWidget()
        formWdgt.setLayout(QtWidgets.QFormLayout())
        self._wdgt.layout().addWidget(formWdgt)

        self._readForceStatusEntry = CobotCheckForceStatusEntry(
            controller=self._controller
        )
        self._readForceStatusEntry.sigFinishedCheck.connect(self._onCheckFinished)
        formWdgt.layout().addRow('Current force:', self._readForceStatusEntry.wdgt)
        if self._controller.cobotClient.isSimulated:
            self._simulateCheckBtn = QtWidgets.QPushButton('Simulate check')
            self._simulateCheckBtn.clicked.connect(self._onSimulateCheckBtnClicked)
            formWdgt.layout().addRow('', self._simulateCheckBtn)

        self._btnBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self._btnBox.accepted.connect(self._wdgt.accept)
        self._btnBox.rejected.connect(self._wdgt.reject)
        self._btnBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)  # don't enable until check complete
        self._wdgt.layout().addWidget(self._btnBox)

    def _onSimulateCheckBtnClicked(self):
        asyncio.create_task(asyncTryAndLogExceptionOnError(self._simulateCheck))

    async def _simulateCheck(self):
        assert self._controller.cobotClient.isSimulated

        for i in range(self._readForceStatusEntry.numForceLevels):
            await self._controller.cobotClient.setSimulatedForceValue(i)
            await asyncio.sleep(1.)

        for i in range(self._readForceStatusEntry.numForceLevels - 1, -1, -1):
            await self._controller.cobotClient.setSimulatedForceValue(i)
            await asyncio.sleep(1.)

    def _onCheckFinished(self):
        self._btnBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)

    def _onDlgFinished(self, result: int):
        succeeded = result == QtWidgets.QDialog.Accepted
        if succeeded:
            self._controller.configuration.forceLastCheckedAtTime = datetime.today().strftime('%y%m%d%H%M%S.%f')

        self.dialogFinishedEvent.set()

    def show(self):
        self._wdgt.show()

    @property
    def wdgt(self):
        return self._wdgt





