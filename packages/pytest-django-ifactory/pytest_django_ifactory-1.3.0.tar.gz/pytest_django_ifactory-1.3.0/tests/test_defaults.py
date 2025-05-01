"""Unit tests for pytest-django-ifactory's default value generators."""

from __future__ import annotations

import datetime

import pytest
from django.contrib.gis.db import models
from django.utils.dateparse import parse_datetime, parse_time

from pytest_django_ifactory.defaults import generate_default_value


def test_default_default() -> None:
    assert generate_default_value(models.Field()) is None


def test_default_unique_default() -> None:
    with pytest.raises(ValueError, match="unique not supported"):
        generate_default_value(models.Field(), unique=True)


@pytest.mark.parametrize("field_type", [models.BooleanField, models.JSONField])
@pytest.mark.parametrize("field_is_unique", [True, False])
def test_unique_not_implemented(
    field_type: type[models.Field], field_is_unique: bool
) -> None:
    field = field_type(unique=field_is_unique)
    with pytest.raises(ValueError, match="unique not supported"):
        generate_default_value(field, unique=not field_is_unique)


def test_boolean_field_default() -> None:
    assert generate_default_value(models.BooleanField()) is True


@pytest.mark.parametrize(
    "field_type",
    [
        models.CharField,
        models.EmailField,
        models.FileField,
        models.ImageField,
        models.SlugField,
        models.TextField,
    ],
)
class TestCharFieldDefault:
    def test_nonunique(self, field_type: type[models.Field]) -> None:
        field = field_type(max_length=9, unique=False)
        assert generate_default_value(field) == "abcd"

    @pytest.mark.parametrize("field_is_unique", [True, False])
    def test_unique(
        self, field_type: type[models.Field], field_is_unique: bool
    ) -> None:
        field = field_type(max_length=9, unique=field_is_unique)
        default = generate_default_value(field, unique=not field_is_unique)
        assert callable(default)
        assert default() == "abcd"
        assert default() == "abce"

    def test_short_max_length(self, field_type: type[models.Field]) -> None:
        field = field_type(max_length=3, unique=False)
        assert generate_default_value(field) == "abc"


class TestDateFieldDefault:
    def test_nonunique(self) -> None:
        default = generate_default_value(models.DateField())
        assert default == datetime.date.fromtimestamp(0)

    @pytest.mark.parametrize("field_is_unique", [True, False])
    def test_unique(self, field_is_unique: bool) -> None:
        field = models.DateField(unique=field_is_unique)  # type: ignore[var-annotated]
        default = generate_default_value(field, unique=not field_is_unique)
        assert callable(default)
        assert default() == datetime.date.fromtimestamp(0)
        assert default() == datetime.date.fromtimestamp(0) + datetime.timedelta(days=1)

    def test_auto_now(self) -> None:
        assert generate_default_value(models.DateField(auto_now=True)) is None

    def test_auto_now_add(self) -> None:
        assert generate_default_value(models.DateField(auto_now_add=True)) is None


class TestDateTimeFieldDefault:
    def test_nonunique(self) -> None:
        default = generate_default_value(models.DateTimeField())
        assert default == parse_datetime("1970-01-01T00:00Z")

    @pytest.mark.parametrize("field_is_unique", [True, False])
    def test_unique(self, field_is_unique: bool) -> None:
        field = models.DateTimeField(  # type: ignore[var-annotated]
            unique=field_is_unique
        )
        default = generate_default_value(field, unique=not field_is_unique)
        assert callable(default)
        assert default() == parse_datetime("1970-01-01T00:00Z")
        assert default() == parse_datetime("1970-01-01T01:00Z")

    def test_auto_now(self) -> None:
        assert generate_default_value(models.DateTimeField(auto_now=True)) is None

    def test_auto_now_add(self) -> None:
        assert generate_default_value(models.DateTimeField(auto_now_add=True)) is None


class TestFloatFieldDefault:
    def test_nonunique(self) -> None:
        assert generate_default_value(models.FloatField()) == pytest.approx(0)

    @pytest.mark.parametrize("field_is_unique", [True, False])
    def test_unique(self, field_is_unique: bool) -> None:
        field = models.FloatField(unique=field_is_unique)  # type: ignore[var-annotated]
        default = generate_default_value(field, unique=not field_is_unique)
        assert callable(default)
        assert default() == pytest.approx(0)
        assert default() == pytest.approx(1)


@pytest.mark.parametrize(
    "field_type",
    [
        models.BigIntegerField,
        models.DecimalField,
        models.IntegerField,
        models.PositiveIntegerField,
        models.PositiveSmallIntegerField,
        models.SmallIntegerField,
    ],
)
class TestIntegerFieldDefault:
    def test_nonunique(self, field_type: type[models.Field]) -> None:
        field = field_type()
        assert generate_default_value(field) == 0

    @pytest.mark.parametrize("field_is_unique", [True, False])
    def test_unique(
        self, field_type: type[models.Field], field_is_unique: bool
    ) -> None:
        field = field_type(unique=field_is_unique)
        default = generate_default_value(field, unique=not field_is_unique)
        assert callable(default)
        assert default() == 0
        assert default() == 1


class TestTimeFieldDefault:
    def test_nonunique(self) -> None:
        default = generate_default_value(models.TimeField())
        assert default == parse_time("00:00")

    @pytest.mark.parametrize("field_is_unique", [True, False])
    def test_unique(self, field_is_unique: bool) -> None:
        field = models.TimeField(unique=field_is_unique)  # type: ignore[var-annotated]
        default = generate_default_value(field, unique=not field_is_unique)
        assert callable(default)
        assert default() == parse_time("00:00:00")
        assert default() == parse_time("00:00:01")

    def test_auto_now(self) -> None:
        assert generate_default_value(models.TimeField(auto_now=True)) is None

    def test_auto_now_add(self) -> None:
        assert generate_default_value(models.TimeField(auto_now_add=True)) is None


@pytest.mark.parametrize(
    ("field_type", "expected_defaults"),
    [
        (models.GeometryField, ["POINT (1 0)", "POINT (2 0)"]),
        (models.PointField, ["POINT (1 0)", "POINT (2 0)"]),
        (models.LineStringField, ["LINESTRING (1 0, 0 1)", "LINESTRING (2 0, 0 1)"]),
        (
            models.PolygonField,
            ["POLYGON ((0 0, 1 1, 0 1, 0 0))", "POLYGON ((0 0, 2 1, 0 1, 0 0))"],
        ),
        (models.MultiPointField, ["MULTIPOINT ((1 0))", "MULTIPOINT ((2 0))"]),
        (
            models.MultiLineStringField,
            ["MULTILINESTRING ((1 0, 0 1))", "MULTILINESTRING ((2 0, 0 1))"],
        ),
        (
            models.MultiPolygonField,
            [
                "MULTIPOLYGON (((0 0, 1 1, 0 1, 0 0)))",
                "MULTIPOLYGON (((0 0, 2 1, 0 1, 0 0)))",
            ],
        ),
        (
            models.GeometryCollectionField,
            ["GEOMETRYCOLLECTION (POINT (1 0))", "GEOMETRYCOLLECTION (POINT (2 0))"],
        ),
    ],
)
class TestGeometryFieldDefault:
    def test_nonunique(
        self, field_type: type[models.GeometryField], expected_defaults: list[str]
    ) -> None:
        default = generate_default_value(field_type())
        assert default == expected_defaults[0]

    @pytest.mark.parametrize("field_is_unique", [True, False])
    def test_unique(
        self,
        field_type: type[models.GeometryField],
        expected_defaults: list[str],
        field_is_unique: bool,
    ) -> None:
        field = field_type(unique=field_is_unique)
        default = generate_default_value(field, unique=not field_is_unique)
        assert callable(default)
        assert default() == expected_defaults[0]
        assert default() == expected_defaults[1]


def test_json_field_default() -> None:
    field = models.JSONField()
    assert generate_default_value(field) == {}
