"""Pytest plugin module."""

from __future__ import annotations

import pytest

from .ifactory import InstanceFactory


class PytestDjangoIFactorySpec:
    """Hook specification namespace for this plugin."""

    def pytest_django_ifactory_configure(self, ifactory: type[InstanceFactory]) -> None:
        """Configure model field defaults at the pytest instance factory."""


def pytest_addhooks(pluginmanager: pytest.PytestPluginManager) -> None:
    pluginmanager.add_hookspecs(PytestDjangoIFactorySpec)


@pytest.fixture(autouse=True, scope="session")
def _django_ifactory_register(request: pytest.FixtureRequest) -> None:
    request.config.pluginmanager.hook.pytest_django_ifactory_configure(
        ifactory=InstanceFactory
    )


@pytest.fixture
def ifactory(db: None) -> InstanceFactory:  # noqa: ARG001
    return InstanceFactory()


@pytest.fixture
def transactional_ifactory(transactional_db: None) -> InstanceFactory:  # noqa: ARG001
    return InstanceFactory()
