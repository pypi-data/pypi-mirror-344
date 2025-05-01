"""Test configuration for pytest-django-ifactory."""

from __future__ import annotations

import os
import shutil
from pathlib import Path

import pytest
from django.conf import settings

pytest_plugins = ["pytester"]


def pytest_configure() -> None:
    settings.configure(
        DATABASES={"default": {"ENGINE": "django.contrib.gis.db.backends.spatialite"}},
        SPATIALITE_LIBRARY_PATH=os.environ.get("SPATIALITE_LIBRARY_PATH"),
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.gis",
            "testapp",
        ],
        USE_TZ=True,
    )


@pytest.fixture
def django_pytester(pytester: pytest.Pytester) -> pytest.Pytester:
    cwd = Path(__file__).parent
    shutil.copy(cwd / "djangosettings.py", pytester.path)
    shutil.copytree(cwd / "testapp", pytester.path / "testapp")
    return pytester
