"""Unit and regression tests for the instance factory class."""

from __future__ import annotations

import copy
from typing import TYPE_CHECKING

import pytest
from testapp.models import AllFieldsModel, ModelA, ModelB, ModelC

if TYPE_CHECKING:
    from collections.abc import Iterator

    from pytest_django_ifactory.ifactory import InstanceFactory


@pytest.fixture(params=["ifactory", "transactional_ifactory"])
def ifactory(request: pytest.FixtureRequest) -> InstanceFactory:
    return request.getfixturevalue(request.param)  # type: ignore[no-any-return]


def test_all_fields(ifactory: InstanceFactory) -> None:
    instance = ifactory.create(AllFieldsModel)
    for field in instance._meta.get_fields():
        assert getattr(instance, field.name) is not None


def test_initialization(ifactory: InstanceFactory) -> None:
    assert hasattr(ifactory, "testapp")
    assert hasattr(ifactory.testapp, "modela")
    assert hasattr(ifactory.testapp, "modelb")
    assert isinstance(ifactory.testapp.modela().name, str)
    b = ifactory.testapp.modelb()
    assert isinstance(b.name, str)
    assert isinstance(b.required_a, ModelA)
    assert b.nullable_a1 is None
    assert b.nullable_a2 is None


def test_blank_default(ifactory: InstanceFactory) -> None:
    a = ifactory.create(ModelA)
    assert not a.blank


def test_create_with_attrs(ifactory: InstanceFactory) -> None:
    assert ifactory.create(ModelA, name="foo").name == "foo"


def test_create_with_model_attr(ifactory: InstanceFactory) -> None:
    c = ifactory.create(ModelC, model="a field named model")
    assert c.model == "a field named model"


class TestConfigure:
    @pytest.fixture
    def cifactory(self, ifactory: InstanceFactory) -> Iterator[InstanceFactory]:
        original_defaults = copy.deepcopy(ifactory._defaults)
        yield ifactory
        type(ifactory)._defaults = original_defaults

    @pytest.mark.parametrize("model", ["testapp.modelb", ModelB])
    def test_primitive(
        self, cifactory: InstanceFactory, model: str | type[ModelB]
    ) -> None:
        cifactory.configure_defaults(model, name="foo")
        b = cifactory.create(ModelB)
        assert b.name == "foo"

    def test_callable(self, cifactory: InstanceFactory) -> None:
        cifactory.configure_defaults("testapp.modela", name=lambda: "foo")
        assert cifactory.create(ModelA).name == "foo"

    @pytest.mark.parametrize("model", ["testapp.NoModel", "noapp.NoModel"])
    def test_invalid_model(self, cifactory: InstanceFactory, model: str) -> None:
        with pytest.raises(LookupError):
            cifactory.configure_defaults(model)

    def test_create(self, cifactory: InstanceFactory) -> None:
        cifactory.configure_defaults("testapp.modelb", nullable_a1=cifactory.Create)
        assert isinstance(cifactory.create(ModelB).nullable_a1, ModelA)

    def test_create_with_attrs(self, cifactory: InstanceFactory) -> None:
        cifactory.configure_defaults(
            "testapp.modelb", nullable_a1=cifactory.Create(name="foo")
        )
        instance = cifactory.create(ModelB)
        assert instance.nullable_a1
        assert instance.nullable_a1.name == "foo"

    def test_lookup(self, cifactory: InstanceFactory) -> None:
        ModelA.objects.create(name="foo")
        ModelA.objects.create(name="bar")
        cifactory.configure_defaults("testapp.modelb", nullable_a1=cifactory.Lookup)
        instance = cifactory.create(ModelB)
        assert instance.nullable_a1
        assert instance.nullable_a1.name == "foo"

    def test_lookup_with_attrs(self, cifactory: InstanceFactory) -> None:
        ModelA.objects.create(name="foo")
        cifactory.configure_defaults(
            "testapp.modelb", nullable_a1=cifactory.Lookup(name="foo")
        )
        instance = cifactory.create(ModelB)
        assert instance.nullable_a1
        assert instance.nullable_a1.name == "foo"

    def test_unique(self, cifactory: InstanceFactory) -> None:
        cifactory.configure_defaults("testapp.modela", category=cifactory.Unique)
        instance1 = cifactory.create(ModelA)
        instance2 = cifactory.create(ModelA)
        assert instance1.category != instance2.category

    def test_configure_model_attr(self, cifactory: InstanceFactory) -> None:
        cifactory.configure_defaults("testapp.modelc", model="model default")
        instance = cifactory.create(ModelC)
        assert instance.model == "model default"

    def test_plugin(self, cifactory: InstanceFactory) -> None:
        cifactory.configure_defaults("testapp.ModelA", name="adam")
        cifactory.configure_defaults(
            "testapp.ModelB", name="bert", nullable_a1=cifactory.Create
        )

        a = cifactory.create(ModelA, name="alan")
        assert ModelA.objects.count() == 1
        assert a.name == "alan"
        b = cifactory.create(ModelB, required_a=a)
        assert ModelB.objects.count() == 1
        assert ModelA.objects.count() == 2
        assert b.name == "bert"
        assert b.required_a is a
        assert isinstance(b.nullable_a1, ModelA)
        assert b.nullable_a1.name == "adam"
        assert b.nullable_a2 is None
