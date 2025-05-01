"""Untyped unit and regression tests for the instance factory class.

This tests the older API that doesn't work well with static type
checking.

"""

from testapp.models import ModelA, ModelB


def test_create(ifactory):
    instance_a = ifactory.testapp.modela(name="model a")
    assert isinstance(instance_a, ModelA)
    assert instance_a.name == "model a"
    instance_b = ifactory.testapp.modelb(name="model b")
    assert isinstance(instance_b, ModelB)
    assert instance_b.name == "model b"


def test_dynamic_method_names(ifactory):
    assert ifactory.testapp.modela.__name__ == "modela"
    assert ifactory.testapp.modelb.__name__ == "modelb"
