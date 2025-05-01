"""Type helpers for pytest-django-ifactory."""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any, TypeVar, Union

if TYPE_CHECKING:
    from django.db.models import Field

T = TypeVar("T")
FieldSetter = Union[T, Callable[[], T], None]

F = TypeVar("F", bound="Field[Any, Any]")
ValueGenerator = Callable[[F, bool], FieldSetter[Any]]
