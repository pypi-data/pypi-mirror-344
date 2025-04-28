import asyncio
import concurrent.futures

import attrs
import json
import logging
import numpy as np
from packaging.version import Version
import pytransform3d.rotations as ptr
import pytransform3d.transformations as ptt
import pyvista as pv
from skspatial.objects import Line, Plane, Vector
import time
import typing as tp
import zmq
import zmq.asyncio as azmq

from NaviNIBS_Cobot.Devices.CobotClient import CobotClient
from NaviNIBS_Cobot.Devices.CobotConnector import \
    cobotTargetingServerHostname, \
    cobotTargetingServerPubPort, \
    cobotTargetingServerCmdPort, \
    TargetingState, \
    ContactMode, \
    TargetChangeRetractMode, \
    TargetChangeContactMode


from NaviNIBS_Cobot.Devices.CobotConnector.CobotActionSequence import CobotActionSequence, CobotAction

from NaviNIBS.Devices.ToolPositionsClient import ToolPositionsClient, TimestampedToolPosition
from NaviNIBS.util import exceptionToStr
from NaviNIBS.util.Asyncio import asyncWaitWithCancel, asyncTryAndLogExceptionOnError
from NaviNIBS.util.logging import createLogFileHandler
from NaviNIBS.util.numpy import array_equalish
from NaviNIBS.util.Signaler import Signal
from NaviNIBS.util.Transforms import composeTransform, concatenateTransforms, invertTransform, applyTransform
from NaviNIBS.util.ZMQConnector import ZMQConnectorServer, logger as logger_ZMQConnector

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger_ZMQConnector.setLevel(logging.INFO)

SurfMesh = pv.PolyData
_novalue = object()


def posAndQuatToTransform(pos: tuple[float, float, float], quat: tuple[float, float, float, float]) -> np.ndarray:
    return ptt.transform_from_pq(np.concatenate([np.asarray(pos), np.asarray(quat)]))


def transformToPosAndQuat(transform: np.ndarray) -> tuple[tuple[float, float, float], tuple[float, float, float, float]]:
    pos, quat = np.split(ptt.pq_from_transform(transform), [3])
    return tuple(pos), tuple(quat)


@attrs.define(kw_only=True)
class CobotConnectorServer:
    """
    Some operations with the cobot are very time-sensitive, so we need our CobotClient to
    run in a dedicated process. This server will run the CobotClient and act as an intermediary for a CobotTargetingController running in the primary process.

    Note that because this is running outside of the main process, we don't rely on keeping track of the full Session model, instead assuming a ZMQConnector from the primary process will inform us of any necessary info.

    Things this class needs to do:
    - Keep client connected and feeding watchdog
    - Monitor joint positions and send to ToolPositionsServer
    - When targeting a location, monitor ToolPositionsServer for updates in subject head position, and send new target orientations to cobot to compensate for head movement
    - Handle state transitions for complex actions like transitioning between targets
    - (Optionally) keep transform between on-coil tracker and cobot's estimate of coil tracker position up to date

    """
    _hostname: str = cobotTargetingServerHostname
    _pubPort: int = cobotTargetingServerPubPort
    _cmdPort: int = cobotTargetingServerCmdPort

    _cobotAddr: str
    _cobotSyncPort: int = 13000
    _cobotAsyncPort: int = 13001
    _cobotIsSimulated: bool | None = None
    """
    If set to None, will be automatically determined based on IP. 
    If IP is set to '127.0.0.1' or 'localhost', isSimulated will be set to True. Else it will be set to False.
    """

    _logFilepath: str | None = None
    _logFileHandler: logging.FileHandler = attrs.field(init=False)

    _cobotSessionNameSuffix: str | None = None
    _doTrackCobotDevicePositions: bool = True
    _trackPositionsRate: float = 10.  # in Hz

    _cobotConnectedEvent: asyncio.Event = attrs.field(init=False, factory=asyncio.Event)

    _connector: ZMQConnectorServer = attrs.field(init=False, repr=False)

    _cobotClient: CobotClient = attrs.field(init=False)
    _positionsClient: ToolPositionsClient | None = attrs.field(init=False, default=None)

    _subjectTrackerToMRITransf: np.ndarray | None = attrs.field(default=None)
    _subjectTrackerKey: str | None = attrs.field(default=None)

    _targetLabel: str | None = attrs.field(default=None)
    sigTargetLabelChanged: Signal = attrs.field(init=False, factory=Signal)
    __targetIsAccessible: bool | None = attrs.field(init=False, default=None)
    sigTargetAccessibleChanged: Signal = attrs.field(init=False, factory=Signal)

    _targetCoilToMRITransf: np.ndarray | None = attrs.field(default=None)
    _targetingInfoUpdatedEvent: asyncio.Event = attrs.field(init=False, factory=asyncio.Event)

    _monitorTargetAccessibilityRate: float = 2.  # in Hz

    _lastMeasuredForce: float | None = attrs.field(init=False, default=None)
    sigMeasuredForceChanged: Signal = attrs.field(init=False, factory=Signal)
    _monitorMeasuredForceRate: float = 5.  # in Hz

    _lastRawCoilIDValue: float | None = attrs.field(init=False, default=None)
    sigRawCoilIDValueChanged: Signal = attrs.field(init=False, factory=Signal)

    _lastRawForceValue: float | None = attrs.field(init=False, default=None)
    sigRawForceValueChanged: Signal = attrs.field(init=False, factory=Signal)

    _lastSensitivity: float | None = attrs.field(init=False, default=None)
    sigSensitivityChanged: Signal = attrs.field(init=False, factory=Signal)
    """
    Note: sensitivity is only updated when also monitoring measured force
    """

    _minContactTimeForStability: float = 5.  # in seconds

    _realignWhenDistErrorExceeds: float = 1.  # in mm
    _realignWhenZAngleErrorExceeds: float = 2  # in deg
    _realignWhenHorizAngleErrorExceeds: float = 4  # in deg

    _moveWhenZDistErrorExceeds: float = 1.  # in mm; only applies when targeting state is MOVED

    sigRealignThresholdsChanged: Signal = attrs.field(init=False, factory=Signal)

    _alignedWhenDistErrorUnder: float = 0.5  # in mm
    _alignedWhenZAngleErrorUnder: float = 1.  # in deg
    _alignedWhenHorizAngleErrorUnder: float = 2.  # in deg

    _doneMovingWhenZDistErrorUnder: float = 0.5  # in mm; only applies when targeting state is MOVING

    # more relaxed thresholds for determining things like when we're aligned "enough" to start servoing down to a new target
    _approximatelyAlignedWhenDistErrorUnder: float = 4.  # in mm
    _approximatelyAlignedWhenZAngleErrorUnder: float = 4.  # in deg
    _approximatelyAlignedWhenHorizAngleErrorUnder: float = 8.  # in deg

    _almostDoneMovingWhenZDistErrorUnder: float = 4  # in mm; only applies when targeting state is MOVING

    _isApproximatelyAlignedEvent: asyncio.Event = attrs.field(init=False, factory=asyncio.Event)  # only updated while tracking a target
    sigIsApproximatelyAlignedChanged: Signal = attrs.field(init=False, factory=Signal)

    sigAlignedThresholdsChanged: Signal = attrs.field(init=False, factory=Signal)

    _cobotCoilTrackerKey: str = 'CobotCoil'
    _cobotCoilToolToTrackerTransf: np.ndarray | None = attrs.field(default=None, init=False)
    """
    Used to potentially correct for any misalignment between Cobot's idea of coil position vs. actual measured coil position.
    
    When necessary information is available, this is updated automatically.
    """
    sigCobotCoilToolChanged: Signal = attrs.field(init=False, factory=Signal)

    _cobotCoilTrackerToNaviNIBSCoilCoordTransf: np.ndarray = attrs.field(
        factory=lambda: composeTransform(ptr.active_matrix_from_intrinsic_euler_yzy([np.pi, -np.pi / 2, 0])))

    _coilTrackerKey: str | None = attrs.field(default=None)
    """
    If not None and not equal to cobotCoilTrackerKey, this represents key of a tracker mounted on (or near) the coil.
    Can be used for improving accuracy of coil pose estimation compared to relying on distant cobot cart tracker.
    """
    _coilToolToTrackerTransf: np.ndarray | None = attrs.field(default=None)
    """
    Typically this is the transform resulting from manual coil calibration. Should be set externally.
    """
    sigCoilToolChanged: Signal = attrs.field(init=False, factory=Signal)

    _activeCartTrackerKey: str | None = attrs.field(init=False, default=None)

    _headMeshPath: str | None = attrs.field(default=None)  # assumed to be in MRI space
    _headMesh: SurfMesh | None = attrs.field(init=False, default=None)

    _doSimulateForceReadings: bool = True
    # these are only used if cobot is simulated and set to simulate force readings:
    _coilMeshPath: str | None = attrs.field(default=None)
    _coilMesh: SurfMesh | None = attrs.field(init=False, default=None)
    _coilMeshToToolTransf: np.ndarray | None = attrs.field(default=None)
    _simulatedForceOffsetDistance: float = 4.  # in mm, positive numbers cause force to start increasing sooner as coil approaches head
    _simulatedForceInfoUpdatedEvent: asyncio.Event = attrs.field(init=False, factory=asyncio.Event)
    _lastSetForce: float | None = attrs.field(init=False, default=None)
    _lastSetNonzeroForce: bool = attrs.field(init=False, default=False)

    _state: TargetingState = attrs.field(init=False, default=TargetingState.DISCONNECTED)
    stateChangedEvent: asyncio.Event() = attrs.field(init=False, factory=asyncio.Event)
    sigStateChanged: Signal = attrs.field(init=False, factory=Signal)

    _contactMode: ContactMode = attrs.field(init=False, default=ContactMode.DEFAULT)
    sigContactModeChanged: Signal = attrs.field(init=False, factory=Signal)
    _targetZOffsetAtForceThreshold: float | None = attrs.field(init=False, default=None)
    sigHasCalibratedContactDepthForCurrentTargetChanged: Signal = attrs.field(init=False, factory=Signal)
    _airgapOffsetFromContact: float = attrs.field(default=5.)
    sigAirgapOffsetFromContactChanged: Signal = attrs.field(init=False, factory=Signal)
    _targetZOffsetAtScalp: float | None = attrs.field(init=False, default=None)
    _airgapOffsetFromScalp: float = attrs.field(default=5.)
    sigAirgapOffsetFromScalpChanged: Signal = attrs.field(init=False, factory=Signal)
    _airgapOffsetFromTarget: float = attrs.field(default=5.)
    sigAirgapOffsetFromTargetChanged: Signal = attrs.field(init=False, factory=Signal)

    _isTryingToContact: bool = attrs.field(init=False, default=False)
    """
    High-level indicator of whether we're trying to "contact" (or airgap/freeze at contact according to contactMode)
    
    Note that this may be circumvented by low-level commands sent directly to cobot or asynchronous changes like an emergency stop 
    """
    sigTryingToContactChanged: Signal = attrs.field(init=False, factory=Signal)

    _distantTargetChangeRetractMode: TargetChangeRetractMode = attrs.field(init=False, default=TargetChangeRetractMode.FULLY_RETRACT_THEN_ALIGN)
    sigDistantTargetChangeRetractModeChanged: Signal = attrs.field(init=False, factory=Signal)
    _distantTargetChangeContactMode: TargetChangeContactMode = attrs.field(init=False, default=TargetChangeContactMode.RESUME_WHEN_APPROXIMATELY_ALIGNED)
    sigDistantTargetChangeContactModeChanged: Signal = attrs.field(init=False, factory=Signal)

    _nearTargetChangeRetractMode: TargetChangeRetractMode = attrs.field(init=False, default=TargetChangeRetractMode.PARTIALLY_RETRACT_AND_ALIGN)
    sigNearTargetChangeRetractModeChanged: Signal = attrs.field(init=False, factory=Signal)
    _nearTargetChangeContactMode: TargetChangeContactMode = attrs.field(init=False, default=TargetChangeContactMode.RESUME_WHEN_APPROXIMATELY_ALIGNED)
    sigNearTargetChangeContactModeChanged: Signal = attrs.field(init=False, factory=Signal)

    _targetChangeDistanceThreshold: float = attrs.field(init=False, default=15.)  # maximum distance (in mm) between targets to be considered "near"
    _targetChangeAngleThreshold: float = attrs.field(init=False, default=15.)  # maximum angle (in deg) between targets to be considered "near"
    sigTargetChangeDistanceThresholdChanged: Signal = attrs.field(init=False, factory=Signal)
    sigTargetChangeAngleThresholdChanged: Signal = attrs.field(init=False, factory=Signal)

    _actionSequenceStack: list[CobotActionSequence] = attrs.field(init=False, factory=list)
    actionSequenceStackChangedEvent: asyncio.Event() = attrs.field(init=False, factory=asyncio.Event)
    sigActionSequenceStackChanged: Signal = attrs.field(init=False, factory=Signal)
    _runActionSequencesTask: asyncio.Task | None = attrs.field(init=False, default=None)

    _latestJointPositions: dict[str, list[float]] = attrs.field(init=False, factory=dict)
    sigJointPositionsChanged: Signal = attrs.field(init=False, factory=Signal)
    _latestJointPositionLimits: dict[str, list[float]] = attrs.field(init=False, factory=dict)
    sigJointPositionLimitsChanged: Signal = attrs.field(init=False, factory=Signal)

    def __attrs_post_init__(self):
        if self._logFilepath is not None:
            self._logFileHandler = createLogFileHandler(self._logFilepath)
            logging.getLogger('').addHandler(self._logFileHandler)

        logger.info(f'Initializing {self.__class__.__name__}')

        self._connector = ZMQConnectorServer(
            obj=self,
            reqRepPort=self._cmdPort,
            pubSubPort=self._pubPort,
            bindAddr=self._hostname
        )

        isSimulated = self._cobotIsSimulated
        if isSimulated is None:
            isSimulated = self._cobotAddr in ('127.0.0.1', 'localhost')

        self._cobotClient = CobotClient(
            host=self._cobotAddr,
            syncPort=self._cobotSyncPort,
            asyncPort=self._cobotAsyncPort,
            isSimulated=isSimulated
        )

        asyncio.create_task(asyncTryAndLogExceptionOnError(self.connectToCobotAndInitialize,
                                                           assertFromScratch=True))

        self._positionsClient = ToolPositionsClient()

        if self._doTrackCobotDevicePositions:
            asyncio.create_task(asyncTryAndLogExceptionOnError(self._loop_trackCobotDevicePositions))

        asyncio.create_task(asyncTryAndLogExceptionOnError(self._loop_stateMachine))

        asyncio.create_task(asyncTryAndLogExceptionOnError(self._loop_monitorForceSensor))

        asyncio.create_task(asyncTryAndLogExceptionOnError(self._loop_monitorTargetAccessibility))

        asyncio.create_task(asyncTryAndLogExceptionOnError(self._loop_alignCoilPoses))

        if self._doSimulateForceReadings:
            self._positionsClient.sigLatestPositionsChanged.connect(lambda: self._simulatedForceInfoUpdatedEvent.set())
            asyncio.create_task(asyncTryAndLogExceptionOnError(self._loop_simulateForce))

        # connect to cobotClient signals
        for sig in (
            'sigConnectedChanged',
            'sigEnabledChanged',
            'sigControlIsLockedChanged',
            'sigPoweredChanged',
            'sigHomedChanged',
            'sigAlignMotionInProgressChanged',
            'sigAlignMotionAbortedChanged',
            'sigInToleranceToDestinationChanged',
            'sigContactChanged',
            'sigServoingChanged',
            'sigFreedriveButtonPressedChanged',
            'sigAxesMovingChanged',
            'sigEstopped',
            'sigFreedrivingChanged',
            'sigInProtectiveStopChanged',
            'sigInWorkspaceChanged'
        ):
            getattr(self._cobotClient, sig).connect(lambda sig=sig: self._onClientSignaled(sig))

        for sig in (
            'sigMeasuredForceChanged',
            'sigSensitivityChanged',
            'sigTargetLabelChanged',
            'sigTargetAccessibleChanged',
            'sigStateChanged',
            'sigContactModeChanged',
            'sigAirgapOffsetFromContactChanged',
            'sigAirgapOffsetFromScalpChanged',
            'sigAirgapOffsetFromTargetChanged',
            'sigDistantTargetChangeRetractModeChanged',
            'sigDistantTargetChangeContactModeChanged',
            'sigNearTargetChangeRetractModeChanged',
            'sigNearTargetChangeContactModeChanged',
            'sigTargetChangeDistanceThresholdChanged',
            'sigTargetChangeAngleThresholdChanged',
            'sigTryingToContactChanged',
            'sigHasCalibratedContactDepthForCurrentTargetChanged',
            'sigRealignThresholdsChanged',
            'sigAlignedThresholdsChanged',
            'sigActionSequenceStackChanged',
            'sigIsApproximatelyAlignedChanged',
            'sigCobotCoilToolChanged',
            'sigCoilToolChanged',
            'sigJointPositionsChanged',
            'sigJointPositionLimitsChanged',
        ):
            getattr(self, sig).connect(lambda sig=sig: self._connector.publish([b'signal', sig.encode('utf-8')]))

        self.sigContactModeChanged.connect(lambda: self._updateState(['sigContactModeChanged']))

    def __del__(self):
        logger.info('Deleting CobotConnectorServer')

    class MissingInformationError(RuntimeError):
        pass

    @property
    def cobotSessionNameSuffix(self):
        return self._cobotSessionNameSuffix

    @property
    def cobotClient(self):
        return self._cobotClient

    @property
    def subjectTrackerToMRITransf(self):
        return self._subjectTrackerToMRITransf

    @subjectTrackerToMRITransf.setter
    def subjectTrackerToMRITransf(self, val: np.ndarray | list[float] | None):
        if isinstance(val, list):
            val = np.asarray(val)
        if array_equalish(self._subjectTrackerToMRITransf, val):
            return

        logger.info(f'Setting new subjectTrackerToMRITransf: {val}')
        self._subjectTrackerToMRITransf = val
        self._targetingInfoUpdatedEvent.set()
        self._simulatedForceInfoUpdatedEvent.set()

    @property
    def subjectTrackerKey(self):
        return self._subjectTrackerKey

    @subjectTrackerKey.setter
    def subjectTrackerKey(self, val: str | None):
        if self._subjectTrackerKey == val:
            return
        logger.info(f'Setting new subjectTrackerKey: {val}')
        self._subjectTrackerKey = val
        self._targetingInfoUpdatedEvent.set()
        self._simulatedForceInfoUpdatedEvent.set()

    @property
    def targetLabel(self):
        return self._targetLabel

    @targetLabel.setter
    def targetLabel(self, val: str | None):
        if self._targetLabel == val:
            return
        logger.info(f'Setting new targetLabel: {val}')
        self._targetLabel = val
        self.sigTargetLabelChanged.emit()

    @property
    def targetCoilToMRITransf(self):
        return self._targetCoilToMRITransf

    @targetCoilToMRITransf.setter
    def targetCoilToMRITransf(self, newCoilToMRITransf: np.ndarray | list[float] | None):
        if isinstance(newCoilToMRITransf, list):
            newCoilToMRITransf = np.asarray(newCoilToMRITransf)
        if array_equalish(self._targetCoilToMRITransf, newCoilToMRITransf):
            return

        logger.info(f'Setting new targetCoilToMRITransf: {newCoilToMRITransf}')

        self.isApproximatelyAligned = False  # will be re-set if still aligned on first check when in appropriate state
        # TODO: maybe set up a way to only clear isApproximatelyAligned after checking if we are no longer aligned at new target
        # (but with minimal extra CPU work)

        if self._state in (
            TargetingState.ALIGNED_SERVOING,
            TargetingState.ALIGNED_CONTACTING,
            TargetingState.ALIGNED_RETRACTING,
            TargetingState.ALIGNED_RETRACTED,
            TargetingState.ALIGNING_SERVOING,
            TargetingState.ALIGNING_CONTACTING,
            TargetingState.ALIGNING_RETRACTING,
            TargetingState.ALIGNING_RETRACTED,
            TargetingState.MOVING,
            TargetingState.MOVED,
            TargetingState.MOVED_FROZEN,
        ):
            # check if new target is near or far, and change state accordingly
            assert self._targetCoilToMRITransf is not None
            actionSequence = CobotActionSequence(label='Change target')
            if newCoilToMRITransf is None:
                # target cleared
                match self._state:
                    case TargetingState.ALIGNED_SERVOING |\
                            TargetingState.ALIGNED_CONTACTING |\
                            TargetingState.ALIGNING_SERVOING |\
                            TargetingState.ALIGNING_CONTACTING |\
                            TargetingState.MOVING |\
                            TargetingState.MOVED |\
                            TargetingState.MOVED_FROZEN:
                        self._changeToState(TargetingState.UNALIGNED_RETRACTING)
                        actionSequence.append(CobotAction(asyncFn=self.stopContact))
                    case TargetingState.ALIGNED_RETRACTED |\
                            TargetingState.ALIGNING_RETRACTED:
                        self._changeToState(TargetingState.IDLE)
            else:
                # target changed

                # TODO: handle case where old target may be very close to new target
                #  (implying minimal change needed), but actual coil position is very far from both targets (implying larger change needed)

                if self._areTargetsNear(self._targetCoilToMRITransf, newCoilToMRITransf):
                    logger.info('Changing to a nearby target')
                    changeRetractMode = self._nearTargetChangeRetractMode
                    changeContactMode = self._nearTargetChangeContactMode
                else:
                    logger.info('Changing to a distant target')
                    changeRetractMode = self._distantTargetChangeRetractMode
                    changeContactMode = self._distantTargetChangeContactMode

                prevState = self._state

                if changeRetractMode != TargetChangeRetractMode.ALIGN_WITHOUT_RETRACT:
                    if self._state not in (
                        TargetingState.ALIGNED_RETRACTED,
                        TargetingState.ALIGNING_RETRACTED,
                    ):
                        # need to retract (or at least start retracting) before aligning
                        # TODO: add extra code to handle limited retract
                        logger.info('Starting to retract before aligning to new target')
                        self.stopTrackingTarget_sync()  # note that this must be run synchronously, immediately, to prevent aligning to newly set transform
                        actionSequence.append(CobotAction(asyncFn=self.stopContact))
                        match changeRetractMode:
                            case TargetChangeRetractMode.FULLY_RETRACT_THEN_ALIGN:
                                actionSequence.append(CobotAction(asyncFn=self.waitForChangeToState, args=(TargetingState.IDLE,)))
                            case TargetChangeRetractMode.PARTIALLY_RETRACT_AND_ALIGN:
                                actionSequence.append(CobotAction(asyncFn=self.waitForTime, args=(1.0,)))  # TODO: make wait time an attribute rather than hardcoding here
                            case TargetChangeRetractMode.LIMITED_RETRACT_THEN_ALIGN:
                                raise NotImplementedError  # TODO
                            case _:
                                raise NotImplementedError

                actionSequence.append(CobotAction(asyncFn=self.startTrackingTarget))

                wasPreviouslyNotContacting = prevState in (
                    TargetingState.ALIGNED_RETRACTED,
                    TargetingState.ALIGNED_RETRACTING,
                    TargetingState.ALIGNING_RETRACTED,
                    TargetingState.ALIGNING_RETRACTING,
                )

                match changeContactMode:
                    case TargetChangeContactMode.DO_NOT_RESUME_CONTACT:
                        pass

                    case TargetChangeContactMode.RESUME_IMMEDIATELY |\
                        TargetChangeContactMode.INITIATE_IMMEDIATELY:
                        if changeContactMode == TargetChangeContactMode.RESUME_IMMEDIATELY and wasPreviouslyNotContacting:
                            pass  # was not contacting before, don't resume
                        else:
                            actionSequence.append(CobotAction(asyncFn=self.startContact))

                    case TargetChangeContactMode.RESUME_WHEN_IN_TOLERANCE |\
                            TargetChangeContactMode.INITIATE_WHEN_IN_TOLERANCE:
                        if changeContactMode == TargetChangeContactMode.RESUME_WHEN_IN_TOLERANCE and wasPreviouslyNotContacting:
                            pass  # was not contacting before, don't resume
                        else:
                            actionSequence.append(CobotAction(asyncFn=self.waitForInTolerance))
                            actionSequence.append(CobotAction(asyncFn=self.startContact))

                    case TargetChangeContactMode.RESUME_WHEN_APPROXIMATELY_ALIGNED |\
                        TargetChangeContactMode.INITIATE_WHEN_APPROXIMATELY_ALIGNED:
                        if changeContactMode == TargetChangeContactMode.RESUME_WHEN_APPROXIMATELY_ALIGNED and wasPreviouslyNotContacting:
                            pass  # was not contacting before, don't resume
                        else:
                            actionSequence.append(CobotAction(asyncFn=self.waitForApproximatelyAligned))
                            actionSequence.append(CobotAction(asyncFn=self.startContact))

                    case TargetChangeContactMode.RESUME_WHEN_ALIGNED |\
                            TargetChangeContactMode.INITIATE_WHEN_ALIGNED:
                        if changeContactMode == TargetChangeContactMode.RESUME_WHEN_ALIGNED and wasPreviouslyNotContacting:
                            pass  # was not contacting before, don't resume
                        else:
                            actionSequence.append(CobotAction(asyncFn=self.waitForChangeToState, args=(
                                [TargetingState.ALIGNED_RETRACTED,
                                 TargetingState.ALIGNED_RETRACTING],
                            )))
                            actionSequence.append(CobotAction(asyncFn=self.startContact))

                    case _:
                        raise NotImplementedError

                asyncio.create_task(asyncTryAndLogExceptionOnError(self.startActionSequence, actionSequence))

        self._targetCoilToMRITransf = newCoilToMRITransf
        self._targetZOffsetAtForceThreshold = None  # reset calibrated offset whenever target changes
        self.sigHasCalibratedContactDepthForCurrentTargetChanged.emit()
        self._targetZOffsetAtScalp = None  # reset cached offset whenever target changes
        self._targetingInfoUpdatedEvent.set()

    @property
    def maybeOffsetTargetCoilToMRITransf(self):
        if self._targetCoilToMRITransf is None:
            return None

        modifiedTargetCoilToMRITransf = self._targetCoilToMRITransf.copy()
        # logger.debug(f'targetCoilToMRITransf before any offsets: {modifiedTargetCoilToMRITransf}')
        match self.contactMode:
            case ContactMode.DEFAULT:
                pass

            case ContactMode.CONTACT_THEN_FREEZE:
                if self._targetZOffsetAtForceThreshold is not None:
                    extraTransf = np.eye(4)
                    extraTransf[2, 3] = self._targetZOffsetAtForceThreshold
                    modifiedTargetCoilToMRITransf = concatenateTransforms(
                        [extraTransf, modifiedTargetCoilToMRITransf]
                    )

            case ContactMode.AIRGAPPED_FROM_CONTACT:
                if self._targetZOffsetAtForceThreshold is not None:
                    extraTransf = np.eye(4)
                    extraTransf[2, 3] = self._targetZOffsetAtForceThreshold
                    extraTransf[2, 3] += self._airgapOffsetFromContact

                    logger.debug(f'zOffsetAtForce: {self._targetZOffsetAtForceThreshold}  zOffsetAirgap: {self._airgapOffsetFromContact}   extraTransf: {extraTransf}')

                    modifiedTargetCoilToMRITransf = concatenateTransforms(
                        [extraTransf, modifiedTargetCoilToMRITransf]
                    )

            case ContactMode.AIRGAPPED_FROM_SCALP:
                headMesh = self.getHeadMesh_sync()
                if headMesh is None:
                    logger.warning('Cannot airgap from scalp without head mesh')
                else:
                    extraTransf = np.eye(4)
                    extraTransf[2, 3] = self.targetZOffsetAtScalp
                    extraTransf[2, 3] += self._airgapOffsetFromScalp

                    logger.debug(f'zOffsetAtScalp: {self._targetZOffsetAtScalp}  zOffsetAirgap: {self._airgapOffsetFromScalp}   extraTransf: {extraTransf}')

                    modifiedTargetCoilToMRITransf = concatenateTransforms(
                        [extraTransf, modifiedTargetCoilToMRITransf]
                    )

            case ContactMode.OFFSET_FROM_TARGET:
                extraTransf = np.eye(4)
                extraTransf[2, 3] = 0
                extraTransf[2, 3] += self._airgapOffsetFromTarget

                logger.debug(
                    f'zOffsetAirgap: {self._airgapOffsetFromTarget}   extraTransf: {extraTransf}')

                modifiedTargetCoilToMRITransf = concatenateTransforms(
                    [extraTransf, modifiedTargetCoilToMRITransf]
                )

            case _:
                raise NotImplementedError

        # logger.debug(f'targetCoilToMRITransf after any offsets: {modifiedTargetCoilToMRITransf}')
        return modifiedTargetCoilToMRITransf

    @property
    def cobotCoilTrackerKey(self):
        return self._cobotCoilTrackerKey

    @cobotCoilTrackerKey.setter
    def cobotCoilTrackerKey(self, val: str | None):
        if self._cobotCoilTrackerKey == val:
            return
        logger.info(f'Setting new cobotCoilTrackerKey: {val}')
        self._cobotCoilTrackerKey = val
        self.sigCobotCoilToolChanged.emit()

    @property
    def cobotCoilToolToTrackerTransf(self):
        return self._cobotCoilToolToTrackerTransf

    def getCobotCoilToolToTrackerTransfAsList(self):
        transf = self.cobotCoilToolToTrackerTransf
        if transf is None:
            return None
        else:
            return transf.tolist()

    @cobotCoilToolToTrackerTransf.setter
    def cobotCoilToolToTrackerTransf(self, val: np.ndarray | list | None):
        if isinstance(val, list):
            val = np.asarray(val)
        if array_equalish(self._cobotCoilToolToTrackerTransf, val):
            return
        logger.debug(f'Setting new cobotCoilToolToTrackerTransf: {val}')
        self._cobotCoilToolToTrackerTransf = val
        self.sigCobotCoilToolChanged.emit()

    @property
    def coilTrackerKey(self):
        return self._coilTrackerKey

    @coilTrackerKey.setter
    def coilTrackerKey(self, val: str | None):
        if self._coilTrackerKey == val:
            return
        logger.info(f'Setting new coilTrackerKey: {val}')
        self._coilTrackerKey = val
        self.cobotCoilToolToTrackerTransf = None
        self._simulatedForceInfoUpdatedEvent.set()
        self.sigCoilToolChanged.emit()

    @property
    def headMeshPath(self):
        return self._headMeshPath

    @headMeshPath.setter
    def headMeshPath(self, val: str | None):
        if self._headMeshPath == val:
            return
        logger.info(f'Setting new headMeshPath: {val}')
        self._headMeshPath = val
        if self._headMesh is not None:
            # clear cached mesh
            self._headMesh = None
        asyncio.create_task(asyncTryAndLogExceptionOnError(self.getHeadMesh))  # start loading new mesh immediately to try to have ready for any non-async methods that might need it
        self._simulatedForceInfoUpdatedEvent.set()

    def getHeadMesh_sync(self) -> SurfMesh | None:
        """
        Get mesh synchronously, blocking until it is loaded
        """
        if self._headMesh is None:
            if self._headMeshPath is not None:
                asyncio.create_task(asyncTryAndLogExceptionOnError(self.getHeadMesh))
            return None  # None can indicate path is not set, or is loading and will be available soon

        return self._headMesh

    async def getHeadMesh(self) -> SurfMesh | None:
        """
        Get mesh asynchronously in a separate thread so that load time doesn't cause
        us to trigger the watchdog
        """
        if self._headMesh is None:
            if self._headMeshPath is None:
                return None
            logger.info('Loading head mesh asynchronously')
            loop = asyncio.get_running_loop()
            with concurrent.futures.ProcessPoolExecutor() as pool:
                self._headMesh = await loop.run_in_executor(pool, pv.read, self._headMeshPath)
        return self._headMesh

    @property
    def coilMeshPath(self):
        return self._coilMeshPath

    @coilMeshPath.setter
    def coilMeshPath(self, val: str | None):
        if self._coilMeshPath == val:
            return
        logger.info(f'Setting new coilMeshPath: {val}')
        self._coilMeshPath = val
        if self._coilMesh is not None:
            # clear cached mesh
            self._coilMesh = None
        self._simulatedForceInfoUpdatedEvent.set()

    async def getCoilMesh(self) -> SurfMesh | None:
        """
        Get mesh asynchronously in a separate thread so that load time doesn't cause
        us to trigger the watchdog
        """
        if self._coilMesh is None:
            if self._coilMeshPath is None:
                return None
            logger.info('Loading coil mesh asynchronously')
            loop = asyncio.get_running_loop()
            with concurrent.futures.ProcessPoolExecutor() as pool:
                self._coilMesh = await loop.run_in_executor(pool, pv.read, self._coilMeshPath)
        return self._coilMesh

    @property
    def coilMeshToToolTransf(self):
        return self._coilMeshToToolTransf

    @coilMeshToToolTransf.setter
    def coilMeshToToolTransf(self, val: np.ndarray | list[float] | None):
        if isinstance(val, list):
            val = np.asarray(val)
        if array_equalish(self._coilMeshToToolTransf, val):
            return
        logger.info(f'Setting new coilMeshToTrackerTransf: {val}')
        self._coilMeshToToolTransf = val
        self._simulatedForceInfoUpdatedEvent.set()

    @property
    def coilToolToTrackerTransf(self):
        return self._coilToolToTrackerTransf

    @coilToolToTrackerTransf.setter
    def coilToolToTrackerTransf(self, val: np.ndarray | list[float] | None):
        if isinstance(val, list):
            val = np.asarray(val)
        if array_equalish(self._coilToolToTrackerTransf, val):
            return
        logger.info(f'Setting new coilToolToTrackerTransf: {val}')
        self._coilToolToTrackerTransf = val
        self._simulatedForceInfoUpdatedEvent.set()
        self.sigCoilToolChanged.emit()

    @property
    def state(self):
        return self._state

    @property
    def contactMode(self):
        return self._contactMode

    @contactMode.setter
    def contactMode(self, val: ContactMode | int):
        if isinstance(val, int):
            val = ContactMode(val)
        if self._contactMode == val:
            return
        logger.info(f'Setting new contactMode: {val.name}')

        if self._isTryingToContact:
            if val == ContactMode.DEFAULT:
                raise RuntimeError('Cannot change contact mode to DEFAULT while previously trying to contact; use async setter to automatically handle transition, or manually stop contact before calling sync setter')

        self._contactMode = val
        self.sigContactModeChanged.emit()

        if self._isTryingToContact:
            asyncio.create_task(asyncTryAndLogExceptionOnError(self.startContact))  # start contact with new mode

    async def setContactMode(self, contactMode: ContactMode):
        if contactMode == self.contactMode:
            return

        if self._isTryingToContact and contactMode == ContactMode.DEFAULT:
            # temporarily stop contact while in previous mode, change mode, then resume contact
            actionSequence = CobotActionSequence(
                label='Pause contact, change contact mode, and resume contact',
                actions=[
                    CobotAction(asyncFn=self.stopContact),
                    CobotAction(asyncFn=self.setContactMode, args=[contactMode]),
                    CobotAction(asyncFn=self.startContact)
                ])
            await self.startActionSequence(actionSequence)
        else:
            self.contactMode = contactMode

    @property
    def nearTargetChangeRetractMode(self):
        return self._nearTargetChangeRetractMode

    @nearTargetChangeRetractMode.setter
    def nearTargetChangeRetractMode(self, val: TargetChangeRetractMode | int):
        if isinstance(val, int):
            val = TargetChangeRetractMode(val)
        if self._nearTargetChangeRetractMode == val:
            return
        logger.info(f'Setting new nearTargetChangeRetractMode: {val.name}')

        self._nearTargetChangeRetractMode = val
        self.sigNearTargetChangeRetractModeChanged.emit()

    @property
    def distantTargetChangeRetractMode(self):
        return self._distantTargetChangeRetractMode

    @distantTargetChangeRetractMode.setter
    def distantTargetChangeRetractMode(self, val: TargetChangeRetractMode | int):
        if isinstance(val, int):
            val = TargetChangeRetractMode(val)
        if self._distantTargetChangeRetractMode == val:
            return
        logger.info(f'Setting new distantTargetChangeRetractMode: {val.name}')

        self._distantTargetChangeRetractMode = val
        self.sigDistantTargetChangeRetractModeChanged.emit()

    @property
    def nearTargetChangeContactMode(self):
        return self._nearTargetChangeContactMode

    @nearTargetChangeContactMode.setter
    def nearTargetChangeContactMode(self, val: TargetChangeContactMode | int):
        if isinstance(val, int):
            val = TargetChangeContactMode(val)
        if self._nearTargetChangeContactMode == val:
            return
        logger.info(f'Setting new nearTargetChangeContactMode: {val.name}')

        self._nearTargetChangeContactMode = val
        self.sigNearTargetChangeContactModeChanged.emit()

    @property
    def distantTargetChangeContactMode(self):
        return self._distantTargetChangeContactMode

    @distantTargetChangeContactMode.setter
    def distantTargetChangeContactMode(self, val: TargetChangeContactMode | int):
        if isinstance(val, int):
            val = TargetChangeContactMode(val)
        if self._distantTargetChangeContactMode == val:
            return
        logger.info(f'Setting new distantTargetChangeContactMode: {val.name}')

        self._distantTargetChangeContactMode = val
        self.sigDistantTargetChangeContactModeChanged.emit()

    @property
    def isTryingToContact(self):
        return self._isTryingToContact

    async def run(self):
        while True:
            await asyncio.sleep(1.)

    async def connectToCobotAndInitialize(self, assertFromScratch: bool = False):
        logger.info('connecting to cobot and initializing')

        if self._state not in (TargetingState.DISCONNECTED, TargetingState.UNINITIALIZED):
            if assertFromScratch:
                raise RuntimeError('Already connected and initialized')
            else:
                logger.warning('Already connected and initialized')
                return

        if assertFromScratch:
            assert not self._cobotConnectedEvent.is_set()

        await asyncio.sleep(0.1)
        if not self._cobotClient.isConnected and not self._cobotClient.isConnecting.locked():
            await self._cobotClient.connect()

        await self._cobotClient.connectedEvent.wait()

        if True:
            # log controller and robot IDs
            logger.info(f'Controller ID: {await self._cobotClient.getControllerID()}')

            logger.info(f'Robot ID: {await self._cobotClient.getRobotID()}')

        if self._cobotClient.sessionHasStarted:
            if assertFromScratch:
                raise RuntimeError('Session already started')
        else:
            logger.info('Starting session')
            await self.startSession()

        if assertFromScratch and self._cobotClient.isPoweredOn:
            # may have been powered on by previous session (?)
            # (should only happen during simulator testing when watchdog is disabled)
            logger.info('Powering off')
            await self._cobotClient.powerOff()
            await asyncio.sleep(1.)

        baseTracker = self._cobotClient.BaseTracker.Right  # TODO: let client set rather than hardcoding here
        if await self._cobotClient.getActiveBaseTracker() != baseTracker:
            await self._cobotClient.setActiveBaseTracker(baseTracker)

        if not self._cobotClient.isPoweredOn:
            logger.info('Powering on')
            await self._cobotClient.powerOn()
            await self._cobotClient.poweredOnEvent.wait()

        if self._cobotClient.isHomed:
            if assertFromScratch:
                raise RuntimeError('Already homed')
        else:
            logger.info('Homing')
            await self._cobotClient.startHoming()
            # TODO: add simultaneous await for homing error, stop / retry init
            await self._cobotClient.homedEvent.wait()

        match await self._cobotClient.getActiveBaseTracker():
            case self._cobotClient.BaseTracker.Left:
                cartTrackerKey = 'CobotLeft'
            case self._cobotClient.BaseTracker.Right:
                cartTrackerKey = 'CobotRight'
            case _:
                raise NotImplementedError

        self._activeCartTrackerKey = cartTrackerKey

        self._cobotConnectedEvent.set()
        logger.info('Cobot connected, session started, and homed')

    @property
    def lastMeasuredForce(self):
        return self._lastMeasuredForce

    @property
    def __lastMeasuredForce(self):
        return self._lastMeasuredForce

    @__lastMeasuredForce.setter
    def __lastMeasuredForce(self, val: float | None):
        if self._lastMeasuredForce == val:
            return
        logger.debug(f'New measured force: {val}')
        self._lastMeasuredForce = val
        self.sigMeasuredForceChanged.emit()

    @property
    def lastRawCoilIDValue(self):
        return self._lastRawCoilIDValue

    @property
    def __lastRawCoilIDValue(self):
        return self._lastRawCoilIDValue

    @__lastRawCoilIDValue.setter
    def __lastRawCoilIDValue(self, val: float | None):
        if self._lastRawCoilIDValue == val:
            return
        logger.debug(f'New raw coil ID value: {val}')
        self._lastRawCoilIDValue = val
        self.sigRawCoilIDValueChanged.emit()

    @property
    def lastRawForceValue(self):
        return self._lastRawForceValue

    @property
    def __lastRawForceValue(self):
        return self._lastRawForceValue

    @__lastRawForceValue.setter
    def __lastRawForceValue(self, val: float | None):
        if self._lastRawForceValue == val:
            return
        logger.debug(f'New raw force value: {val}')
        self._lastRawForceValue = val
        self.sigRawForceValueChanged.emit()

    @property
    def sensitivity(self):
        return self._lastSensitivity

    @property
    def __lastSensitivity(self):
        return self._lastSensitivity

    @__lastSensitivity.setter
    def __lastSensitivity(self, val: float | None):
        if self._lastSensitivity == val:
            return
        logger.debug(f'New sensitivity: {val}')
        self._lastSensitivity = val
        self.sigSensitivityChanged.emit()

    async def getSensitivity(self) -> float:
        self.__lastSensitivity = await self._cobotClient.getSensitivity()
        return self.__lastSensitivity

    async def setSensitivity(self, newVal: float):
        logger.info(f'Changing sensitivity to {newVal}')
        await self._cobotClient.setSensitivity(newVal)
        self.__lastSensitivity = await self._cobotClient.getSensitivity()

    async def _loop_monitorForceSensor(self):

        checkSensitivityEveryN = 10
        nSinceSensitivityCheck = checkSensitivityEveryN

        checkRawValuesEveryN = 5
        nSinceRawValuesCheck = checkRawValuesEveryN

        while True:
            if not self._cobotConnectedEvent.is_set():
                logger.debug('Waiting for cobot to connect')
                self.__lastMeasuredForce = None
                await self._cobotConnectedEvent.wait()
                continue

            try:
                self.__lastMeasuredForce = await self._cobotClient.getForce()

                if Version('.'.join(str(x) for x in self._cobotClient.controllerVersion)) >= Version('2.2'):
                    nSinceRawValuesCheck += 1
                    if nSinceRawValuesCheck > checkRawValuesEveryN:
                        nSinceRawValuesCheck = 1
                        rawValues = await self._cobotClient.getCoilRawValues()
                        self.__lastRawCoilIDValue = rawValues['id']
                        self.__lastRawForceValue = rawValues['contact']

                nSinceSensitivityCheck += 1
                if nSinceSensitivityCheck > checkSensitivityEveryN:
                    nSinceSensitivityCheck = 1
                    self.__lastSensitivity = await self._cobotClient.getSensitivity()

            except CobotClient.NotConnectedError:
                logger.warning('Cobot not connected, cannot read force')
                self.__lastMeasuredForce = None
                await asyncio.sleep(10./self._monitorMeasuredForceRate)

            except CobotClient.SensorMissingError:
                logger.warning('No force sensor reading available: is coil connected?')
                self.__lastMeasuredForce = None
                await asyncio.sleep(10./self._monitorMeasuredForceRate)
            except CobotClient.HomingNotDoneError:
                logger.warning('Homing not done, cannot read force')
                self.__lastMeasuredForce = None
                await asyncio.sleep(10. / self._monitorMeasuredForceRate)

            await asyncio.sleep(1./self._monitorMeasuredForceRate)

    async def _loop_trackCobotDevicePositions(self):
        """
        Continually poll and update NaviNIBS with the current position of the Cobot joint positions.

        The cobotWorld coordinate system has its origin at the active cart tracker (either left or right, can be determined with GET(BASEI)).

        The location of the base of the arm relative to this can be obtained by GET(BASE, device=COBOT).

        The location of the workspace origin (??) can be obtained by GET(BASE, device=ARM).

        The location of the cobot's idea of the coil can be obtained by GET(POSITION, device=ARM).

        These can then all be converted to neuronav camera world space based on the camera's idea of the
        cart tracker position.

        """

        async def resetPositions():
            for key in (
                'CobotCart',
                'CobortArmBase',
                'CobotWorkspace',
                'CobotCoil',
                'CobotArmJ1',
                'CobotArmJ2',
                'CobotArmJ3',
                'CobotArmJ4',
                'CobotArmJ5',
                'CobotArmJ6',
                'CobotArmEndpointModule'
            ):
                await self._positionsClient.recordNewPosition_async(
                    key=key,
                    position=TimestampedToolPosition(
                        time=time.time(),
                        transf=None
                    )
                )

        while True:
            if not self._positionsClient.isConnected:
                logger.debug('Waiting for positionsClient to connect')
                await resetPositions()
                await asyncio.sleep(1)
                continue

            if not self._cobotConnectedEvent.is_set():
                logger.debug('Waiting for cobot to connect')
                await resetPositions()
                await self._cobotConnectedEvent.wait()
                logger.debug('Done waiting for cobot to connect')
                continue

            # determine which cart tracker is active
            assert self._activeCartTrackerKey is not None
            cartTrackerKey = self._activeCartTrackerKey
            # cartTrackerKey should match key in SessionConfig_Tools

            # Get the cobot's base position
            try:
                cobotBaseToCobotWorldTransform = posAndQuatToTransform(*await self._cobotClient.getBaseToWorldTransform(deviceName='COBOT'))

                await self._positionsClient.recordNewPosition_async(
                    key='CobotCart',
                    position=TimestampedToolPosition(
                        time=time.time(),
                        transf=cobotBaseToCobotWorldTransform,
                        relativeTo=cartTrackerKey
                    )
                )

                await self._positionsClient.recordNewPosition_async(
                    key='CobotArmBase',
                    position=TimestampedToolPosition(
                        time=time.time(),
                        transf=cobotBaseToCobotWorldTransform,
                        relativeTo=cartTrackerKey
                    )
                )

                # Get the workspace base position
                workspaceBaseToCobotWorldTransform = posAndQuatToTransform(*await self._cobotClient.getBaseToWorldTransform(deviceName='ARM'))

                await self._positionsClient.recordNewPosition_async(
                    key='CobotWorkspace',
                    position=TimestampedToolPosition(
                        time=time.time(),
                        transf=workspaceBaseToCobotWorldTransform,
                        relativeTo=cartTrackerKey
                    )
                )

                # Get the cobot's idea of current coil position
                coilTrackerToCobotWorldTransform = posAndQuatToTransform(*await self._cobotClient.getCoilToWorldTransform())

                # convert from Cobot's coil coordinate system to NaviNIBS coordinate system
                coilTrackerToCobotWorldTransform = concatenateTransforms([
                    invertTransform(self._cobotCoilTrackerToNaviNIBSCoilCoordTransf),
                    coilTrackerToCobotWorldTransform])

                await self._positionsClient.recordNewPosition_async(
                    key=self._cobotCoilTrackerKey,
                    position=TimestampedToolPosition(
                        time=time.time(),
                        transf=coilTrackerToCobotWorldTransform,
                        relativeTo=cartTrackerKey
                    )
                )

                # Get the joint positions
                jointPositions = await self._cobotClient.getJointPositions()
                # logger.debug(f'Joint positions: {jointPositions}')

                j1TransfInit = composeTransform(ptr.active_matrix_from_angle(basis=0, angle=np.pi/2),
                                            np.asarray([0, 0, 89.159]))

                j1Transf = concatenateTransforms([
                    composeTransform(ptr.active_matrix_from_angle(basis=1, angle=np.deg2rad(jointPositions[0]))),
                    j1TransfInit])

                await self._positionsClient.recordNewPosition_async(
                    key='CobotArmJ1',
                    position=TimestampedToolPosition(
                        time=time.time(),
                        transf=j1Transf,
                        relativeTo='CobotArmBase'
                    ))

                j2TransfInit = composeTransform(np.eye(3), np.asarray([0, 0, 0]))
                j2Transf = concatenateTransforms([
                    composeTransform(ptr.active_matrix_from_angle(basis=2, angle=np.deg2rad(jointPositions[1])+np.pi)),
                    j2TransfInit])

                await self._positionsClient.recordNewPosition_async(
                    key='CobotArmJ2',
                    position=TimestampedToolPosition(
                        time=time.time(),
                        transf=j2Transf,
                        relativeTo='CobotArmJ1'
                    ))

                j3TransfInit1 = composeTransform(ptr.active_matrix_from_angle(basis=0, angle=0),
                                                np.asarray([-392.25, 0, -4]))
                j3TransfInit2 = composeTransform(np.eye(3), np.asarray([425, 0, 0]))
                j3Transf = concatenateTransforms([
                    j3TransfInit1,
                    composeTransform(ptr.active_matrix_from_angle(basis=2, angle=np.deg2rad(jointPositions[2])+np.pi)),
                    j3TransfInit2
                ])

                await self._positionsClient.recordNewPosition_async(
                    key='CobotArmJ3',
                    position=TimestampedToolPosition(
                        time=time.time(),
                        transf=j3Transf,
                        relativeTo='CobotArmJ2'
                    ))

                j4TransfInit = composeTransform(ptr.active_matrix_from_angle(basis=0, angle=np.pi/2),
                                                np.asarray([0, 0, 109.15]))
                j4Transf = concatenateTransforms([
                    composeTransform(ptr.active_matrix_from_angle(basis=1, angle=np.deg2rad(jointPositions[3]))),
                    j4TransfInit])

                await self._positionsClient.recordNewPosition_async(
                    key='CobotArmJ4',
                    position=TimestampedToolPosition(
                        time=time.time(),
                        transf=j4Transf,
                        relativeTo='CobotArmJ3'
                    ))

                j5TransfInit = composeTransform(ptr.active_matrix_from_angle(basis=0, angle=-np.pi/2),
                                     np.asarray([0, 0, 94.65]))

                j5Transf = concatenateTransforms([
                    composeTransform(ptr.active_matrix_from_angle(basis=1, angle=-np.deg2rad(jointPositions[4]))),
                    j5TransfInit])

                await self._positionsClient.recordNewPosition_async(
                    key='CobotArmJ5',
                    position=TimestampedToolPosition(
                        time=time.time(),
                        transf=j5Transf,
                        relativeTo='CobotArmJ4'
                    ))

                j6TransfInit = composeTransform(ptr.active_matrix_from_angle(basis=0, angle=0),
                                                np.asarray([0, 0, 82.3]))

                j6Transf = concatenateTransforms([
                    composeTransform(ptr.active_matrix_from_angle(basis=2, angle=np.deg2rad(jointPositions[5]))),
                    j6TransfInit])

                await self._positionsClient.recordNewPosition_async(
                    key='CobotArmJ6',
                    position=TimestampedToolPosition(
                        time=time.time(),
                        transf=j6Transf,
                        relativeTo='CobotArmJ5'
                    ))

                await self._positionsClient.recordNewPosition_async(
                    key='CobotArmEndpointModule',
                    position=TimestampedToolPosition(
                        time=time.time(),
                        transf=np.eye(4),
                        relativeTo='CobotArmJ6'
                    ))

                if True:
                    # keep track of recent joint positions and joint position limits

                    armJointPositions = await self._cobotClient.getJointPositions(deviceName='ARM')

                    positionsChanged: bool = False
                    for deviceName, positions in [('COBOT', jointPositions), ('ARM', armJointPositions)]:
                        if deviceName not in self._latestJointPositions or self._latestJointPositions[deviceName] != positions:
                            self._latestJointPositions[deviceName] = positions
                            positionsChanged = True

                    if positionsChanged:
                        self.sigJointPositionsChanged.emit()

                    cobotPosLims = await self._cobotClient.getJointPositionLimits(deviceName='COBOT')

                    armPosLims = await self._cobotClient.getJointPositionLimits(
                        deviceName='ARM',
                    )

                    posLimsChanged: bool = False

                    for prefix, lims in [('COBOT_', cobotPosLims), ('ARM_', armPosLims)]:
                        for key, limsSubset in lims.items():
                            fullKey = prefix + key
                            if fullKey not in self._latestJointPositionLimits or self._latestJointPositionLimits[fullKey] != limsSubset:
                                self._latestJointPositionLimits[fullKey] = limsSubset
                                posLimsChanged = True

                    if posLimsChanged:
                        self.sigJointPositionLimitsChanged.emit()

            except CobotClient.NotConnectedError:
                logger.warning('Cobot not connected, cannot finish updating positions')
                await asyncio.sleep(1)
                continue

            await asyncio.sleep(1/self._trackPositionsRate)

    @property
    def latestJointPositions(self):
        return self._latestJointPositions

    @property
    def latestJointPositionLimits(self):
        return self._latestJointPositionLimits

    async def _loop_alignCoilPoses(self):
        """
        If using separate dedicated coil tracker, continually update estimated transform aligning
        measured coil position to cobot's idea of coil position calculated from cart position and joint angles.
        """

        positionsChangedEvent = asyncio.Event()

        self._positionsClient.sigLatestPositionsChanged.connect(lambda: positionsChangedEvent.set())

        lastWarnedAboutTrackerToToolTransform: float | None = None

        while True:
            await positionsChangedEvent.wait()
            await asyncio.sleep(0.05)  # TODO: add parameter rate limit rather than hardcoding here
            positionsChangedEvent.clear()
            if self._coilTrackerKey is None or self._cobotCoilTrackerKey == self._coilTrackerKey:
                # no automatic updates needed
                continue

            coilTrackerToCameraTransf = self._positionsClient.getLatestTransf(self._coilTrackerKey, None)
            if coilTrackerToCameraTransf is None or self._coilToolToTrackerTransf is None:
                cobotCoilToolToTrackerTransf = None
            else:
                cobotCoilTrackerToCameraTransf = self._positionsClient.getLatestTransf(self._cobotCoilTrackerKey, None)
                if cobotCoilTrackerToCameraTransf is None:
                    cobotCoilToolToTrackerTransf = None
                else:
                    cobotCoilToolToTrackerTransf = concatenateTransforms([
                        self._coilToolToTrackerTransf,
                        coilTrackerToCameraTransf,
                        invertTransform(cobotCoilTrackerToCameraTransf),
                    ])

            if cobotCoilToolToTrackerTransf is None:
                # don't update if no new data
                continue

            maxDistDeviation: float = 10.  # in mm
            maxAngleDeviation: float = 10.  # in degrees

            distDeviation = np.linalg.norm(cobotCoilToolToTrackerTransf[:3,3])
            angleDeviation = np.rad2deg(ptr.axis_angle_from_matrix(cobotCoilToolToTrackerTransf[:3,:3]))[-1]
            if distDeviation > maxDistDeviation or angleDeviation > maxAngleDeviation:
                # don't let situations like user error with selecting wrong TMS coil to cause extreme cobot shifts. Actual error between cobot's idea of the coil and actual position should never be very large.
                warnRateLimit = 10.  # in seconds
                if lastWarnedAboutTrackerToToolTransform is None or \
                        time.time() - lastWarnedAboutTrackerToToolTransform > warnRateLimit:
                    logger.warning(f'coil tracker to cobot coil tool transform is too far from expected value: {cobotCoilToolToTrackerTransf}')
                    lastWarnedAboutTrackerToToolTransform = time.time()
                continue

            if False:
                # immediately update based on this instant's alignment
                self.cobotCoilToolToTrackerTransf = cobotCoilToolToTrackerTransf

            else:
                # do some exponential weighted smoothing of previous alignment and new alignment
                smoothedTransf = self.cobotCoilToolToTrackerTransf
                if smoothedTransf is None:
                    smoothedTransf = np.eye(4)

                currentTransf = cobotCoilToolToTrackerTransf

                # do averaging in quaternion representation
                currentTransf = ptt.pq_from_transform(currentTransf)
                smoothedTransf = ptt.pq_from_transform(smoothedTransf)

                smoothingWeight = 0.95  # TODO: make a parameter and experiment to determine reasonable default
                """
                Values closer to one produce smoother values (slower response to changes); a value of zero immediately changes to the new value.
                """
                assert 0 <= smoothingWeight < 1

                # blend rotation
                smoothedTransf[3:] = ptr.quaternion_slerp(smoothedTransf[3:], currentTransf[3:], 1-smoothingWeight)

                # blend translation
                smoothedTransf[0:3] = smoothingWeight*smoothedTransf[0:3] + (1-smoothingWeight)*currentTransf[0:3]

                self.cobotCoilToolToTrackerTransf = ptt.transform_from_pq(smoothedTransf)

    @property
    def targetIsAccessible(self):
        return self._targetIsAccessible

    @property
    def _targetIsAccessible(self):
        return self.__targetIsAccessible

    @_targetIsAccessible.setter
    def _targetIsAccessible(self, value):
        if self.__targetIsAccessible == value:
            return
        self.__targetIsAccessible = value
        self.sigTargetAccessibleChanged.emit()

    @property
    def airgapOffsetFromContact(self):
        return self._airgapOffsetFromContact

    @airgapOffsetFromContact.setter
    def airgapOffsetFromContact(self, value: float):
        if self._airgapOffsetFromContact == value:
            return

        assert value >= 0, 'Airgap offset must be non-negative'

        self._airgapOffsetFromContact = value
        self.sigAirgapOffsetFromContactChanged.emit()

    @property
    def airgapOffsetFromScalp(self):
        return self._airgapOffsetFromScalp

    @airgapOffsetFromScalp.setter
    def airgapOffsetFromScalp(self, value: float):
        if self._airgapOffsetFromScalp == value:
            return

        assert value >= 0, 'Airgap offset must be non-negative'

        self._airgapOffsetFromScalp = value
        self.sigAirgapOffsetFromScalpChanged.emit()

    @property
    def airgapOffsetFromTarget(self):
        return self._airgapOffsetFromTarget

    @airgapOffsetFromTarget.setter
    def airgapOffsetFromTarget(self, value: float):
        if self._airgapOffsetFromTarget == value:
            return

        self._airgapOffsetFromTarget = value
        self.sigAirgapOffsetFromTargetChanged.emit()

    @property
    def targetZOffsetAtScalp(self) -> float | None:
        if self._targetZOffsetAtScalp is None:
            if self._targetCoilToMRITransf is None:
                return None
            headMesh = self.getHeadMesh_sync()
            if headMesh is None:
                return None
            headPtsInTargetSpace = applyTransform(invertTransform(self._targetCoilToMRITransf), headMesh.points, doCheck=False)
            # assume coil bottom surface is at z=0, and z<0 corresponds to below coil
            # note that this doesn't account for shape or exact position of coil mesh itself
            zDistToCoil = headPtsInTargetSpace[:, 2].max(axis=0)
            self._targetZOffsetAtScalp = zDistToCoil

        return self._targetZOffsetAtScalp

    @property
    def hasCalibratedContactDepthForCurrentTarget(self):
        return self._targetZOffsetAtForceThreshold is not None

    @property
    def realignWhenDistErrorExceeds(self):
        return self._realignWhenDistErrorExceeds

    @realignWhenDistErrorExceeds.setter
    def realignWhenDistErrorExceeds(self, value: float):
        if self._realignWhenDistErrorExceeds == value:
            return
        if value < self._alignedWhenDistErrorUnder:
            logger.warning('realignWhenDistErrorExceeds should be greater than alignedWhenDistErrorUnder')
        self._realignWhenDistErrorExceeds = value
        self.sigRealignThresholdsChanged.emit()

    @property
    def realignWhenZAngleErrorExceeds(self):
        return self._realignWhenZAngleErrorExceeds

    @realignWhenZAngleErrorExceeds.setter
    def realignWhenZAngleErrorExceeds(self, value: float):
        if self._realignWhenZAngleErrorExceeds == value:
            return
        if value < self._alignedWhenZAngleErrorUnder:
            logger.warning('realignWhenZAngleErrorExceeds should be greater than alignedWhenZAngleErrorUnder')
        self._realignWhenZAngleErrorExceeds = value
        self.sigRealignThresholdsChanged.emit()

    @property
    def realignWhenHorizAngleErrorExceeds(self):
        return self._realignWhenHorizAngleErrorExceeds

    @realignWhenHorizAngleErrorExceeds.setter
    def realignWhenHorizAngleErrorExceeds(self, value: float):
        if self._realignWhenHorizAngleErrorExceeds == value:
            return
        if value < self._alignedWhenHorizAngleErrorUnder:
            logger.warning('realignWhenHorizAngleErrorExceeds should be greater than alignedWhenHorizAngleErrorUnder')
        self._realignWhenHorizAngleErrorExceeds = value
        self.sigRealignThresholdsChanged.emit()

    @property
    def moveWhenZDistErrorExceeds(self):
        return self._moveWhenZDistErrorExceeds

    @moveWhenZDistErrorExceeds.setter
    def moveWhenZDistErrorExceeds(self, value: float):
        if self._moveWhenZDistErrorExceeds == value:
            return
        if value < self._doneMovingWhenZDistErrorUnder:
            logger.warning('moveWhenZDistErrorExceeds should be greater than doneMovingWhenZDistErrorUnder')
        self._moveWhenZDistErrorExceeds = value
        self.sigRealignThresholdsChanged.emit()

    @property
    def alignedWhenDistErrorUnder(self):
        return self._alignedWhenDistErrorUnder

    @alignedWhenDistErrorUnder.setter
    def alignedWhenDistErrorUnder(self, value: float):
        if self._alignedWhenDistErrorUnder == value:
            return
        if value > self._realignWhenDistErrorExceeds:
            logger.warning('alignedWhenDistErrorUnder should be less than realignWhenDistErrorExceeds')
        self._alignedWhenDistErrorUnder = value
        self.sigAlignedThresholdsChanged.emit()

    @property
    def alignedWhenZAngleErrorUnder(self):
        return self._alignedWhenZAngleErrorUnder

    @alignedWhenZAngleErrorUnder.setter
    def alignedWhenZAngleErrorUnder(self, value: float):
        if self._alignedWhenZAngleErrorUnder == value:
            return
        if value > self._realignWhenZAngleErrorExceeds:
            logger.warning('alignedWhenZAngleErrorUnder should be less than realignWhenZAngleErrorExceeds')
        self._alignedWhenZAngleErrorUnder = value
        self.sigAlignedThresholdsChanged.emit()

    @property
    def alignedWhenHorizAngleErrorUnder(self):
        return self._alignedWhenHorizAngleErrorUnder

    @alignedWhenHorizAngleErrorUnder.setter
    def alignedWhenHorizAngleErrorUnder(self, value: float):
        if self._alignedWhenHorizAngleErrorUnder == value:
            return
        if value > self._realignWhenHorizAngleErrorExceeds:
            logger.warning('alignedWhenHorizAngleErrorUnder should be less than realignWhenHorizAngleErrorExceeds')
        self._alignedWhenHorizAngleErrorUnder = value
        self.sigAlignedThresholdsChanged.emit()

    @property
    def doneMovingWhenZDistErrorUnder(self):
        return self._doneMovingWhenZDistErrorUnder

    @doneMovingWhenZDistErrorUnder.setter
    def doneMovingWhenZDistErrorUnder(self, value: float):
        if self._doneMovingWhenZDistErrorUnder == value:
            return
        if value > self._moveWhenZDistErrorExceeds:
            logger.warning('doneMovingWhenZDistErrorUnder should be less than moveWhenZDistErrorExceeds')
        self._doneMovingWhenZDistErrorUnder = value
        self.sigAlignedThresholdsChanged.emit()

    # TODO: add getters, setters, and change signals for approximatelyAligned* and almostDoneMoving* thresholds

    @property
    def isApproximatelyAligned(self):
        return self._isApproximatelyAlignedEvent.is_set()

    @isApproximatelyAligned.setter
    def isApproximatelyAligned(self, value: bool):
        if value == self._isApproximatelyAlignedEvent.is_set():
            return
        logger.debug(f'isApproximatelyAligned changed to {value}')
        if value:
            self._isApproximatelyAlignedEvent.set()
        else:
            self._isApproximatelyAlignedEvent.clear()
        self.sigIsApproximatelyAlignedChanged.emit()

    def _getCoilToCobotWorldTransf(self, targetCoilToMRITransf: np.ndarray | None) -> np.ndarray | None:
        if self._subjectTrackerToMRITransf is None \
                or self._subjectTrackerKey is None \
                or targetCoilToMRITransf is None:
            return None

        subjectTrackerToCameraTransf = self._positionsClient.getLatestTransf(self._subjectTrackerKey, None)
        if self._activeCartTrackerKey is None:
            return None
        cobotWorldToCameraTransf = self._positionsClient.getLatestTransf(self._activeCartTrackerKey, None)
        if subjectTrackerToCameraTransf is None or cobotWorldToCameraTransf is None:
            return None

        cobotCoilToolToTrackerTransf = self._cobotCoilToolToTrackerTransf
        if cobotCoilToolToTrackerTransf is None:
            cobotCoilToolToTrackerTransf = np.eye(4)

        coilTrackerToCobotWorldTransf = concatenateTransforms([
            self._cobotCoilTrackerToNaviNIBSCoilCoordTransf,  # difference in coordinate system definitions
            invertTransform(cobotCoilToolToTrackerTransf),  # when using separate coil tracker, this accounts for discrepancy between cobot's estimate of coil pose and more directly measured pose
            targetCoilToMRITransf,  # desired target
            invertTransform(self._subjectTrackerToMRITransf),
            subjectTrackerToCameraTransf,
            invertTransform(cobotWorldToCameraTransf)])

        return coilTrackerToCobotWorldTransf

    def _areTargetsNear(self, coilToMRITransf_A: np.ndarray, coilToMRITransf_B: np.ndarray) -> bool:
        testPts_coilSpace = np.asarray([[0, 0, 0], [0, 0, 1], [0, 1, 0]])
        testPts_coilSpace_AinB = applyTransform([
            coilToMRITransf_A,
            invertTransform(coilToMRITransf_B)
        ], testPts_coilSpace, doCheck=False)

        distBetweenTargets = np.linalg.norm(testPts_coilSpace_AinB[0, :])

        if distBetweenTargets > self._targetChangeDistanceThreshold:
            return False

        targetZVector = Vector(np.diff(testPts_coilSpace[0:2, :], axis=0).squeeze())
        targetZVector_AinB = Vector(np.diff(testPts_coilSpace_AinB[0:2, :], axis=0).squeeze())

        zAngleError = np.rad2deg(targetZVector.angle_between(targetZVector_AinB))

        if zAngleError > self._targetChangeAngleThreshold:
            return False

        horizAngleError = np.rad2deg(np.arctan2(np.diff(testPts_coilSpace_AinB[[0, 2], 0], axis=0),
                                                np.diff(testPts_coilSpace_AinB[[0, 2], 1], axis=0)))

        if abs(horizAngleError) > self._targetChangeAngleThreshold:
            return False

        return True

    async def _loop_monitorTargetAccessibility(self):
        while True:
            if self._subjectTrackerToMRITransf is None \
                    or self._subjectTrackerKey is None \
                    or self._targetCoilToMRITransf is None:
                # don't have all necessary info for aligning to target
                self._targetIsAccessible = None
                self._targetingInfoUpdatedEvent.clear()
                await self._targetingInfoUpdatedEvent.wait()
                continue

            self._targetingInfoUpdatedEvent.clear()
            await asyncWaitWithCancel(
                (asyncio.sleep(1/self._monitorTargetAccessibilityRate),
                 self._targetingInfoUpdatedEvent.wait()),
                return_when=asyncio.FIRST_COMPLETED)

            coilToCobotWorldTransf = self._getCoilToCobotWorldTransf(self.maybeOffsetTargetCoilToMRITransf)

            if coilToCobotWorldTransf is None:
                # probably missing cart/subject tracker pose from camera
                self._targetIsAccessible = None
                continue

            posXYZ, quatWXYZ = transformToPosAndQuat(coilToCobotWorldTransf)

            try:
                isReachable = await self._cobotClient.checkTargetReachable(posXYZ, quatWXYZ)
            except (CobotClient.TooFarFromCurrentPositionError, CobotClient.OutOfReachError) as e:
                isReachable = None
            except CobotClient.NotConnectedError:
                isReachable = None

            self._targetIsAccessible = isReachable

    async def setTargetingInfo(self,
                               targetLabel: str | None = _novalue,
                               targetCoilToMRITransf: np.ndarray | list[float] | None = _novalue):
        if targetLabel is not _novalue:
            self.targetLabel = targetLabel

        if targetCoilToMRITransf is not _novalue:
            self.targetCoilToMRITransf = targetCoilToMRITransf

    async def _loop_simulateForce(self):
        while True:
            await asyncio.sleep(0.1)
            await self._simulatedForceInfoUpdatedEvent.wait()
            if not self._cobotClient.isSimulated:
                continue
            self._simulatedForceInfoUpdatedEvent.clear()
            # make sure we have necessary info for determining force value
            if any(x is None for x in (
                self._subjectTrackerToMRITransf,
                self._subjectTrackerKey,
                self._coilTrackerKey,
                self._headMeshPath,
                self._coilMeshPath,
                self._coilMeshToToolTransf,
                self._coilToolToTrackerTransf,
            )):
                # missing some info for setting force
                # logger.debug('Missing information, cannot (yet) set simulated force')
                if self._lastSetForce is not None:
                    await self._cobotClient.setSimulatedForceValue(0)
                    self._lastSetForce = None
                continue

            subjectTrackerToCameraTransf = self._positionsClient.getLatestTransf(self._subjectTrackerKey, None)
            coilTrackerToCameraTransf = self._positionsClient.getLatestTransf(self._coilTrackerKey, None)

            if subjectTrackerToCameraTransf is None or coilTrackerToCameraTransf is None:
                # don't know exactly where subject is relative to coil
                # could set force to zero here, but may have been caused by temporary camera tracking loss
                # so just leave force as it was
                # logger.debug('Missing subjectTrackerToCameraTransf or coilTrackerToCameraTransf, cannot set simulated force')
                continue

            MRIToCoilToolTransf = concatenateTransforms([
                invertTransform(self._subjectTrackerToMRITransf),
                subjectTrackerToCameraTransf,
                invertTransform(coilTrackerToCameraTransf),
                invertTransform(self._coilToolToTrackerTransf)
            ])

            headMesh = await self.getHeadMesh()
            headPtsInCoilToolSpace = applyTransform(MRIToCoilToolTransf,
                                                    headMesh.points, doCheck=False)
            # assume coil bottom surface is at z=0, and z<0 corresponds to below coil
            # note that this doesn't account for shape or exact position of coil mesh itself
            zDistToCoil = headPtsInCoilToolSpace[:, 2].max(axis=0)

            zDistToCoil += self._simulatedForceOffsetDistance

            # logger.debug(f'zDistToCoil: {zDistToCoil}')

            # positive zDistToCoil indicates coil is contacting / in head

            forceSlope = 1.  # in force units per mm
            forceVal = zDistToCoil * forceSlope
            forceVal = np.round(np.clip(forceVal, 0, 4))

            if forceVal != self._lastSetForce:
                logger.info(f'Setting simulated force to {forceVal}')
                try:
                    await self._cobotClient.setSimulatedForceValue(forceVal)
                except self._cobotClient.SensorMissingError:
                    logger.info('Cannot set simulated force because sensor is missing')
                    await asyncio.sleep(1.)
                else:
                    self._lastSetForce = forceVal

    def _updateState(self, signalKeys: list[str] | None = None):
        prevState = self._state

        logger.debug(f'_updateState: {signalKeys}')

        def matchesSig(sigKey: str):
            return signalKeys is None or sigKey in signalKeys

        if matchesSig('sigConnectedChanged') and not self._cobotClient.isConnected:
            self._cobotConnectedEvent.clear()
            self._changeToState(TargetingState.DISCONNECTED)
            return

        if (matchesSig('sigConnectedChanged') and self._cobotClient.isConnected and not
                (self._cobotClient.isEnabled or self._cobotClient.isPoweredOn or self._cobotClient.isHomed)) or \
                (matchesSig('sigControlIsLockedChanged') and not self._cobotClient.controlIsLocked) or \
                (matchesSig('sigEnabledChanged') and not self._cobotClient.isEnabled) or \
                (matchesSig('sigPoweredChanged') and not self._cobotClient.isPoweredOn) or \
                (matchesSig('sigHomedChanged') and not self._cobotClient.isHomed):
            self._changeToState(TargetingState.UNINITIALIZED)
            return

        if matchesSig('sigInProtectiveStopChanged') and self._cobotClient.isInProtectiveStop:
            self._changeToState(TargetingState.PROTECTIVE_STOPPED)
            return

        elif matchesSig('sigInProtectiveStopChanged') and prevState in (TargetingState.PROTECTIVE_STOPPED,):
            self._changeToState(TargetingState.IDLE)
            return

        if matchesSig('sigFreedrivingChanged') and self._cobotClient.isFreedriving:
            self._changeToState(TargetingState.FREEDRIVING)
            return
        elif matchesSig('sigFreedrivingChanged') and prevState in (TargetingState.FREEDRIVING,):
            self._changeToState(TargetingState.IDLE)
            return

        if matchesSig('sigServoingChanged'):
            if self._cobotClient.isServoing:
                match prevState:
                    case TargetingState.UNALIGNED_SERVOING |\
                            TargetingState.UNALIGNED_CONTACTING |\
                            TargetingState.ALIGNED_SERVOING |\
                            TargetingState.ALIGNED_CONTACTING |\
                            TargetingState.ALIGNING_SERVOING |\
                            TargetingState.ALIGNING_CONTACTING:
                        pass  # no change in state

                    case TargetingState.IDLE |\
                            TargetingState.UNALIGNED_RETRACTING:
                        self._changeToState(TargetingState.UNALIGNED_SERVOING)

                    case TargetingState.ALIGNED_RETRACTED |\
                            TargetingState.ALIGNED_RETRACTING:
                        self._changeToState(TargetingState.ALIGNED_SERVOING)

                    case TargetingState.ALIGNING_RETRACTED |\
                            TargetingState.ALIGNING_RETRACTING:
                        self._changeToState(TargetingState.ALIGNING_SERVOING)

                    case TargetingState.MOVING:
                        self._changeToState(TargetingState.ALIGNING_SERVOING)

                    case TargetingState.MOVED:
                        self._changeToState(TargetingState.ALIGNING_SERVOING)

                    case TargetingState.MOVED_FROZEN:
                        self._changeToState(TargetingState.UNALIGNED_SERVOING)

                    case _:
                        logger.warning(f'Unexpected started servoing from state: {prevState.name}')
                        pass  # TODO: maybe change to UNALIGNED_SERVOING here

            elif self._cobotClient.isRetracting:
                # TODO: check whether isServoing is also true while retracting; if so, need to move this condition inside previous condition
                match prevState:
                    case TargetingState.UNALIGNED_RETRACTING |\
                            TargetingState.ALIGNED_RETRACTING |\
                            TargetingState.ALIGNING_RETRACTING:
                        pass  # no change in state

                    case TargetingState.UNALIGNED_SERVOING |\
                            TargetingState.UNALIGNED_CONTACTING:
                        self._changeToState(TargetingState.UNALIGNED_RETRACTING)

                    case TargetingState.ALIGNED_SERVOING |\
                            TargetingState.ALIGNED_CONTACTING:
                        self._changeToState(TargetingState.ALIGNED_RETRACTING)

                    case TargetingState.ALIGNING_SERVOING |\
                            TargetingState.ALIGNING_CONTACTING:
                        self._changeToState(TargetingState.ALIGNING_RETRACTING)

                    case TargetingState.MOVING:
                        self._changeToState(TargetingState.ALIGNING_RETRACTING)

                    case TargetingState.MOVED:
                        self._changeToState(TargetingState.ALIGNING_RETRACTING)

                    case TargetingState.MOVED_FROZEN:
                        self._changeToState(TargetingState.UNALIGNED_RETRACTING)

                    case _:
                        logger.warning(f'Unexpected started retracting from state: {prevState}')
                        pass  # TODO: maybe change to UNALIGNED_RETRACTING here

            else:
                # is not servoing and is not retracting
                pass  # changes from retracting -> retracted should be handled by _waitForRetractedThenUpdateState

        # TODO: maybe change to ALIGNING_RETRACTED/RETRACTING while moving to park or welcome positions

        if prevState in (TargetingState.DISCONNECTED, TargetingState.UNINITIALIZED):
            if self._cobotClient.sessionHasStarted and \
                    self._cobotClient.isEnabled and \
                    self._cobotClient.controlIsLocked and \
                    self._cobotClient.isPoweredOn and \
                    self._cobotClient.isHomed:
                self._changeToState(TargetingState.IDLE)
            else:
                self._changeToState(TargetingState.UNINITIALIZED)
            return

    async def startTrackingTarget(self):
        assert self.targetIsAccessible  # TODO: add support for generating intermediate targets at this point if not accessible
        prevState = self._state
        match prevState:
            case TargetingState.ALIGNED_RETRACTED |\
                 TargetingState.ALIGNING_RETRACTED |\
                 TargetingState.IDLE:
                nextState = TargetingState.ALIGNING_RETRACTED

            case TargetingState.ALIGNED_SERVOING |\
                    TargetingState.ALIGNING_SERVOING |\
                    TargetingState.UNALIGNED_SERVOING:
                nextState = TargetingState.ALIGNING_SERVOING

            case TargetingState.ALIGNED_CONTACTING |\
                    TargetingState.ALIGNING_CONTACTING |\
                    TargetingState.UNALIGNED_CONTACTING:
                nextState = TargetingState.ALIGNING_CONTACTING

            case TargetingState.ALIGNED_RETRACTING |\
                    TargetingState.ALIGNING_RETRACTING |\
                    TargetingState.UNALIGNED_RETRACTING:
                nextState = TargetingState.ALIGNING_RETRACTING

            case TargetingState.MOVING |\
                    TargetingState.MOVED:
                if not self._isTryingToContact:
                    if True:
                        # for stopContact to work correctly (i.e. send a ICoilRetracted message on completion), we actually need to briefly turn on contact before stopping contact here
                        await self._cobotClient.startContact()
                    await self._cobotClient.stopContact()
                    nextState = TargetingState.ALIGNING_RETRACTING
                else:
                    # note: this will start moving directly to next target;
                    # caller should make sure this will not cause problems
                    nextState = TargetingState.MOVING

            case TargetingState.MOVED_FROZEN:
                # no guarantee that the target is still nearby, so don't allow tracking
                # while in this state
                raise RuntimeError(f'Cannot start tracking target from state {prevState}')

            case TargetingState.FREEDRIVING:
                await self._cobotClient.stopContact()
                nextState = TargetingState.ALIGNING_RETRACTING  # TODO: double check this produces reasonable behavior

            case _:
                raise RuntimeError(f'Cannot start tracking target from state {prevState}')

        self._changeToState(nextState)

    async def stopTrackingTarget(self):
        self.stopTrackingTarget_sync()

    def stopTrackingTarget_sync(self):
        prevState = self._state
        match prevState:
            case TargetingState.ALIGNED_RETRACTED |\
                    TargetingState.ALIGNING_RETRACTED |\
                    TargetingState.IDLE:
                nextState = TargetingState.IDLE

            case TargetingState.ALIGNED_SERVOING |\
                    TargetingState.ALIGNING_SERVOING |\
                    TargetingState.UNALIGNED_SERVOING:
                nextState = TargetingState.UNALIGNED_SERVOING

            case TargetingState.ALIGNED_CONTACTING |\
                    TargetingState.ALIGNING_CONTACTING |\
                    TargetingState.UNALIGNED_CONTACTING:
                nextState = TargetingState.UNALIGNED_CONTACTING

            case TargetingState.ALIGNED_RETRACTING |\
                    TargetingState.ALIGNING_RETRACTING |\
                    TargetingState.UNALIGNED_RETRACTING:
                nextState = TargetingState.UNALIGNED_RETRACTING

            case TargetingState.MOVING |\
                    TargetingState.MOVED:
                nextState = TargetingState.MOVED_FROZEN

            case TargetingState.DISCONNECTED |\
                    TargetingState.UNINITIALIZED |\
                    TargetingState.FREEDRIVING:
                nextState = prevState

            case _:
                raise RuntimeError(f'Cannot stop tracking target from state {prevState}')

        self._changeToState(nextState)

    def startFreedriving(self):
        prevState = self._state

        match prevState:
            case TargetingState.DISCONNECTED |\
                    TargetingState.UNINITIALIZED:
                raise RuntimeError(f'Cannot start freedriving from state {prevState}')
            case _:
                nextState = TargetingState.FREEDRIVING

        self._changeToState(nextState)

    def stopFreedriving(self):
        prevState = self._state

        match prevState:
            case TargetingState.FREEDRIVING:
                nextState = TargetingState.IDLE
            case _:
                if self.cobotClient.isFreedriving:
                    logger.warning('State machine not in FREEDRIVING, but cobot is in freedriving mode. Stopping freedriving.')
                    asyncio.create_task(asyncTryAndLogExceptionOnError(self.cobotClient.stopFreedrive))
                    if prevState in (
                        TargetingState.UNINITIALIZED,
                        TargetingState.IDLE,
                    ):
                        nextState = prevState
                    else:
                        nextState = TargetingState.IDLE
                else:
                    raise RuntimeError(f'Cannot stop freedriving from state {prevState}')

        self._changeToState(nextState)

    async def startContact(self):
        logger.debug('startContact')

        match self.contactMode:
            case ContactMode.DEFAULT:
                self._isTryingToContact = True
                self.sigTryingToContactChanged.emit()
                await self._cobotClient.startContact()

            case ContactMode.CONTACT_THEN_FREEZE:
                await self.startContactAndFreeze()

            case ContactMode.AIRGAPPED_FROM_CONTACT:
                await self.startAirgappingFromContact()

            case ContactMode.AIRGAPPED_FROM_SCALP:
                await self.startAirgappingFromScalp()

            case ContactMode.OFFSET_FROM_TARGET:
                await self.startAirgappingFromTarget()

            case _:
                raise NotImplementedError

    async def _reportStartingContact(self):
        self._isTryingToContact = True
        self.sigTryingToContactChanged.emit()

    async def stopContact(self):
        logger.debug('stopContact')
        self._isTryingToContact = False
        self.sigTryingToContactChanged.emit()
        match self._state:
            case TargetingState.ALIGNED_CONTACTING | \
                    TargetingState.ALIGNED_SERVOING | \
                    TargetingState.ALIGNING_CONTACTING |\
                    TargetingState.ALIGNING_SERVOING |\
                    TargetingState.UNALIGNED_CONTACTING |\
                    TargetingState.UNALIGNED_SERVOING:
                await self._cobotClient.stopContact()

            case TargetingState.ALIGNED_RETRACTING |\
                    TargetingState.ALIGNING_RETRACTING |\
                    TargetingState.UNALIGNED_RETRACTING:
                pass  # do nothing, already retracting

            case TargetingState.MOVED_FROZEN:
                if True:
                    # for stopContact to work correctly (i.e. send a ICoilRetracted message on completion), we actually need to briefly turn on contact before stopping contact here
                    await self._cobotClient.startContact()
                await self._cobotClient.stopContact()
                self._changeToState(TargetingState.UNALIGNED_RETRACTING)

            case TargetingState.MOVING |\
                    TargetingState.MOVED:
                await self.startTrackingTarget()  # this will handle initiating retract

            case _:
                raise RuntimeError(f'Unexpected request to stop contact from state {self._state}')

    def _changeToState(self, nextState: TargetingState):
        prevState = self._state

        if nextState == prevState:
            return

        logger.debug(f'_changeToState: {prevState.name} -> {nextState.name}')

        match prevState:
            case TargetingState.DISCONNECTED:
                if False:
                    assert nextState == TargetingState.UNINITIALIZED
                else:
                    assert nextState in (
                        TargetingState.UNINITIALIZED,
                        TargetingState.IDLE,
                        TargetingState.PROTECTIVE_STOPPED)

            case TargetingState.UNINITIALIZED:
                assert nextState in (TargetingState.IDLE, TargetingState.DISCONNECTED, TargetingState.PROTECTIVE_STOPPED)

            case _:
                pass

        match nextState:
            case TargetingState.DISCONNECTED:
                pass  # aside from prevState checks above, prevState can be any

            case TargetingState.UNINITIALIZED:
                pass  # aside from prevState checks above, prevState can be any

            case TargetingState.FREEDRIVING:
                pass  # aside from prevState checks above, prevState can be any
                # TODO: maybe allow directly transitioning from uninitialized to FREEDRIVING

            case TargetingState.PROTECTIVE_STOPPED:
                pass  # prevstate can be any

            case TargetingState.IDLE:
                assert prevState in (
                    TargetingState.DISCONNECTED,
                    TargetingState.UNINITIALIZED,
                    TargetingState.UNALIGNED_RETRACTING,
                    TargetingState.PROTECTIVE_STOPPED,
                    TargetingState.FREEDRIVING,
                    TargetingState.ALIGNED_RETRACTED,
                    TargetingState.ALIGNING_RETRACTED,
                )

            case TargetingState.UNALIGNED_SERVOING:
                assert prevState in (TargetingState.IDLE,
                                     TargetingState.UNALIGNED_RETRACTING,
                                     TargetingState.ALIGNED_SERVOING,
                                     TargetingState.ALIGNING_SERVOING,
                                     TargetingState.MOVED_FROZEN)

            case TargetingState.UNALIGNED_CONTACTING:
                assert prevState in (TargetingState.UNALIGNED_SERVOING,
                                     TargetingState.ALIGNED_CONTACTING,
                                     TargetingState.ALIGNING_CONTACTING)

            case TargetingState.UNALIGNED_RETRACTING:
                assert prevState in (
                    TargetingState.UNALIGNED_CONTACTING,
                    TargetingState.UNALIGNED_SERVOING,
                    TargetingState.ALIGNED_SERVOING,
                    TargetingState.ALIGNED_CONTACTING,
                    TargetingState.ALIGNED_RETRACTING,
                    TargetingState.ALIGNING_SERVOING,
                    TargetingState.ALIGNING_CONTACTING,
                    TargetingState.ALIGNING_RETRACTING,
                    TargetingState.MOVING,
                    TargetingState.MOVED,
                    TargetingState.MOVED_FROZEN,
                )

            case TargetingState.ALIGNED_RETRACTED:
                assert prevState in (
                    TargetingState.ALIGNING_RETRACTED,
                    TargetingState.ALIGNED_RETRACTING,
                )

            case TargetingState.ALIGNED_SERVOING:
                assert prevState in (
                    TargetingState.ALIGNED_RETRACTED,
                    TargetingState.ALIGNED_RETRACTING,
                    TargetingState.ALIGNING_SERVOING
                )

            case TargetingState.ALIGNED_CONTACTING:
                assert prevState in (
                    TargetingState.ALIGNED_SERVOING,
                    TargetingState.ALIGNING_CONTACTING,
                )

            case TargetingState.ALIGNED_RETRACTING:
                assert prevState in (
                    TargetingState.ALIGNED_SERVOING,
                    TargetingState.ALIGNED_CONTACTING,
                    TargetingState.ALIGNING_RETRACTING,
                    TargetingState.UNALIGNED_RETRACTING,
                )

            case TargetingState.ALIGNING_RETRACTED:
                assert prevState in (
                    TargetingState.IDLE,
                    TargetingState.ALIGNED_RETRACTED,
                    TargetingState.ALIGNING_RETRACTED,
                    TargetingState.ALIGNING_RETRACTING,
                )

            case TargetingState.ALIGNING_SERVOING:
                assert prevState in (
                    TargetingState.ALIGNING_RETRACTED,
                    TargetingState.ALIGNING_RETRACTING,
                    TargetingState.ALIGNING_SERVOING,
                    TargetingState.ALIGNED_SERVOING,
                    TargetingState.UNALIGNED_SERVOING,
                    TargetingState.MOVING,
                    TargetingState.MOVED
                )

            case TargetingState.ALIGNING_CONTACTING:
                assert prevState in (
                    TargetingState.ALIGNING_SERVOING,
                    TargetingState.ALIGNED_CONTACTING,
                    TargetingState.UNALIGNED_CONTACTING,
                )

            case TargetingState.ALIGNING_RETRACTING:
                assert prevState in (
                    TargetingState.ALIGNING_SERVOING,
                    TargetingState.ALIGNING_CONTACTING,
                    TargetingState.ALIGNED_RETRACTING,
                    TargetingState.UNALIGNED_RETRACTING,
                    TargetingState.MOVED,
                    TargetingState.MOVING,
                )

            case TargetingState.MOVING:
                if True:
                    # if already servoing, MOVE does not work as expected (depth is ignored). So make sure we're not servoing or retracting before entering this state
                    # in the future, may be able to find a command that stops servoing but does not retract, in which case
                    # this could be relaxed
                    assert prevState not in (
                        TargetingState.ALIGNED_SERVOING,
                        TargetingState.ALIGNED_CONTACTING,
                        TargetingState.ALIGNED_RETRACTING,
                        TargetingState.ALIGNING_SERVOING,
                        TargetingState.ALIGNING_CONTACTING,
                        TargetingState.ALIGNING_RETRACTING,
                        TargetingState.UNALIGNED_SERVOING,
                        TargetingState.UNALIGNED_CONTACTING,
                    )
                pass  # TODO: consider whether to further restrict which prevStates can transition into MOVING

            case TargetingState.MOVED:
                assert prevState in (
                    TargetingState.MOVING,
                )

            case TargetingState.MOVED_FROZEN:
                assert prevState in (
                    TargetingState.MOVING,
                    TargetingState.MOVED,
                )

            case _:
                raise NotImplementedError(f'Unhandled state: {nextState.name}')

        logger.info(f'Changing state from {prevState.name} to {nextState.name}')
        self._state = nextState
        self.stateChangedEvent.set()
        self.sigStateChanged.emit()
        # logger.debug('sigStateChanged emitted')

    async def _waitForStableContact(self, minContactTimeForStability: float | None = None):

        if minContactTimeForStability is None:
            minContactTimeForStability = self._minContactTimeForStability

        lostContactEvent = asyncio.Event()

        def _onContactChanged():
            if not self._cobotClient.isInContact:
                lostContactEvent.set()

        logger.info('Waiting for stable contact')

        while True:
            if not self.cobotClient.isInContact:
                await self.cobotClient.contactEstablishedEvent.wait()

            lostContactEvent.clear()
            with self.cobotClient.sigContactChanged.connected(_onContactChanged):
                try:
                    await asyncio.wait_for(lostContactEvent.wait(), minContactTimeForStability)
                except asyncio.TimeoutError:
                    logger.info('Achieved stable contact')
                    return

    async def _waitForStableContactThenUpdateState(self):
        await self._waitForStableContact()
        match self._state:
            case TargetingState.UNALIGNED_SERVOING:
                nextState = TargetingState.UNALIGNED_CONTACTING
            case TargetingState.ALIGNED_SERVOING:
                nextState = TargetingState.ALIGNED_CONTACTING
            case TargetingState.ALIGNING_SERVOING:
                nextState = TargetingState.ALIGNING_CONTACTING
            case _:
                return  # don't change state
        self._changeToState(nextState)

    async def _waitForRetractedThenUpdateState(self):
        await self.cobotClient.coilRetractedEvent.wait()
        match self._state:
            case TargetingState.UNALIGNED_RETRACTING:
                nextState = TargetingState.IDLE
            case TargetingState.ALIGNED_RETRACTING:
                nextState = TargetingState.ALIGNED_RETRACTED
            case TargetingState.ALIGNING_RETRACTING:
                nextState = TargetingState.ALIGNING_RETRACTED
            case _:
                return  # don't change state
        self._changeToState(nextState)

    async def calculateAlignmentError(self, targetCoilToMRITransf: np.ndarray) -> tuple[float, float, float, float]:
        """
        Returns tuple of errors (horiz_dist_mm, z_dist_mm, horiz_angle_deg, z_angle_deg) between specified transform and current transform

        Note that z_dist_mm and horiz_angle_deg are signed.

        Raises MissingInformationError if cannot compute errors due to missing information.
        """

        if any(x is None for x in (
            self._coilTrackerKey,
            self._subjectTrackerKey
        )):
            raise self.MissingInformationError('Cannot compute alignment error without tracker keys')

        subjectTrackerToCameraTransf = self._positionsClient.getLatestTransf(self._subjectTrackerKey, None)
        coilTrackerToCameraTransf = self._positionsClient.getLatestTransf(self._coilTrackerKey, None)

        if any(x is None for x in (
            subjectTrackerToCameraTransf,
            coilTrackerToCameraTransf
        )):
            raise self.MissingInformationError('Cannot compute alignment error without latest tracker transforms')

        targetCoilToCurrentCoilToolTransf = concatenateTransforms([
            targetCoilToMRITransf,
            invertTransform(self._subjectTrackerToMRITransf),
            subjectTrackerToCameraTransf,
            invertTransform(coilTrackerToCameraTransf),
            invertTransform(self._coilToolToTrackerTransf)
        ])

        testPts_targetSpace = np.asarray([[0, 0, 0], [0, 0, 1], [0, 1, 0]])

        testPts_currentCoilSpace = applyTransform(targetCoilToCurrentCoilToolTransf, testPts_targetSpace, doCheck=False)

        horizDistError = np.linalg.norm(testPts_currentCoilSpace[0, :2])
        zDistError = -testPts_currentCoilSpace[0, 2]

        targetZVector = Vector(np.diff(testPts_targetSpace[0:2, :], axis=0).squeeze())
        currentZVector = Vector(np.diff(testPts_currentCoilSpace[0:2, :], axis=0).squeeze())

        zAngleError = np.rad2deg(targetZVector.angle_between(currentZVector))

        horizAngleError = np.rad2deg(np.arctan2(np.diff(testPts_currentCoilSpace[[0, 2], 0], axis=0).squeeze(),
                                                np.diff(testPts_currentCoilSpace[[0, 2], 1], axis=0).squeeze()))

        logger.debug(f'horizDistError: {horizDistError} zDistError: {zDistError} horizAngleError: {horizAngleError} zAngleError: {zAngleError}')

        return horizDistError, zDistError, horizAngleError, zAngleError

    async def _waitForAlignedThenUpdateState(self):
        while True:
            logger.debug('_waitForAlignedThenUpdateState')
            try:
                horizDistError, zDistError, horizAngleError, zAngleError = await self.calculateAlignmentError(self._targetCoilToMRITransf)
            except self.MissingInformationError:
                await asyncio.sleep(0.1)  # TODO: set up timeout if missing info for too long
                continue

            if horizDistError > self._approximatelyAlignedWhenDistErrorUnder or \
                    abs(horizAngleError) > self._approximatelyAlignedWhenHorizAngleErrorUnder or \
                    zAngleError > self._approximatelyAlignedWhenZAngleErrorUnder:
                self.isApproximatelyAligned = False
            else:
                self.isApproximatelyAligned = True

            if horizDistError > self._alignedWhenDistErrorUnder or \
                    abs(horizAngleError) > self._alignedWhenHorizAngleErrorUnder or \
                    zAngleError > self._alignedWhenZAngleErrorUnder:
                # still misaligned

                # update target
                try:
                    await self._startAligningToTargetWithAutoZOffset(self._targetCoilToMRITransf)
                except self.MissingInformationError:
                    pass  # TODO: set up timeout if missing info for too long
                except (CobotClient.OutOfReachError, CobotClient.JointOutOfRangeError):
                    pass  # TODO: set up timeout if cannot reach for too long
                except CobotClient.TooFarFromCurrentPositionError:
                    # TODO: maybe try an intermediate target
                    pass  # TODO: set up timeout if too far from current position for too long
                # TODO: maybe further rate limit how quickly new targets are sent here
                await asyncio.sleep(0.1)  # TODO: make this a configurable poll rate
                continue
            else:
                # aligned
                # TODO: maybe wait for stability of alignment before considering fully aligned

                # send one last target to update for any small offsets
                try:
                    await self._startAligningToTargetWithAutoZOffset(self._targetCoilToMRITransf)
                except self.MissingInformationError:
                    pass
                except (CobotClient.OutOfReachError, CobotClient.JointOutOfRangeError):
                    pass
                except CobotClient.TooFarFromCurrentPositionError:
                    pass
                break

        match self._state:
            case TargetingState.ALIGNING_SERVOING:
                nextState = TargetingState.ALIGNED_SERVOING
            case TargetingState.ALIGNING_CONTACTING:
                nextState = TargetingState.ALIGNED_CONTACTING
            case TargetingState.ALIGNING_RETRACTING:
                nextState = TargetingState.ALIGNED_RETRACTING
            case TargetingState.ALIGNING_RETRACTED:
                nextState = TargetingState.ALIGNED_RETRACTED
            case _:
                return  # don't change state
        self._changeToState(nextState)

    async def _waitForMisalignedThenUpdateState(self):
        while True:
            try:
                horizDistError, zDistError, horizAngleError, zAngleError = await self.calculateAlignmentError(self._targetCoilToMRITransf)
            except self.MissingInformationError:
                # TODO: timeout at some point and revert state to idle (?) if we can't verify alignment for too long
                await asyncio.sleep(0.1)
                continue

            if horizDistError > self._approximatelyAlignedWhenDistErrorUnder or \
                    abs(horizAngleError) > self._approximatelyAlignedWhenHorizAngleErrorUnder or \
                    zAngleError > self._approximatelyAlignedWhenZAngleErrorUnder:
                self.isApproximatelyAligned = False
            else:
                self.isApproximatelyAligned = True

            if horizDistError <= self._realignWhenDistErrorExceeds and \
                    abs(horizAngleError) <= self._realignWhenHorizAngleErrorExceeds and \
                    zAngleError <= self._realignWhenZAngleErrorExceeds:
                # still aligned
                await asyncio.sleep(0.1)  # TODO: make this a configurable poll rate
                continue
            else:
                # misaligned
                break

        match self._state:
            case TargetingState.ALIGNED_SERVOING:
                nextState = TargetingState.ALIGNING_SERVOING
            case TargetingState.ALIGNED_CONTACTING:
                nextState = TargetingState.ALIGNING_CONTACTING
            case TargetingState.ALIGNED_RETRACTING:
                nextState = TargetingState.ALIGNING_RETRACTING
            case TargetingState.ALIGNED_RETRACTED:
                nextState = TargetingState.ALIGNING_RETRACTED
            case _:
                return  # don't change state
        self._changeToState(nextState)

    async def _waitForMovedThenUpdateState(self):
        while True:
            try:
                horizDistError, zDistError, horizAngleError, zAngleError = await self.calculateAlignmentError(self.maybeOffsetTargetCoilToMRITransf)
            except self.MissingInformationError:
                # TODO: timeout at some point and revert state to idle (?) if we can't verify alignment for too long
                await asyncio.sleep(0.1)
                continue

            if horizDistError > self._approximatelyAlignedWhenDistErrorUnder or \
                    abs(horizAngleError) > self._approximatelyAlignedWhenHorizAngleErrorUnder or \
                    zAngleError > self._approximatelyAlignedWhenZAngleErrorUnder or \
                    abs(zDistError) > self._almostDoneMovingWhenZDistErrorUnder:  # TODO: consider not including zDistError in this check depending on how isApproximatelyAligned needs to be used when moving
                self.isApproximatelyAligned = False
            else:
                self.isApproximatelyAligned = True

            if horizDistError > self._alignedWhenDistErrorUnder or \
                    abs(horizAngleError) > self._alignedWhenHorizAngleErrorUnder or \
                    zAngleError > self._alignedWhenZAngleErrorUnder or \
                    abs(zDistError) > self._moveWhenZDistErrorExceeds:
                # still need to move

                # update target
                try:
                    await self._startMovingToTarget(self.maybeOffsetTargetCoilToMRITransf)
                except self.MissingInformationError:
                    pass  # TODO: set up timeout if missing info for too long
                except (CobotClient.OutOfReachError, CobotClient.JointOutOfRangeError):
                    pass  # TODO: set up timeout if cannot reach for too long
                except CobotClient.TooFarFromCurrentPositionError:
                    # TODO: maybe try an intermediate target
                    pass  # TODO: set up timeout if too far from current position for too long
                # TODO: maybe further rate limit how quickly new targets are sent here
                await asyncio.sleep(0.1)  # TODO: make this a configurable poll rate
                continue
            else:
                # done moving
                # TODO: maybe wait for stability of alignment before considering fully aligned

                # send one last target to update for any small offsets
                try:
                    await self._startMovingToTarget(self.maybeOffsetTargetCoilToMRITransf)
                except self.MissingInformationError:
                    pass
                except (CobotClient.OutOfReachError, CobotClient.JointOutOfRangeError):
                    pass
                except CobotClient.TooFarFromCurrentPositionError:
                    pass
                break

        match self._state:
            case TargetingState.MOVING:
                nextState = TargetingState.MOVED
            case _:
                return  # don't change state
        self._changeToState(nextState)

    async def _waitForNeedToMoveThenUpdateState(self):
        while True:
            try:
                horizDistError, zDistError, horizAngleError, zAngleError = await self.calculateAlignmentError(self.maybeOffsetTargetCoilToMRITransf)
            except self.MissingInformationError:
                # TODO: timeout at some point and revert state to idle (?) if we can't verify alignment for too long
                await asyncio.sleep(0.1)
                continue

            if horizDistError > self._approximatelyAlignedWhenDistErrorUnder or \
                    abs(horizAngleError) > self._approximatelyAlignedWhenHorizAngleErrorUnder or \
                    zAngleError > self._approximatelyAlignedWhenZAngleErrorUnder or \
                    abs(zDistError) > self._almostDoneMovingWhenZDistErrorUnder:  # TODO: consider not including zDistError in this check depending on how isApproximatelyAligned needs to be used when moving
                self.isApproximatelyAligned = False
            else:
                self.isApproximatelyAligned = True

            if horizDistError <= self._realignWhenDistErrorExceeds and \
                    abs(horizAngleError) <= self._realignWhenHorizAngleErrorExceeds and \
                    zAngleError <= self._realignWhenZAngleErrorExceeds and \
                    abs(zDistError) <= self._moveWhenZDistErrorExceeds:
                # still aligned
                await asyncio.sleep(0.1)  # TODO: make this a configurable poll rate
                continue
            else:
                # need to move
                break

        match self._state:
            case TargetingState.MOVED:
                nextState = TargetingState.MOVING
            case _:
                return  # don't change state
        self._changeToState(nextState)

    async def _startAligningToTargetWithAutoZOffset(self, targetCoilToMRITransf: np.ndarray):
        """
        Aligns to target coil, but adjusted for current z offset to correct for Cobot z axis misalignment.

        Internal method only, to be called by state machine code

        Raises MissingInformationError if cannot compute errors due to missing information.

        Raises CobotClient.OutOfReachError or CobotClient.JointOutOfRangeError if adjusted target is inaccessible.
        """

        # logger.debug(f'coilToMRITransf before offset: {targetCoilToMRITransf}')

        horizDistError, zDistError, horizAngleError, zAngleError = await self.calculateAlignmentError(targetCoilToMRITransf)

        extraTransf = np.eye(4)
        extraTransf[2, 3] = zDistError

        offsetTargetCoilToMRITransf = concatenateTransforms([extraTransf, targetCoilToMRITransf])

        # logger.debug(f'coilToMRITransf after offset: {offsetTargetCoilToMRITransf}')

        assert self._state in (
            TargetingState.ALIGNING_SERVOING,
            TargetingState.ALIGNING_CONTACTING,
            TargetingState.ALIGNING_RETRACTING,
            TargetingState.ALIGNING_RETRACTED,
        )  # caller should have set state correctly before this

        coilToCobotWorldTransf = self._getCoilToCobotWorldTransf(offsetTargetCoilToMRITransf)

        if coilToCobotWorldTransf is None:
            raise self.MissingInformationError('Cannot compute coilToCobotWorldTransf')

        if True:
            # project offset back down toward scalp along cobot's servo axis (i.e. at different, offset location) so that we don't run into issues with target "out of reach" just due to z offset
            workspaceBaseToCobotWorldTransform = posAndQuatToTransform(
                *await self._cobotClient.getBaseToWorldTransform(deviceName='ARM'))  # TODO: cache this instead of requesting each time (it should rarely change)

            coilToCobotWorkspaceTransf = concatenateTransforms([
                coilToCobotWorldTransf,
                invertTransform(workspaceBaseToCobotWorldTransform)])

            # logger.debug(f'coilToCobotWorkspaceTransf before modifying offset: {coilToCobotWorkspaceTransf}')

            servoAxis = coilToCobotWorkspaceTransf[:3, 3].copy()
            servoAxis /= np.linalg.norm(servoAxis)

            # logger.debug(f'Servo axis: {servoAxis}')

            extraTransf = np.eye(4)
            extraTransf[:3, 3] = -zDistError * servoAxis

            # logger.debug(f'extraTransf: {extraTransf}')

            modifiedOffsetCoilToCobotWorkspaceTransf = concatenateTransforms([
                coilToCobotWorkspaceTransf,
                extraTransf
            ])

            # logger.debug(f'coilToCobotWorkspaceTransf after modifying offset: {modifiedOffsetCoilToCobotWorkspaceTransf}')

            modifiedOffsetCoilToCobotWorldTransf = concatenateTransforms([
                modifiedOffsetCoilToCobotWorkspaceTransf,
                workspaceBaseToCobotWorldTransform,
            ])

            coilToCobotWorldTransf = modifiedOffsetCoilToCobotWorldTransf

        # logger.debug(f'coilToCobotWorldTransf: {coilToCobotWorldTransf}')

        posXYZ, quatWXYZ = transformToPosAndQuat(coilToCobotWorldTransf)

        try:
            await self._cobotClient.startAligningToTarget(posXYZ, quatWXYZ)
        except self._cobotClient.OutOfReachError as e:
            logger.warning('Adjusted target is out of reach')
            raise e
        except self._cobotClient.JointOutOfRangeError as e:
            logger.warning('Adjusted target is out of joint range')
            raise e
        except self._cobotClient.TooFarFromCurrentPositionError as e:
            logger.warning('Adjusted target is too far from current position')
            raise e

    async def _startMovingToTarget(self, targetCoilToMRITransf: np.ndarray):
        """
        NOTE: this allows directly moving to specified target location with fewer safeguards than typical align + servo process. Caller should validate that target is reachable before calling this method.
        """

        assert self._state in (
            TargetingState.MOVING,
        )  # caller should have set state correctly before this

        coilToCobotWorldTransf = self._getCoilToCobotWorldTransf(targetCoilToMRITransf)

        if coilToCobotWorldTransf is None:
            raise self.MissingInformationError('Cannot compute coilToCobotWorldTransf')

        posXYZ, quatWXYZ = transformToPosAndQuat(coilToCobotWorldTransf)

        try:
            await self._cobotClient.startMovingToTarget(posXYZ=posXYZ, quatWXYZ=quatWXYZ)
        except self._cobotClient.OutOfReachError as e:
            logger.warning('Target is out of reach')
            raise e
        except self._cobotClient.JointOutOfRangeError as e:
            logger.warning('Target is out of joint range')
            raise e

    async def _loop_stateMachine(self):

        waitingForContactTask: asyncio.Task | None = None  # used to count contact "stable" even when moving between aligning/aligned/unaligned servoing states
        # TODO: add some check for exiting "contacting" state if lost contact for too long during CONTACTED states
        waitingForRetractedTask: asyncio.Task | None = None
        waitingForAlignedTask: asyncio.Task | None = None
        waitingForMisalignedTask: asyncio.Task | None = None
        waitingForMovedTask: asyncio.Task | None = None
        waitingForNeedToMoveTask: asyncio.Task | None = None

        while True:
            logger.debug('_loop_stateMachine')

            self.stateChangedEvent.clear()

            if self._state in (
                TargetingState.UNALIGNED_SERVOING,
                TargetingState.ALIGNED_SERVOING,
                TargetingState.ALIGNING_SERVOING,
            ):
                if waitingForContactTask is None or waitingForContactTask.done():
                    logger.debug('Starting waitingForContactTask')
                    waitingForContactTask = asyncio.create_task(
                        asyncTryAndLogExceptionOnError(self._waitForStableContactThenUpdateState))
            else:
                if waitingForContactTask is not None:
                    logger.debug('Canceling waitingForContactTask')
                    waitingForContactTask.cancel()
                    waitingForContactTask = None

            if self._state in (
                TargetingState.UNALIGNED_RETRACTING,
                TargetingState.ALIGNED_RETRACTING,
                TargetingState.ALIGNING_RETRACTING,
            ):
                if waitingForRetractedTask is None or waitingForRetractedTask.done():
                    logger.debug('Starting waitingForRetractedTask')
                    waitingForRetractedTask = asyncio.create_task(
                        asyncTryAndLogExceptionOnError(self._waitForRetractedThenUpdateState))
            else:
                if waitingForRetractedTask is not None:
                    logger.debug('Canceling waitingForRetractedTask')
                    waitingForRetractedTask.cancel()
                    waitingForRetractedTask = None

            if self._state in (
                TargetingState.ALIGNING_SERVOING,
                TargetingState.ALIGNING_CONTACTING,
                TargetingState.ALIGNING_RETRACTING,
                TargetingState.ALIGNING_RETRACTED,
            ):
                if waitingForAlignedTask is None or waitingForAlignedTask.done():
                    logger.debug('Starting waitingForAlignedTask')
                    waitingForAlignedTask = asyncio.create_task(
                        asyncTryAndLogExceptionOnError(self._waitForAlignedThenUpdateState))
            else:
                if waitingForAlignedTask is not None:
                    logger.debug('Canceling waitingForAlignedTask')
                    waitingForAlignedTask.cancel()
                    waitingForAlignedTask = None

            if self._state in (
                TargetingState.ALIGNED_SERVOING,
                TargetingState.ALIGNED_CONTACTING,
                TargetingState.ALIGNED_RETRACTING,
                TargetingState.ALIGNED_RETRACTED,
            ):
                if waitingForMisalignedTask is None or waitingForMisalignedTask.done():
                    logger.debug('Starting waitingForMisalignedTask')
                    waitingForMisalignedTask = asyncio.create_task(
                        asyncTryAndLogExceptionOnError(self._waitForMisalignedThenUpdateState))
            else:
                if waitingForMisalignedTask is not None:
                    logger.debug('Canceling waitingForMisalignedTask')
                    waitingForMisalignedTask.cancel()
                    waitingForMisalignedTask = None

            if self._state in (
                TargetingState.MOVING,
            ):
                if waitingForMovedTask is None or waitingForMovedTask.done():
                    logger.debug('Starting waitingForMovedTask')
                    waitingForMovedTask = asyncio.create_task(
                        asyncTryAndLogExceptionOnError(self._waitForMovedThenUpdateState))

            else:
                if waitingForMovedTask is not None:
                    logger.debug('Canceling waitingForMovedTask')
                    waitingForMovedTask.cancel()
                    waitingForMovedTask = None

            if self._state in (
                TargetingState.MOVED,
            ):
                if waitingForNeedToMoveTask is None or waitingForNeedToMoveTask.done():
                    logger.debug('Starting waitingForNeedToMoveTask')
                    waitingForNeedToMoveTask = asyncio.create_task(
                        asyncTryAndLogExceptionOnError(self._waitForNeedToMoveThenUpdateState))

            else:
                if waitingForNeedToMoveTask is not None:
                    logger.debug('Canceling waitingForNeedToMoveTask')
                    waitingForNeedToMoveTask.cancel()
                    waitingForNeedToMoveTask = None

            match self._state:
                case TargetingState.DISCONNECTED:
                    await self.stateChangedEvent.wait()

                case TargetingState.UNINITIALIZED:
                    await self.stateChangedEvent.wait()

                case TargetingState.PROTECTIVE_STOPPED:
                    await self.stateChangedEvent.wait()

                case TargetingState.FREEDRIVING:
                    if not self.cobotClient.isFreedriving:
                        await self.cobotClient.startFreedrive()
                    await self.stateChangedEvent.wait()

                case TargetingState.IDLE:
                    await self.stateChangedEvent.wait()

                case TargetingState.UNALIGNED_SERVOING:
                    await self.stateChangedEvent.wait()

                case TargetingState.UNALIGNED_CONTACTING:
                    await self.stateChangedEvent.wait()

                case TargetingState.UNALIGNED_RETRACTING:
                    await self.stateChangedEvent.wait()

                case TargetingState.ALIGNED_SERVOING:
                    await self.stateChangedEvent.wait()

                case TargetingState.ALIGNED_CONTACTING:
                    await self.stateChangedEvent.wait()

                case TargetingState.ALIGNED_RETRACTING:
                    await self.stateChangedEvent.wait()

                case TargetingState.ALIGNED_RETRACTED:
                    await self.stateChangedEvent.wait()

                case TargetingState.ALIGNING_SERVOING:
                    await self.stateChangedEvent.wait()

                case TargetingState.ALIGNING_CONTACTING:
                    await self.stateChangedEvent.wait()

                case TargetingState.ALIGNING_RETRACTING:
                    await self.stateChangedEvent.wait()

                case TargetingState.ALIGNING_RETRACTED:
                    await self.stateChangedEvent.wait()

                case TargetingState.MOVING:
                    await self.stateChangedEvent.wait()

                case TargetingState.MOVED:
                    await self.stateChangedEvent.wait()

                case TargetingState.MOVED_FROZEN:
                    await self.stateChangedEvent.wait()

                case _:
                    logger.error('Unexpected state: {self._state}')
                    raise NotImplementedError

    async def _loop_runActionSequences(self):
        while True:
            logger.debug('_loop_runActionSequences')
            if len(self._actionSequenceStack) == 0:
                self.actionSequenceStackChangedEvent.clear()
                await self.actionSequenceStackChangedEvent.wait()
                continue

            await asyncio.sleep(0.)  # yield

            currentActionSequence = self._actionSequenceStack[-1]
            try:
                currentAction = currentActionSequence.__next__()
            except StopIteration:
                assert currentActionSequence.isDone
                self._actionSequenceStack.pop()
                self.actionSequenceStackChangedEvent.set()
                self.sigActionSequenceStackChanged.emit()
                continue

            self.actionSequenceStackChangedEvent.set()  # set to indicate that we incremented within current sequence
            self.sigActionSequenceStackChanged.emit()

            # run current action
            asyncFn = currentAction.getAsyncFn(self)
            if asyncFn is None:
                syncFn = currentAction.getSyncFn(self)
                assert syncFn is not None, 'Action must have either async or sync function'
                logger.debug(f'Running sync action: {syncFn.__name__}')
                syncFn(*currentAction.args, **currentAction.kwargs)
            else:
                logger.debug(f'Awaiting action: {currentAction.asyncFnStr}')
                await asyncFn(*currentAction.args, **currentAction.kwargs)
            # note: if this raises an exception, the entire action sequence stack will effectively be aborted

    async def startRootActionSequence(self, actionSequence: CobotActionSequence | dict):
        # only allow public starting of an action sequence if no other action sequences are in progress
        if len(self._actionSequenceStack) is not None:
            await self.cancelActionSequences()

        await self.startActionSequence(actionSequence=actionSequence)

    async def startActionSequence(self, actionSequence: CobotActionSequence | dict):
        if isinstance(actionSequence, dict):
            actionSequence = CobotActionSequence.fromDict(actionSequence)

        logger.info(f'Starting action sequence: {actionSequence}')

        self._actionSequenceStack.append(actionSequence)
        self.actionSequenceStackChangedEvent.set()
        self.sigActionSequenceStackChanged.emit()

        if self._runActionSequencesTask is None:
            self._runActionSequencesTask = asyncio.create_task(asyncTryAndLogExceptionOnError(self._loop_runActionSequences))

        # note that if a previous action sequence is already running, this new (nested) sequence won't start running until the current action (within the parent sequence) is done

    async def cancelActionSequences(self):
        logger.info('cancelActionSequences')
        if self._runActionSequencesTask is None:
            return
        self._runActionSequencesTask.cancel()
        self._runActionSequencesTask = None
        self._actionSequenceStack.clear()
        self.actionSequenceStackChangedEvent.set()
        self.sigActionSequenceStackChanged.emit()

    def getActionSequenceProgressAndLabels(self) -> tuple[tuple[int | None, int, tuple[str,...]], ...]:
        """
        Returns a tuple of (currentActionIndex, totalNumActions, (actionSequenceLabel, action0Label, action1Label,...))
         for each action sequence in the stack, with the "currently executing" (or about to be executed) action
         sequence last.
        """
        return tuple((actionSequence.lastRanActionIndex, len(actionSequence),
                      tuple([actionSequence.label] + [action.label for action in actionSequence.actions])) for actionSequence in self._actionSequenceStack)

    async def _waitForStableContactAndRecordOffset(self, minContactTimeForStability: float | None = None):
        zDistError = None
        while True:
            await self._waitForStableContact(minContactTimeForStability=minContactTimeForStability)
            try:
                horizDistError, zDistError, horizAngleError, zAngleError = await self.calculateAlignmentError(self._targetCoilToMRITransf)
            except self.MissingInformationError:
                continue  # wait for stable contact again and then try to recalc zDistError
            else:
                break

        logger.info(f'Setting _targetZOffsetAtForceThreshold to {zDistError}')
        self._targetZOffsetAtForceThreshold = zDistError
        self.sigHasCalibratedContactDepthForCurrentTargetChanged.emit()
        self._targetingInfoUpdatedEvent.set()

    async def waitForChangeToState(self, state: TargetingState | int | str | list[TargetingState | int | str]):
        if isinstance(state, list):
            # wait for any of the states in the list
            states = state
            for iState in range(len(states)):
                if isinstance(states[iState], int):
                    states[iState] = TargetingState(states[iState])
                elif isinstance(states[iState], str):
                    states[iState] = TargetingState[states[iState]]
                else:
                    assert isinstance(states[iState], TargetingState)

            while self._state not in states:
                await self.stateChangedEvent.wait()

        else:
            if isinstance(state, int):
                state = TargetingState(state)
            elif isinstance(state, str):
                state = TargetingState[state]
            assert isinstance(state, TargetingState)

            while self._state != state:
                await self.stateChangedEvent.wait()

    async def waitForTime(self, time: float):
        await asyncio.sleep(time)

    async def waitForInTolerance(self):
        await self._cobotClient.inToleranceToDestinationEvent.wait()

    async def waitForApproximatelyAligned(self):
        assert self._state in (
            TargetingState.ALIGNED_SERVOING,
            TargetingState.ALIGNED_CONTACTING,
            TargetingState.ALIGNED_RETRACTING,
            TargetingState.ALIGNED_RETRACTED,
            TargetingState.ALIGNING_SERVOING,
            TargetingState.ALIGNING_CONTACTING,
            TargetingState.ALIGNING_RETRACTING,
            TargetingState.ALIGNING_RETRACTED,
            TargetingState.MOVING,
            TargetingState.MOVED), 'isApproximatelyAligned not updated in other states'

        await self._isApproximatelyAlignedEvent.wait()

    async def waitForRetracted(self):
        await self._cobotClient.coilRetractedEvent.wait()

    async def startMovingToTarget(self):
        assert self.targetIsAccessible
        assert not self.cobotClient.isServoing and not self.cobotClient.isRetracting, 'Must retract fully before MOVE'
        # TODO: if we can find a way to stop servoing without a full retraction, can change this assert to just stop contact here
        # but doing stopContact and MOVE immediately after does not work with current implementation (Cobot fully retracts, ignoring MOVE depth)
        self._changeToState(TargetingState.MOVING)

    async def startContactAndFreeze(self):
        """
        Note: this just initiates the sequence, returning immediately
        """
        logger.info(f'startContactAndFreeze')

        assert self.targetLabel is not None
        assert self.targetCoilToMRITransf is not None
        self.contactMode = ContactMode.CONTACT_THEN_FREEZE

        actionSequence = CobotActionSequence(
            label='Start contact and freeze',
            actions=[
                CobotAction(asyncFn=self.setContactMode, args=[ContactMode.DEFAULT]),
                CobotAction(asyncFn=self.startContact),
                CobotAction(asyncFn=self._waitForStableContactAndRecordOffset),
                CobotAction(asyncFn=self.stopContact),
                CobotAction(asyncFn=self.waitForRetracted),  # unfortunately need to fully retract before setting MOVE depth
                CobotAction(asyncFn=self.setContactMode, args=[ContactMode.CONTACT_THEN_FREEZE]),
                CobotAction(asyncFn=self._reportStartingContact),
                CobotAction(asyncFn=self.startMovingToTarget),
                CobotAction(asyncFn=self.waitForChangeToState, kwargs=dict(state=TargetingState.MOVED)),
            ])
        await self.startActionSequence(actionSequence)

    async def startAirgappingFromContact(self, doForceCalibration: bool = False):
        logger.info('startAirgappingFromContact')

        assert self.targetLabel is not None
        assert self.targetCoilToMRITransf is not None
        self.contactMode = ContactMode.AIRGAPPED_FROM_CONTACT

        if self._targetZOffsetAtForceThreshold is None or doForceCalibration:
            # calibrate contact depth by touching, then back off
            logger.info('Calibrating airgapped offset')
            actionSequence = CobotActionSequence(
                label='Start airgapping',
                actions=[
                    CobotAction(asyncFn=self.setContactMode, args=[ContactMode.DEFAULT]),
                    CobotAction(asyncFn=self.startContact),
                    CobotAction(asyncFn=self._waitForStableContactAndRecordOffset),
                    CobotAction(asyncFn=self.stopContact),
                    CobotAction(asyncFn=self.waitForRetracted),  # unfortunately need to fully retract before setting MOVE depth
                    CobotAction(asyncFn=self.setContactMode, args=[ContactMode.AIRGAPPED_FROM_CONTACT]),
                    CobotAction(asyncFn=self._reportStartingContact),
                    CobotAction(asyncFn=self.startMovingToTarget),
                    CobotAction(asyncFn=self.waitForChangeToState, kwargs=dict(state=TargetingState.MOVED)),
                ])
            await self.startActionSequence(actionSequence)
        else:
            # previously calibrated depth available, move directly to airgapped target
            logger.info('Using previously calibrated airgap contact depth')
            # TODO: double check that moving to target won't cause collisions before initiating
            actionSequence = CobotActionSequence(
                label='Start airgapping',
                actions=[
                    CobotAction(asyncFn=self._reportStartingContact),
                    CobotAction(asyncFn=self.startMovingToTarget),
                    CobotAction(asyncFn=self.waitForChangeToState, kwargs=dict(state=TargetingState.MOVED)),
                ])
            if self.cobotClient.isServoing:
                if not self.cobotClient.isRetracting:
                    actionSequence.insert(0, CobotAction(asyncFn=self._cobotClient.stopContact))
                actionSequence.insert(1, CobotAction(asyncFn=self.waitForRetracted))

            await self.startActionSequence(actionSequence)

    async def startAirgappingFromScalp(self):
        assert self.targetLabel is not None
        assert self.targetCoilToMRITransf is not None
        self.contactMode = ContactMode.AIRGAPPED_FROM_SCALP

        await self.getHeadMesh()  # make sure head mesh is loaded, since this is needed for scalp offset calculation
        # TODO: double check that moving to target won't cause collisions before initiating
        actionSequence = CobotActionSequence(
            label='Start airgapping',
            actions=[
                CobotAction(asyncFn=self._reportStartingContact),
                CobotAction(asyncFn=self.startMovingToTarget),
                CobotAction(asyncFn=self.waitForChangeToState, kwargs=dict(state=TargetingState.MOVED)),
            ])
        await self.startActionSequence(actionSequence)

    async def startAirgappingFromTarget(self):
        assert self.targetLabel is not None
        assert self.targetCoilToMRITransf is not None
        self.contactMode = ContactMode.OFFSET_FROM_TARGET

        # TODO: double check that moving to target won't cause collisions before initiating
        actionSequence = CobotActionSequence(
            label='Start airgapping',
            actions=[
                CobotAction(asyncFn=self._reportStartingContact),
                CobotAction(asyncFn=self.startMovingToTarget),
                CobotAction(asyncFn=self.waitForChangeToState, kwargs=dict(state=TargetingState.MOVED)),
            ])
        await self.startActionSequence(actionSequence)

    async def setAirgapOffsetFromScalp_FromContactOffsetDepth(self):
        assert self._targetZOffsetAtForceThreshold is not None

        await self.getHeadMesh()  # make sure head mesh is loaded, since this is needed for scalp offset calculation

        targetZOffsetAtScalp = self.targetZOffsetAtScalp

        assert targetZOffsetAtScalp is not None

        self.airgapOffsetFromScalp = self._targetZOffsetAtForceThreshold + self.airgapOffsetFromContact - targetZOffsetAtScalp

    async def startSession(self, sessionNameSuffix: str | None= None):
        if sessionNameSuffix is None:
            sessionNameSuffix = self._cobotSessionNameSuffix
        await self._cobotClient.startSession(suffix=sessionNameSuffix)

        if self._cobotClient.isEnabled and \
            self._cobotClient.isPoweredOn and \
            self._cobotClient.isHomed:
            """
            Probably skipping initialization this time due to having already been initialized during a previous connection
            """
            if self._activeCartTrackerKey is not None:
                # if previously initialized, cart tracker key should have been set then
                self._cobotConnectedEvent.set()

    def _onClientSignaled(self, signalKey: str):
        self._updateState([signalKey])
        logger.debug(f'Client signaled: {signalKey}')
        self._connector.publish([b'signal', signalKey.encode('utf-8')])

    def getClientAttr(self, item: str):
        return getattr(self._cobotClient, item)

    async def callClientMethod_async(self, clientMethod: str, *args, **kwargs):
        return await getattr(self._cobotClient, clientMethod)(*args, **kwargs)


    @classmethod
    async def createAndRun_async(cls, **kwargs):
        self = cls(**kwargs)
        await self.run()

    @classmethod
    def createAndRun(cls, **kwargs):
        from NaviNIBS.util.Asyncio import asyncioRunAndHandleExceptions
        asyncioRunAndHandleExceptions(cls.createAndRun_async, **kwargs)


if __name__ == '__main__':
    import argparse
    # TODO: implement support for running as a standalone exe, accepting same kwargs as createAndRun but from command line

    CobotConnectorServer.createAndRun()