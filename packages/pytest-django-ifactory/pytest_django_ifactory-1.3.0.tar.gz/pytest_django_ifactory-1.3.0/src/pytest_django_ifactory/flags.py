"""Creation flags for the factory."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from typing_extensions import TypeGuard


__all__ = [
    "CreateRelatedInstance",
    "LookupRelatedInstance",
    "Unique",
    "is_create",
    "is_lookup",
    "is_unique",
]


class CreateRelatedInstance:
    """Flag for creating a related instance using the factory.

    Any *attrs* given to the constructor will be used when creating
    the related instance.

    """

    def __init__(self, **attrs: Any) -> None:
        self.attrs = attrs


def is_create(
    obj: Any,
) -> TypeGuard[CreateRelatedInstance | type[CreateRelatedInstance]]:
    return is_class_or_instance(obj, CreateRelatedInstance)


class LookupRelatedInstance:
    """Flag for looking up a related instance in the database.

    The *attrs* given to the constructor must uniquely identify the
    related instance in the database.

    """

    def __init__(self, **attrs: Any) -> None:
        self.attrs = attrs


def is_lookup(
    obj: Any,
) -> TypeGuard[LookupRelatedInstance | type[LookupRelatedInstance]]:
    return is_class_or_instance(obj, LookupRelatedInstance)


class Unique:
    """Flag for generating a unique value for a field."""


def is_unique(obj: Any) -> TypeGuard[Unique | type[Unique]]:
    return is_class_or_instance(obj, Unique)


def is_class_or_instance(obj: Any, cls: type[Any]) -> bool:
    return obj is cls or isinstance(obj, cls)
