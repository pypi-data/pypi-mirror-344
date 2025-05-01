"""Default value generation for model fields."""

from __future__ import annotations

import datetime
import itertools
import string
from typing import TYPE_CHECKING, Any, overload

from django.core.exceptions import ImproperlyConfigured

if TYPE_CHECKING:
    from collections.abc import Callable

    from .typing import F, FieldSetter, ValueGenerator

try:
    from django.contrib.gis.db import models

    HAVE_GIS_MODELS = True
except ImproperlyConfigured:
    from django.db import models  # type: ignore[no-redef]

    HAVE_GIS_MODELS = False

_generators: dict[type[models.Field], ValueGenerator[Any]] = {}


@overload
def register(field_class: type[F], generator: ValueGenerator[F]) -> None: ...


@overload
def register(
    field_class: type[F], generator: None = ...
) -> Callable[[ValueGenerator[F]], None]: ...


def register(
    field_class: type[F], generator: ValueGenerator[F] | None = None
) -> Callable[[ValueGenerator[F]], None] | None:
    """Register a default value generator for a field class."""

    def decorator(generator: ValueGenerator[F]) -> None:
        _generators[field_class] = generator

    if generator is None:
        return decorator

    decorator(generator)
    return None


def generate_default_value(field: F, unique: bool = False) -> FieldSetter[Any]:
    """Generate a default value for a model field."""

    def _default_generator(_: models.Field[None, Any], unique: bool = False) -> None:
        if unique:
            raise ValueError("unique not supported")
        return None  # noqa: PLR1711, RET501

    generator = _generators.get(type(field), _default_generator)
    return generator(field, unique)  # type: ignore[no-untyped-call]


@register(models.BooleanField)
def boolean_field_default(field: models.BooleanField, unique: bool = False) -> bool:
    if unique or field.unique:
        raise ValueError("unique not supported")
    return True


def char_field_default(
    field: models.CharField | models.FileField | models.TextField, unique: bool = False
) -> FieldSetter[str]:
    length = min(4, field.max_length or 4)
    if unique or field.unique:
        it = itertools.permutations(string.ascii_letters, length)
        return lambda: "".join(next(it))
    return "" if field.blank else "abcd"[:length]


register(models.CharField, char_field_default)
register(models.EmailField, char_field_default)
register(models.FileField, char_field_default)
register(models.ImageField, char_field_default)
register(models.SlugField, char_field_default)
register(models.TextField, char_field_default)


@register(models.DateField)
def date_field_default(
    field: models.DateField, unique: bool = False
) -> FieldSetter[datetime.date]:
    if field.auto_now or field.auto_now_add:
        return None
    if unique or field.unique:
        it = itertools.count(step=24 * 60**2)
        return lambda: datetime.date.fromtimestamp(next(it))
    return datetime.date.fromtimestamp(0)


@register(models.DateTimeField)
def date_time_field_default(
    field: models.DateTimeField, unique: bool = False
) -> FieldSetter[datetime.datetime]:
    def todatetime(timestamp: int) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc)

    if field.auto_now or field.auto_now_add:
        return None
    if unique or field.unique:
        it = itertools.count(step=60**2)
        return lambda: todatetime(next(it))
    return todatetime(0)


@register(models.FloatField)
def float_field_default(
    field: models.FloatField, unique: bool = False
) -> FieldSetter[float]:
    if unique or field.unique:
        it = itertools.count()
        return lambda: float(next(it))
    return 0.0


def integer_field_default(
    field: models.IntegerField | models.DecimalField, unique: bool = False
) -> FieldSetter[int]:
    if unique or field.unique:
        it = itertools.count()
        return lambda: next(it)
    return 0


register(models.BigIntegerField, integer_field_default)
register(models.DecimalField, integer_field_default)
register(models.IntegerField, integer_field_default)
register(models.PositiveIntegerField, integer_field_default)
register(models.PositiveSmallIntegerField, integer_field_default)
register(models.SmallIntegerField, integer_field_default)


@register(models.JSONField)
def json_field_default(field: models.JSONField, unique: bool = False) -> dict[Any, Any]:
    if unique or field.unique:
        raise ValueError("unique not supported")
    return {}


@register(models.TimeField)
def time_field_default(
    field: models.TimeField, unique: bool = False
) -> FieldSetter[datetime.time]:
    def totime(timestamp: int) -> datetime.time:
        return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).time()

    if field.auto_now or field.auto_now_add:
        return None
    if unique or field.unique:
        it = itertools.count()
        return lambda: totime(next(it))
    return totime(0)


def make_geometry_field_default(template: str) -> ValueGenerator[models.GeometryField]:
    def _default(field: models.GeometryField, unique: bool = False) -> FieldSetter[str]:
        if unique or field.unique:
            it = itertools.count(1)
            return lambda: template % next(it)
        return template % 1

    return _default


if HAVE_GIS_MODELS:
    GIS_FIELDS: list[tuple[type[models.GeometryField], str]] = [
        (models.GeometryField, "POINT (%d 0)"),
        (models.PointField, "POINT (%d 0)"),
        (models.LineStringField, "LINESTRING (%d 0, 0 1)"),
        (models.PolygonField, "POLYGON ((0 0, %d 1, 0 1, 0 0))"),
        (models.MultiPointField, "MULTIPOINT ((%d 0))"),
        (models.MultiLineStringField, "MULTILINESTRING ((%d 0, 0 1))"),
        (models.MultiPolygonField, "MULTIPOLYGON (((0 0, %d 1, 0 1, 0 0)))"),
        (models.GeometryCollectionField, "GEOMETRYCOLLECTION (POINT (%d 0))"),
    ]

    for fieldtype, template in GIS_FIELDS:
        register(fieldtype, make_geometry_field_default(template))
