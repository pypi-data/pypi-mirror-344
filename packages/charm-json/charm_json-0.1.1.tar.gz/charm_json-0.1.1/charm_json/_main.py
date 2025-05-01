import collections.abc
import json
import types
import typing

import charm_ as charm

_JSON = typing.Union[
    typing.Mapping[str, "_JSON"], typing.Sequence["_JSON"], str, int, float, bool, None
]
_ReadWriteJSON = typing.Union[
    typing.MutableMapping[str, "_ReadWriteJSON"],
    typing.MutableSequence["_ReadWriteJSON"],
    str,
    int,
    float,
    bool,
    None,
    # Allow setting `typing.Mapping` or `typing.Sequence` (will be cast to mutable equivalent)
    _JSON,
]


class _Databag(typing.Mapping[str, _JSON]):
    _EXCLUDED_KEYS = ("egress-subnets", "ingress-address", "private-address")
    """Keys set by Juju
    
    These values are not JSON-encoded
    """

    def __init__(self, databag: typing.Mapping[str, str], /):
        self._databag = databag

    def __repr__(self):
        return f"{type(self).__name__}({repr(self._databag)})"

    @classmethod
    def _freeze(cls, data, /) -> _JSON:
        """Recursively convert output of `json.loads()` to "immutable" types

        `types.MappingProxyType` is not technically immutable, but for this purpose it is
        effectively immutable
        """
        if (
            isinstance(data, str)
            or isinstance(data, int)
            or isinstance(data, float)
            or isinstance(data, bool)
            or data is None
        ):
            return data
        if isinstance(data, collections.abc.MutableMapping):
            return types.MappingProxyType({key: cls._freeze(value) for key, value in data.items()})
        if isinstance(data, collections.abc.MutableSequence):
            return tuple(cls._freeze(value) for value in data)
        raise TypeError

    def __getitem__(self, key: str):
        if key in self._EXCLUDED_KEYS:
            return self._databag[key]
        return self._freeze(json.loads(self._databag[key]))

    def __iter__(self):
        return iter(self._databag.keys())

    def __len__(self):
        return len(self._databag)


class _MutableMapping(typing.MutableMapping[str, _ReadWriteJSON]):
    """Updates `parent` collection when mutated"""

    def __init__(
        self,
        *,
        parent: typing.Union["_WriteableDatabag", "_MutableMapping", "_MutableSequence"],
        parent_key: typing.Union[str, int],
        data: collections.abc.Mapping,
    ):
        self._parent = parent
        self._parent_key = parent_key
        self._data = dict(data)

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = _load(parent=self, parent_key=key, data=value)
        self._parent[self._parent_key] = self

    def __delitem__(self, key):
        del self._data[key]
        self._parent[self._parent_key] = self

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def setdefault(self, key, default=None, /):
        try:
            return self[key]
        except KeyError:
            pass
        self[key] = default
        # Return `self[key]` instead of `default` so that `default` is converted to
        # `_MutableMapping` or `_MutableSequence` if applicable
        return self[key]


class _MutableSequence(typing.MutableSequence[_ReadWriteJSON]):
    """Updates `parent` collection when mutated"""

    def __init__(
        self,
        *,
        parent: typing.Union["_WriteableDatabag", _MutableMapping, "_MutableSequence"],
        parent_key: typing.Union[str, int],
        data: collections.abc.Sequence,
    ):
        self._parent = parent
        self._parent_key = parent_key
        self._data = list(data)

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = _load(parent=self, parent_key=key, data=value)
        self._parent[self._parent_key] = self

    def __delitem__(self, key):
        del self._data[key]
        self._parent[self._parent_key] = self

    def __len__(self):
        return len(self._data)

    def insert(self, index, value):
        self._data.insert(index, _load(parent=self, parent_key=index, data=value))
        for index, value in enumerate(self._data):
            if isinstance(value, _MutableMapping) or isinstance(value, _MutableSequence):
                value._parent_key = index
        self._parent[self._parent_key] = self


class _Encoder(json.JSONEncoder):
    """Convert `_MutableMapping` to `dict` and `_MutableSequence` to `list`

    `json` does not support `collections.abc.Mapping` or `collections.abc.Sequence`
    """

    def default(self, o):
        if isinstance(o, _MutableMapping):
            return o._data
        if isinstance(o, _MutableSequence):
            return o._data
        return super().default(o)


def _load(
    *,
    parent: typing.Union["_WriteableDatabag", _MutableMapping, _MutableSequence],
    parent_key: typing.Union[str, int],
    data: _JSON,
) -> _ReadWriteJSON:
    """Convert `data` to `_MutableMapping`, `_MutableSequence`, or immutable types

    `_MutableMapping` and `_MutableSequence` update their parent collection when mutated

    Therefore, if any mutation is made to the return value of this function,
    `_WriteableDatabag.__setitem__()` will be called and that mutation will be written to the
    databag
    """
    if (
        isinstance(data, str)
        or isinstance(data, int)
        or isinstance(data, float)
        or isinstance(data, bool)
        or data is None
    ):
        return data
    if isinstance(data, collections.abc.Mapping):
        # We need to create `mapping` before we can populate it with correctly typed values,
        # since any mutable objects inside will need a reference to their parent (`mapping`).
        mapping = _MutableMapping(parent=parent, parent_key=parent_key, data=data)
        for key, value in mapping.items():
            value = _load(parent=mapping, parent_key=key, data=value)
            # Initial value set should not update parent
            mapping._data[key] = value
        return mapping
    if isinstance(data, collections.abc.Sequence):
        # We need to create `sequence` before we can populate it with correctly typed values,
        # since any mutable objects inside will need a reference to their parent (`sequence`).
        sequence = _MutableSequence(parent=parent, parent_key=parent_key, data=data)
        for index, value in enumerate(sequence):
            value = _load(parent=sequence, parent_key=index, data=value)
            # Initial value set should not update parent
            sequence._data[index] = value
        return sequence
    raise TypeError(
        f"Expected type 'str', 'int', 'float', 'bool', 'NoneType', 'Mapping', or 'Sequence'; got {repr(type(data).__name__)}: {repr(data)}"
    )


class _WriteableDatabag(_Databag, typing.MutableMapping[str, _ReadWriteJSON]):
    def __getitem__(self, key: str):
        if key in self._EXCLUDED_KEYS:
            return self._databag[key]
        return _load(parent=self, parent_key=key, data=json.loads(self._databag[key]))

    def __setitem__(self, key: str, value):
        if key in self._EXCLUDED_KEYS:
            if not isinstance(value, str):
                raise TypeError(
                    f"{repr(key)} is set by Juju and is not JSON-encoded. It must be set to type 'str', got {repr(type(value).__name__)}: {repr(value)}"
                )
            self._databag[key] = value
        self._databag[key] = json.dumps(value, cls=_Encoder)

    def __delitem__(self, key):
        del self._databag[key]

    def setdefault(self, key, default=None, /):
        try:
            return self[key]
        except KeyError:
            pass
        self[key] = default
        # Return `self[key]` instead of `default` so that `default` is converted to
        # `_MutableMapping` or `_MutableSequence` if applicable
        return self[key]


class Relation(charm.Relation, typing.Mapping[str, typing.Mapping[str, _JSON]]):
    def __eq__(self, other):
        return isinstance(other, Relation) and super().__eq__(other)

    def __getitem__(self, key):
        databag = charm.Relation.__getitem__(self, key)
        if isinstance(databag, collections.abc.MutableMapping):
            return _WriteableDatabag(databag)
        return _Databag(databag)

    @property
    def my_unit(self) -> typing.MutableMapping[str, _ReadWriteJSON]:
        """This unit's data"""
        return super().my_unit

    @property
    def my_app_rw(self) -> typing.Optional[typing.MutableMapping[str, _ReadWriteJSON]]:
        """This app's data (read-write)

        `None` if this unit is not leader
        """
        return super().my_app_rw

    @property
    def other_units(self) -> typing.Mapping[charm.Unit, typing.Mapping[str, _JSON]]:
        """Other units' data

        In a non-peer relation, this is the data of the other app's units
        In a peer relation, this is the data of this app's units, excluding this unit

        In a subordinate (non-peer) relation, this data only includes the other app's unit that is
        deployed to the same machine as this unit
        Note: subordinate charms can have non-subordinate relations and principal charms can have
        subordinate relations
        """
        return super().other_units

    @property
    def other_app(self) -> typing.Mapping[str, _JSON]:
        """Other app's data"""
        return super().other_app


class PeerRelation(
    Relation,
    charm.PeerRelation,
    # Improve type hint on `[]` or `.get()`
    typing.Mapping[str, typing.Mapping[str, _JSON]],
):
    @property
    def all_units(self) -> typing.Mapping[charm.Unit, typing.Mapping[str, _JSON]]:
        """All units' data

        Includes this unit's data
        """
        return super().all_units

    @property
    def my_app_ro(self) -> typing.Mapping[str, _JSON]:
        """This app's data (read-only)"""
        return super().my_app_ro

    @property
    def other_app(self) -> typing.Mapping[str, _JSON]:
        """This app's data

        In a peer relation, the "other" app is this unit's app

        Same as `my_app_ro`
        """
        return super().other_app


class Endpoint(charm.Endpoint):
    _Relation = Relation

    @property
    def relation(self) -> typing.Optional[Relation]:
        return super().relation
