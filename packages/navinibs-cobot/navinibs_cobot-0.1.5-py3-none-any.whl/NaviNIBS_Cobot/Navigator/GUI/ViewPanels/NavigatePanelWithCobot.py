import asyncio
import attrs
import logging
import qtawesome as qta
from qtpy import QtWidgets, QtGui, QtCore
import typing as tp

from NaviNIBS_Cobot.Devices.CobotTargetingController import CobotTargetingController
from NaviNIBS_Cobot.Devices.CobotConnector import ContactMode
from NaviNIBS_Cobot.Navigator.Model.CobotConfiguration import CobotControl
from NaviNIBS_Cobot.Navigator.GUI.ViewPanels import CobotWidgets as cw
from NaviNIBS_Cobot.Navigator.GUI.ViewPanels.CobotViewLayers import CobotWorkspaceAlignedView
from NaviNIBS_Cobot.Navigator.GUI.ViewPanels.CheckForceSensorDialog import CheckForceSensorDialog

from NaviNIBS.Navigator.GUI.ViewPanels import MainViewPanel
from NaviNIBS.util.GUI.QScrollContainer import QScrollContainer
from NaviNIBS.util.GUI.QCollapsibleSection import QCollapsibleSection
from NaviNIBS.util.GUI.QFlowLayout import QFlowLayout
from NaviNIBS.util.GUI.ErrorDialog import asyncTryAndRaiseDialogOnError
from NaviNIBS.Navigator.GUI.ViewPanels.NavigatePanel import NavigatePanel

logger = logging.getLogger(__name__)


@attrs.define
class BasicControlsWidget:
    _controller: CobotTargetingController
    _wdgt: QtWidgets.QWidget = attrs.field(factory=lambda: QtWidgets.QGroupBox('Basic controls'))

    _entries: dict[str, cw.CobotControlEntry | cw.CobotStatusEntry] = attrs.field(init=False, factory=dict)

    def __attrs_post_init__(self):

        outerLayout = QtWidgets.QVBoxLayout()
        self._wdgt.setLayout(outerLayout)

        innerLayout = QFlowLayout()
        innerLayout.setContentsMargins(0, 0, 0, 0)
        wdgt = QtWidgets.QWidget()
        wdgt.setLayout(innerLayout)
        outerLayout.addWidget(wdgt)

        self._entries['moveToPark'] = cw.CobotMoveToParkControlEntry(
            controller=self._controller
        )
        innerLayout.addWidget(self._entries['moveToPark'].wdgt)

        self._entries['moveToWelcome'] = cw.CobotMoveToWelcomeControlEntry(
            key='moveToWelcome1',
            controller=self._controller,
            positionIndex=1
        )
        innerLayout.addWidget(self._entries['moveToWelcome'].wdgt)

        self._entries['freedrive'] = cw.CobotFreedriveControlEntry(
            controller=self._controller
        )
        innerLayout.addWidget(self._entries['freedrive'].wdgt)

        self._entries['resumeAfterProtectiveStop'] = cw.CobotResumeAfterProtectiveStopControlEntry(
            controller=self._controller
        )
        innerLayout.addWidget(self._entries['resumeAfterProtectiveStop'].wdgt)

        self._entries['estop'] = cw.CobotEStopControlEntry(
            controller=self._controller
        )
        innerLayout.addWidget(self._entries['estop'].wdgt)

        self._entries['connectAndInitialize'] = cw.CobotConnectAndInitializeControlEntry(
            controller=self._controller
        )
        innerLayout.addWidget(self._entries['connectAndInitialize'].wdgt)

        if False:
            self._entries['stop'] = cw.CobotStopControlEntry(
                controller=self._controller
            )
            innerLayout.addWidget(self._entries['stop'].wdgt)


        innerLayout = QtWidgets.QFormLayout()
        innerLayout.setContentsMargins(0, 0, 0, 0)
        formWdgt = QtWidgets.QWidget()
        formWdgt.setLayout(innerLayout)
        outerLayout.addWidget(formWdgt)

        self._entries['inWorkspace'] = cw.CobotInWorkspaceStatusEntry(
            controller=self._controller
        )
        innerLayout.addRow('In workspace:', self._entries['inWorkspace'].wdgt)

        if True:  # TODO: debug, set to False / remove
            self._entries['state'] = cw.CobotStateStatusEntry(
                controller=self._controller
            )
            innerLayout.addRow('State:', self._entries['state'].wdgt)

    @property
    def wdgt(self):
        return self._wdgt


@attrs.define
class TrackingControlsWidget:
    _controller: CobotTargetingController
    _wdgt: QtWidgets.QWidget = attrs.field(factory=lambda: QtWidgets.QGroupBox('Tracking'))
    _alignDistsSection: QCollapsibleSection = attrs.field(init=False)

    _entries: dict[str, cw.CobotControlEntry | cw.CobotStatusEntry] = attrs.field(init=False, factory=dict)

    def __attrs_post_init__(self):
        outerLayout = QtWidgets.QVBoxLayout()
        outerLayout.setContentsMargins(0, 0, 0, 0)
        self._wdgt.setLayout(outerLayout)

        innerLayout = QtWidgets.QFormLayout()
        innerLayout.setContentsMargins(0, 0, 0, 0)
        formWdgt = QtWidgets.QWidget()
        formWdgt.setLayout(innerLayout)
        outerLayout.addWidget(formWdgt)

        self._entries['target'] = cw.CobotTargetLabelStatusEntry(
            controller=self._controller
        )
        innerLayout.addRow('Current cobot target:', self._entries['target'].wdgt)

        self._entries['targetIsAccessible'] = cw.CobotBoolStatusEntry(
            controller=self._controller,
            key='targetIsAccessible',
            stateChangedSignal='sigTargetAccessibleChanged')
        innerLayout.addRow('Target accessible?', self._entries['targetIsAccessible'].wdgt)

        self._entries['setTarget'] = cw.CobotSetTargetOrAutosetControlEntry(
            controller=self._controller)
        if False:
            innerLayout.addRow('', self._entries['setTarget'].wdgt)
        else:
            innerLayout.addRow(self._entries['setTarget'].autosetCheckbox, self._entries['setTarget'].setTargetButton)

        self._entries['track'] = cw.CobotTrackTargetControlEntry(
            controller=self._controller)
        innerLayout.addRow('', self._entries['track'].wdgt)

        self._alignDistsSection = QCollapsibleSection(title='Alignment distance thresholds',
                                                      doStartCollapsed=True)
        outerLayout.addWidget(self._alignDistsSection.outerWdgt)

        innerLayout = QtWidgets.QFormLayout()

        innerLayout.addRow(QtWidgets.QLabel('Aligned when error within:'))

        self._entries['alignedWhenDistErrorUnder'] = cw.CobotSetDistanceThresholdControlEntry(
            controller=self._controller,
            key='alignedWhenDistErrorUnder',
            stateChangedSignal='sigAlignedThresholdsChanged',
        )
        innerLayout.addRow('Horiz distance', self._entries['alignedWhenDistErrorUnder'].wdgt)

        self._entries['alignedWhenZAngleErrorUnder'] = cw.CobotSetAngleThresholdControlEntry(
            controller=self._controller,
            key='alignedWhenZAngleErrorUnder',
            stateChangedSignal='sigAlignedThresholdsChanged',
        )

        innerLayout.addRow('Depth angle', self._entries['alignedWhenZAngleErrorUnder'].wdgt)

        self._entries['alignedWhenHorizAngleErrorUnder'] = cw.CobotSetAngleThresholdControlEntry(
            controller=self._controller,
            key='alignedWhenHorizAngleErrorUnder',
            stateChangedSignal='sigAlignedThresholdsChanged',
        )
        innerLayout.addRow('Horiz angle', self._entries['alignedWhenHorizAngleErrorUnder'].wdgt)

        self._entries['doneMovingWhenZDistErrorUnder'] = cw.CobotSetDistanceThresholdControlEntry(
            controller=self._controller,
            key='doneMovingWhenZDistErrorUnder',
            stateChangedSignal='sigAlignedThresholdsChanged',
        )
        innerLayout.addRow('Depth (move only)', self._entries['doneMovingWhenZDistErrorUnder'].wdgt)

        innerLayout.addRow(QtWidgets.QWidget())  # spacer

        innerLayout.addRow(QtWidgets.QLabel('Realign when error exceeds:'))
        self._entries['realignWhenDistErrorExceeds'] = cw.CobotSetDistanceThresholdControlEntry(
            controller=self._controller,
            key='realignWhenDistErrorExceeds',
            stateChangedSignal='sigRealignThresholdsChanged',
        )
        innerLayout.addRow('Horiz distance', self._entries['realignWhenDistErrorExceeds'].wdgt)

        self._entries['realignWhenZAngleErrorExceeds'] = cw.CobotSetAngleThresholdControlEntry(
            controller=self._controller,
            key='realignWhenZAngleErrorExceeds',
            stateChangedSignal='sigRealignThresholdsChanged',
        )
        innerLayout.addRow('Depth angle', self._entries['realignWhenZAngleErrorExceeds'].wdgt)

        self._entries['realignWhenHorizAngleErrorExceeds'] = cw.CobotSetAngleThresholdControlEntry(
            controller=self._controller,
            key='realignWhenHorizAngleErrorExceeds',
            stateChangedSignal='sigRealignThresholdsChanged',
        )
        innerLayout.addRow('Horiz angle', self._entries['realignWhenHorizAngleErrorExceeds'].wdgt)

        self._entries['moveWhenZDistErrorExceeds'] = cw.CobotSetDistanceThresholdControlEntry(
            controller=self._controller,
            key='moveWhenZDistErrorExceeds',
            stateChangedSignal='sigRealignThresholdsChanged',
        )
        innerLayout.addRow('Depth (move only)', self._entries['moveWhenZDistErrorExceeds'].wdgt)

        self._alignDistsSection.setLayout(innerLayout)

    @property
    def wdgt(self):
        return self._wdgt


@attrs.define
class ContactControlsWidget:
    _controller: CobotTargetingController
    _wdgt: QtWidgets.QWidget = attrs.field(factory=lambda: QtWidgets.QGroupBox('Contact'))

    _entries: dict[str, cw.CobotControlEntry | cw.CobotStatusEntry] = attrs.field(init=False, factory=dict)
    _checkForceDlg: CheckForceSensorDialog | None = attrs.field(init=False, default=None)

    def __attrs_post_init__(self):
        outerLayout = QtWidgets.QVBoxLayout()
        outerLayout.setContentsMargins(0, 0, 0, 0)
        self._wdgt.setLayout(outerLayout)

        _container = QtWidgets.QWidget()
        formLayout = QtWidgets.QFormLayout()
        formLayout.setContentsMargins(0, 0, 0, 0)
        _container.setLayout(formLayout)
        outerLayout.addWidget(_container)

        self._entries['currentForce'] = cw.CobotForceStatusEntry(
            controller=self._controller)
        formLayout.addRow('Current force:', self._entries['currentForce'].wdgt)

        self._entries['contact'] = cw.CobotContactControlEntry(
            controller=self._controller)
        formLayout.addRow('Contact:', self._entries['contact'].wdgt)

        self._entries['contactMode'] = cw.CobotContactModeControlEntry(
            controller=self._controller)
        formLayout.addRow('Contact mode:', self._entries['contactMode'].wdgt)

        self._entries['airgapOffsetFromContact'] = cw.CobotAirgapOffsetFromContactControlEntry(
            controller=self._controller
        )
        formLayout.addRow('Airgap contact offset:', self._entries['airgapOffsetFromContact'].wdgt)

        self._entries['airgapOffsetFromScalp'] = cw.CobotAirgapOffsetFromScalpControlEntry(
            controller=self._controller
        )
        formLayout.addRow('Airgap scalp offset:', self._entries['airgapOffsetFromScalp'].wdgt)

        self._entries['convertContactToScalpOffset'] = cw.CobotSetAirgapOffsetFromScalpFromContactOffsetControlEntry(
            controller=self._controller
        )
        formLayout.addRow(self._entries['convertContactToScalpOffset'].wdgt)

        self._entries['airgapOffsetFromTarget'] = cw.CobotAirgapOffsetFromTargetControlEntry(
            controller=self._controller
        )
        formLayout.addRow('Target offset', self._entries['airgapOffsetFromTarget'].wdgt)

        self._controller.cobotClient.sigContactModeChanged.connect(self._onContactModeChanged)
        self._onContactModeChanged()

        if False:
            # do force check (if needed) when GUI first initializes
            if self._controller.needsForceCheck:
                self._startForceCheck()
        else:
            # don't do force check here (presumably delay until first "start contact"
            pass

    def _startForceCheck(self):
        self._checkForceDlg = CheckForceSensorDialog(parent=self._wdgt, controller=self._controller)
        self._checkForceDlg.show()

    def _onContactModeChanged(self):
        # only show airgap distance widget when contact mode is airgapped
        airgapWdgts = [self._entries['airgapOffsetFromContact'].wdgt,
                       self._entries['airgapOffsetFromScalp'].wdgt,
                       self._entries['convertContactToScalpOffset'].wdgt]
        targetOffsetWdgts = [
                       self._entries['airgapOffsetFromTarget'].wdgt]
        formLayout = airgapWdgts[0].parentWidget().layout()
        assert isinstance(formLayout, QtWidgets.QFormLayout)
        if True:
            # only supported in Qt >= 6.4
            for airgapWdgt in airgapWdgts:
                formLayout.setRowVisible(airgapWdgt, self._controller.cobotClient.contactMode in  (ContactMode.AIRGAPPED_FROM_CONTACT, ContactMode.AIRGAPPED_FROM_SCALP))
            for wdgt in targetOffsetWdgts:
                formLayout.setRowVisible(wdgt, self._controller.cobotClient.contactMode == ContactMode.OFFSET_FROM_TARGET)
        else:
            # for Qt < 6.4
            pass  # don't hide field

    @property
    def wdgt(self):
        return self._wdgt


@attrs.define
class ActionSequencesControlsWidget:
    _controller: CobotTargetingController
    _wdgt: QtWidgets.QWidget = attrs.field(factory=lambda: QtWidgets.QGroupBox('Action sequences'))

    _entries: dict[str, cw.CobotControlEntry | cw.CobotStatusEntry] = attrs.field(init=False, factory=dict)

    def __attrs_post_init__(self):
        outerLayout = QtWidgets.QVBoxLayout()
        outerLayout.setContentsMargins(0, 0, 0, 0)
        self._wdgt.setLayout(outerLayout)

        self._entries['cancelActionSequences'] = cw.CobotCancelActionSequencesControlEntry(
            controller=self._controller
        )

        self._entries['actionSequences'] = cw.CobotActionSequencesTreeStatusEntry(
            controller=self._controller
        )

        if True:
            outerLayout.addWidget(self._entries['cancelActionSequences'].wdgt)
            wdgt = QtWidgets.QWidget()
            wdgt.setLayout(QtWidgets.QVBoxLayout())
            wdgt.layout().setContentsMargins(0, 0, 0, 0)
            wdgt.layout().addWidget(self._entries['actionSequences'].wdgt)

            collapsibleSection = QCollapsibleSection('Pending action sequences',
                                                     innerWdgt=wdgt)
            self._entries['actionSequences_collapsibleSection'] = collapsibleSection
            outerLayout.addWidget(collapsibleSection.outerWdgt)
        else:
            outerLayout.addWidget(self._entries['cancelActionSequences'].wdgt)
            outerLayout.addWidget(self._entries['actionSequences'].wdgt)

    @property
    def wdgt(self):
        return self._wdgt


@attrs.define
class ChangingTargetsControlsWidget:
    _controller: CobotTargetingController
    _wdgt: QtWidgets.QWidget = attrs.field(factory=lambda: QtWidgets.QGroupBox('When changing targets'))

    _entries: dict[str, cw.CobotControlEntry | cw.CobotStatusEntry] = attrs.field(init=False, factory=dict)

    def __attrs_post_init__(self):

        outerLayout = QtWidgets.QVBoxLayout()
        self._wdgt.setLayout(outerLayout)

        # TODO: add widgets to set distance/angle thresholds for near vs far targets

        container = QtWidgets.QGroupBox('Nearby target change')
        outerLayout.addWidget(container)
        formLayout = QtWidgets.QFormLayout()
        formLayout.setContentsMargins(0, 0, 0, 0)
        container.setLayout(formLayout)

        self._entries['nearChangeRetractMode'] = cw.CobotTargetChangeNearRetractMode(
            controller=self._controller)
        formLayout.addRow('Retract mode:', self._entries['nearChangeRetractMode'].wdgt)

        self._entries['nearChangeContactMode'] = cw.CobotTargetChangeNearContactMode(
            controller=self._controller)
        formLayout.addRow('Contact mode:', self._entries['nearChangeContactMode'].wdgt)

        container = QtWidgets.QGroupBox('Distant target change')
        outerLayout.addWidget(container)
        formLayout = QtWidgets.QFormLayout()
        formLayout.setContentsMargins(0, 0, 0, 0)
        container.setLayout(formLayout)

        self._entries['distantChangeRetractMode'] = cw.CobotTargetChangeDistantRetractMode(
            controller=self._controller)
        formLayout.addRow('Retract mode:', self._entries['distantChangeRetractMode'].wdgt)

        self._entries['distantChangeContactMode'] = cw.CobotTargetChangeDistantContactMode(
            controller=self._controller)
        formLayout.addRow('Contact mode:', self._entries['distantChangeContactMode'].wdgt)

    @property
    def wdgt(self):
        return self._wdgt


@attrs.define
class CobotTargetingWidget:
    _controller: CobotTargetingController
    _scroll: QScrollContainer = attrs.field(init=False)

    _basicControlsWdgt: BasicControlsWidget = attrs.field(init=False)
    _trackingControlsWdgt: TrackingControlsWidget = attrs.field(init=False)
    _contactControlsWdgt: ContactControlsWidget = attrs.field(init=False)
    _actionSequencesControlsWdgt: ActionSequencesControlsWidget = attrs.field(init=False)
    _targetChangeControlsWdgt: ChangingTargetsControlsWidget = attrs.field(init=False)

    _sendTargetBtn: QtWidgets.QPushButton = attrs.field(init=False)

    def __attrs_post_init__(self):

        self._scroll = QScrollContainer()
        self._scroll.innerContainerLayout.setContentsMargins(0, 0, 0, 0)
        self._scroll.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)

        self._basicControlsWdgt = BasicControlsWidget(
            controller=self._controller
        )
        self._scroll.innerContainerLayout.addWidget(self._basicControlsWdgt.wdgt)

        self._trackingControlsWdgt = TrackingControlsWidget(
            controller=self._controller
        )
        self._scroll.innerContainerLayout.addWidget(self._trackingControlsWdgt.wdgt)

        self._contactControlsWdgt = ContactControlsWidget(
            controller=self._controller
        )
        self._scroll.innerContainerLayout.addWidget(self._contactControlsWdgt.wdgt)

        self._actionSequencesControlsWdgt = ActionSequencesControlsWidget(
            controller=self._controller
        )
        self._scroll.innerContainerLayout.addWidget(self._actionSequencesControlsWdgt.wdgt)

        self._targetChangeControlsWdgt = ChangingTargetsControlsWidget(
            controller=self._controller
        )
        self._scroll.innerContainerLayout.addWidget(self._targetChangeControlsWdgt.wdgt)

        self._scroll.innerContainerLayout.addStretch()

    @property
    def wdgt(self):
        return self._scroll.scrollArea


@attrs.define
class NavigatePanelWithCobot(NavigatePanel):

    _key: str = 'NavigatePanelWithCobot'
    _label: str = 'Cobot navigate'

    _controller: CobotTargetingController | None = attrs.field(init=False, default=None)
    _cobotControlWdgt: CobotTargetingWidget | None = attrs.field(init=False, default=None, repr=False)
    _doWaitForPanelActivationToInitController: bool = False
    _hasStartedInitializingController: bool = attrs.field(init=False, default=False)
    _controllerInitialized: asyncio.Event = attrs.field(init=False, factory=asyncio.Event)
    finishedAsyncInitialization: asyncio.Event = attrs.field(init=False, factory=asyncio.Event)

    def __attrs_post_init__(self):
        super().__attrs_post_init__()

    def _onSessionSet(self):
        super()._onSessionSet()
        if self._controller is None and \
                not self._doWaitForPanelActivationToInitController and \
                not self._hasStartedInitializingController:
            self._hasStartedInitializingController = True
            asyncio.create_task(asyncTryAndRaiseDialogOnError(self._initializeController))

    def _onPanelInitializedAndSessionSet(self):
        super()._onPanelInitializedAndSessionSet()

        asyncio.create_task(asyncTryAndRaiseDialogOnError(self._onPanelInitializedAndSessionSet_async))

    async def _initializeController(self):
        assert self._controller is None

        config = self.session.addons['NaviNIBS_Cobot'].cobotControl
        assert isinstance(config, CobotControl)

        if config.controller is None:
            await config.initializeController(session=self.session)
            # note that this awaits until controller is actually ready

        self._controller = config.controller

        self._controllerInitialized.set()

    def restoreLayoutIfAvailable(self) -> bool:
        if not self.finishedAsyncInitialization.is_set():
            return False
        else:
            return super().restoreLayoutIfAvailable()

    async def _onPanelInitializedAndSessionSet_async(self):
        if self._controller is None:
            if not self._hasStartedInitializingController:
                self._hasStartedInitializingController = True
                asyncio.create_task(asyncTryAndRaiseDialogOnError(self._initializeController))

        await self._controllerInitialized.wait()

        self._coordinator.sigCurrentTargetChanged.connect(lambda otherCoord=self._controller.targetingCoordinator: setattr(otherCoord, 'currentTargetKey', self._coordinator.currentTargetKey))

        dock, container = self._createDockWidget('Cobot control')
        self._cobotControlWdgt = CobotTargetingWidget(controller=self._controller)
        container.setLayout(QtWidgets.QVBoxLayout())
        container.layout().setContentsMargins(0, 0, 0, 0)
        container.layout().addWidget(self._cobotControlWdgt.wdgt)
        self._wdgt.addDock(dock, position='left')

        self.finishedAsyncInitialization.set()

        self.restoreLayoutIfAvailable()

    def _initializeDefaultViews(self):
        super()._initializeDefaultViews()

        self.addView(key='Workspace-Z', View='CobotWorkspace-Z')
        self.addView(key='Workspace-Y', View='CobotWorkspace-Y')

    def addView(self, key: str, View: str, **kwargs):
        match View:
            case 'CobotWorkspace-Z':
                View = CobotWorkspaceAlignedView
                kwargs.setdefault('title', 'Cobot Workspace (Z)')
                kwargs.setdefault('alignCameraTo', 'tool-CobotWorkspace+X')
                kwargs.setdefault('alignCameraOffset', (0, 0, 40))
                kwargs.setdefault('position', 'bottom')
                kwargs.setdefault('positionRelativeTo', self._views['Crosshairs-X'].dock)
            case 'CobotWorkspace-Y':
                View = CobotWorkspaceAlignedView
                kwargs.setdefault('title', 'Cobot Workspace (Y)')
                kwargs.setdefault('alignCameraTo', 'tool-CobotWorkspace+Z')
                kwargs.setdefault('position', 'bottom')
                kwargs.setdefault('positionRelativeTo', self._views['Crosshairs-Y'].dock)

        super().addView(key=key, View=View, **kwargs)


