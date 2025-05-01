"""Unit and regression tests for the pytest-django-ifactory plugin."""

import pytest


def test_register_and_create(django_pytester: pytest.Pytester) -> None:
    django_pytester.makeconftest(
        """
        def pytest_django_ifactory_configure(ifactory):
            ifactory.configure_defaults('testapp.modela', {
                'name': 'adam',
            })
            ifactory.configure_defaults('testapp.modelb', {
                'name': 'bert',
                'nullable_a1': ifactory.Create,
            })
    """
    )
    django_pytester.makepyfile(
        """
        import pytest
        from testapp.models import ModelA, ModelB

        def test_create(ifactory):
            a = ifactory.testapp.modela(name='alan')
            assert ModelA.objects.count() == 1
            assert a.name == 'alan'
            b = ifactory.testapp.modelb(required_a=a)
            assert ModelA.objects.count() == 2
            assert ModelB.objects.count() == 1
            assert b.name == 'bert'
            assert b.required_a is a
            assert isinstance(b.nullable_a1, ModelA)
            assert b.nullable_a1.name == 'adam'
            assert b.nullable_a2 is None

        def test_create_with_transactional_ifactory(transactional_ifactory):
            a = transactional_ifactory.testapp.modela(name='alan')
            assert ModelA.objects.count() == 1
            assert a.name == 'alan'
            b = transactional_ifactory.testapp.modelb(required_a=a)
            assert ModelA.objects.count() == 2
            assert ModelB.objects.count() == 1
            assert b.name == 'bert'
            assert b.required_a is a
            assert isinstance(b.nullable_a1, ModelA)
            assert b.nullable_a1.name == 'adam'
            assert b.nullable_a2 is None
    """
    )
    result = django_pytester.runpytest_subprocess("--ds=djangosettings", "-v")
    result.assert_outcomes(passed=2)
