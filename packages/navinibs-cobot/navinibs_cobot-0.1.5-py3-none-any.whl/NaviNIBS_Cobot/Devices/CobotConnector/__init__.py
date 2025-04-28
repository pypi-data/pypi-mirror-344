from enum import IntEnum, auto


cobotTargetingServerHostname = '127.0.0.1'
cobotTargetingServerPubPort = 18960
cobotTargetingServerCmdPort = 18961


class TargetingState(IntEnum):
    DISCONNECTED = auto()
    UNINITIALIZED = auto()
    PROTECTIVE_STOPPED = auto()
    FREEDRIVING = auto()
    IDLE = auto()
    UNALIGNED_SERVOING = auto()
    UNALIGNED_CONTACTING = auto()
    UNALIGNED_RETRACTING = auto()
    ALIGNED_SERVOING = auto()
    ALIGNED_CONTACTING = auto()
    ALIGNED_RETRACTING = auto()
    ALIGNED_RETRACTED = auto()
    ALIGNING_SERVOING = auto()
    ALIGNING_CONTACTING = auto()
    ALIGNING_RETRACTING = auto()
    ALIGNING_RETRACTED = auto()
    MOVING = auto()
    MOVED = auto()  # equivalent to ALIGNED (can transition back to MOVING if need to compensate for head movement)
    MOVED_FROZEN = auto()  # equivalent to UNALIGNED (will not compensate for head movement)


class ContactMode(IntEnum):
    DEFAULT = auto()
    CONTACT_THEN_FREEZE = auto()
    AIRGAPPED_FROM_CONTACT = auto()
    AIRGAPPED_FROM_SCALP = auto()
    OFFSET_FROM_TARGET = auto()


class TargetChangeRetractMode(IntEnum):
    FULLY_RETRACT_THEN_ALIGN = auto()
    PARTIALLY_RETRACT_AND_ALIGN = auto()
    LIMITED_RETRACT_THEN_ALIGN = auto()
    ALIGN_WITHOUT_RETRACT = auto()


class TargetChangeContactMode(IntEnum):
    DO_NOT_RESUME_CONTACT = auto()
    RESUME_IMMEDIATELY = auto()  # immediately after sending align to new target
    RESUME_WHEN_IN_TOLERANCE = auto()
    RESUME_WHEN_APPROXIMATELY_ALIGNED = auto()
    RESUME_WHEN_ALIGNED = auto()
    INITIATE_IMMEDIATELY = auto()  # immediately after sending align to new target
    INITIATE_WHEN_IN_TOLERANCE = auto()
    INITIATE_WHEN_APPROXIMATELY_ALIGNED = auto()
    INITIATE_WHEN_ALIGNED = auto()
