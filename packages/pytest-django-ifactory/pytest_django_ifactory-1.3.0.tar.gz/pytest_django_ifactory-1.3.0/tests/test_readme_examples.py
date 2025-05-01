"""Test cases for the code examples in the README."""

from __future__ import annotations

from itertools import groupby
from operator import methodcaller
from typing import TYPE_CHECKING

from django.contrib.auth.models import User

if TYPE_CHECKING:
    import pytest

    from pytest_django_ifactory import InstanceFactory


def get_duplicate_names() -> list[str]:
    all_users = User.objects.order_by("last_name", "first_name")
    users_by_name = groupby(all_users, methodcaller("get_full_name"))
    return [full_name for full_name, users in users_by_name if len(list(users)) > 1]


def test_get_duplicate_names(ifactory: InstanceFactory) -> None:
    ifactory.create(User, first_name="Albert", last_name="Einstein")
    ifactory.create(User, first_name="Albert", last_name="Einstein")
    ifactory.create(User, first_name="Erwin", last_name="Schrodinger")
    ifactory.create(User, first_name="Richard", last_name="Feynman")
    assert get_duplicate_names() == ["Albert Einstein"]
    assert User.objects.count() == 4


def test_register_and_create(django_pytester: pytest.Pytester) -> None:
    django_pytester.makeconftest(
        """
        def pytest_django_ifactory_configure(ifactory):
            ifactory.configure_defaults("auth.user", {
                "first_name": "Albert",
                "last_name": "Einstein",
            })
        """
    )
    django_pytester.makepyfile(
        """
        def test_albert_by_default(ifactory):
            albert = ifactory.auth.user()
            assert albert.get_full_name() == "Albert Einstein"
            not_albert = ifactory.auth.user(first_name="Erwin", last_name="Schrodinger")
            assert not_albert.get_full_name() == "Erwin Schrodinger"
       """
    )
    result = django_pytester.runpytest_subprocess("--ds=djangosettings", "-v")
    result.assert_outcomes(passed=1)
