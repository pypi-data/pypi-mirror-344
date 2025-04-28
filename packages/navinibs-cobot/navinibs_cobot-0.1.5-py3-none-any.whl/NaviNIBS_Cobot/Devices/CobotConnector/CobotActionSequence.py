import asyncio
import attrs
import logging
import numpy as np
import typing as tp


from NaviNIBS.util.attrs import attrsAsDict
from NaviNIBS.util.numpy import attrsWithNumpyAsDict, attrsWithNumpyFromDict

logger = logging.getLogger(__name__)


@attrs.define
class CobotAction:
    _asyncFnStr: str | None = attrs.field(default=None)
    _asyncFn: tp.Callable[..., tp.Awaitable[tp.Any]] | None = attrs.field(
        default=None,
        repr=lambda asyncFn: asyncFn.__name__ if asyncFn is not None else 'None')
    _syncFn: tp.Callable[..., tp.Any] | None = attrs.field(default=None, repr=False)
    _args: tp.Iterable[tp.Any] = attrs.field(factory=list)
    _kwargs: dict[str, tp.Any] = attrs.field(factory=dict)
    _ndarrayKwargs: list[str] = attrs.field(factory=list)  # kwarg keys indicating which values should be treated as ndarray for serialization/deserialization

    def __attrs_post_init__(self):
        assert (self._asyncFn is None) != (self._asyncFnStr is None), "Either asyncFn or asyncFnStr must be set, but not both"
        assert sum(x is not None for x in (self._asyncFn, self._asyncFnStr, self._syncFn)) == 1, "Exactly one of asyncFn, asyncFnStr, syncFn must be set"

    def getAsyncFn(self, connector: tp.Any) -> tp.Callable[..., tp.Awaitable[tp.Any]] | None:
        if self._asyncFn is None:
            return getattr(connector, self._asyncFnStr)
        else:
            return self._asyncFn

    def getSyncFn(self, connector: tp.Any) -> tp.Callable[..., tp.Any] | None:
        return self._syncFn

    @property
    def asyncFnStr(self):
        return self._asyncFnStr

    @property
    def args(self):
        return self._args

    @property
    def kwargs(self):
        return self._kwargs

    @property
    def label(self):
        if self._asyncFnStr is not None:
            return self._asyncFnStr
        elif self._asyncFn is not None:
            return self._asyncFn.__name__
        elif self._syncFn is not None:
            return self._syncFn.__name__
        else:
            raise NotImplementedError

    def asDict(self) -> dict[str, tp.Any]:
        assert self._asyncFn is None, 'Cannot serialize an action with a bound asyncFn'
        d = attrsAsDict(self)
        for key in self._ndarrayKwargs:
            if key in d and d[key] is not None:
                d[key] = d[key].tolist()

        return d

    @classmethod
    def fromDict(cls, d: dict[str, tp.Any]):
        if 'kwargs' in d:
            for key in d.get('ndarrayKwargs', []):
                if key in d['kwargs']:
                    d['kwargs'][key] = np.asarray(d['kwargs'][key])
        return cls(**d)


@attrs.define
class CobotActionSequence:
    _label: str = ''
    _actions: list[CobotAction] = attrs.field(factory=list)

    _lastRanActionIndex: int | None = attrs.field(init=False, default=None)

    def __attrs_post_init__(self):
        pass

    def __iter__(self):
        return self

    def __next__(self) -> CobotAction:
        actionIndex = self._lastRanActionIndex
        if actionIndex is None:
            actionIndex = 0
        else:
            actionIndex += 1
        if actionIndex >= len(self._actions):
            raise StopIteration
        self._lastRanActionIndex = actionIndex
        return self._actions[self._lastRanActionIndex]  # assume that the caller will run the action

    def append(self, action: CobotAction):
        self._actions.append(action)

    def insert(self, index: int, action: CobotAction):
        assert self._lastRanActionIndex is None or index > self._lastRanActionIndex, "Cannot insert an action before the last ran action"
        self._actions.insert(index, action)

    def extend(self, actions: list[CobotAction]):
        self._actions.extend(actions)

    @property
    def label(self):
        return self._label

    @property
    def lastRanActionIndex(self):
        return self._lastRanActionIndex

    @property
    def isDone(self):
        return self._lastRanActionIndex == len(self._actions) - 1

    @property
    def actions(self):
        """
        Note: the returned list should not be edited directly
        """
        return self._actions

    def __len__(self):
        return len(self._actions)

    def asDict(self) -> dict[str, tp.Any]:
        d = attrsAsDict(self, exclude=['actions'])
        d['actions'] = [action.asDict() for action in self._actions]
        return d

    @classmethod
    def fromDict(cls, d: dict[str, tp.Any]):
        d['actions'] = [CobotAction.fromDict(actionDict) for actionDict in d['actions']]
        return cls(**d)

