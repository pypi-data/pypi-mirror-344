from __future__ import annotations
import asyncio
import attrs
import numpy as np
import typing as tp

from NaviNIBS_Cobot.Devices.CobotTargetingController import CobotTargetingController

from NaviNIBS.Navigator.Model.Addons import AddonSessionConfig
from NaviNIBS.Navigator.Model.Session import Session
from NaviNIBS.util.attrs import attrsAsDict


@attrs.define
class CobotControl(AddonSessionConfig):
    _cobotAddr: str = '127.0.0.1'
    """
    IP address of the Cobot system, or of a computer running the Cobot simulator.
    
    Note: for now, if not using the default, this needs to be set in the configuration file. It is not yet possible to edit it via the GUI.
    """
    _cobotIsSimulated: bool | None = None
    """
    If set to None, will be automatically determined based on IP. 
    If IP is set to '127.0.0.1' or 'localhost', isSimulated will be set to True. Else it will be set to False.
    """
    _forceLastCheckedAtTime: str | None = None
    """
    Timestamp of last force check in format '%y%m%d%H%M%S.%f'
    """
    _needsForceCheckAfterMinutes: int = 120

    _controller: tp.Optional[CobotTargetingController] = attrs.field(init=False, default=None)
    _controllerInitLock: asyncio.Lock = attrs.field(init=False, factory=asyncio.Lock)

    def __attrs_post_init__(self):
        super().__attrs_post_init__()

    @property
    def cobotAddr(self):
        return self._cobotAddr

    @property
    def cobotIsSimulated(self):
        return self._cobotIsSimulated

    @property
    def forceLastCheckedAtTime(self):
        return self._forceLastCheckedAtTime

    @forceLastCheckedAtTime.setter
    def forceLastCheckedAtTime(self, newTime: str | None):
        if newTime == self._forceLastCheckedAtTime:
            return
        self.sigConfigAboutToChange.emit(['forceLastCheckedAtTime'])
        self._forceLastCheckedAtTime = newTime
        self.sigConfigChanged.emit(['forceLastCheckedAtTime'])

    @property
    def needsForceCheckAfterMinutes(self):
        return self._needsForceCheckAfterMinutes

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, newController: CobotTargetingController | None):
        if newController is self._controller:
            return
        if self._controller is not None:
            raise NotImplementedError  # TODO: add support for clearing previous, setting new

        assert not self._controllerInitLock.locked()  # make sure an async init isn't in progress

        self._controller = newController

    async def initializeController(self, session: Session):
        assert self._controller is None
        async with self._controllerInitLock:
            if self._controller is not None:
                # someone else completed initialization while we were waiting
                assert self._controller.session is session
                await self._controller.cobotClient.connectedToServerEvent.wait()
                return

            controller = CobotTargetingController(
                session=session,
                connectorServerKwargs=dict(
                    cobotAddr=self.cobotAddr,
                    cobotIsSimulated=self.cobotIsSimulated,
                ))
            # wait until the controller server is ready
            await controller.cobotClient.connectedToServerEvent.wait()

        self.controller = controller

    def asDict(self) -> dict[str, tp.Any]:
        d = attrsAsDict(self)
        return d

    @classmethod
    def fromDict(cls, d: dict[str, tp.Any]):
        return cls(**d)


