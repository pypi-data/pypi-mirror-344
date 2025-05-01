"""The Django model instance factory."""

from __future__ import annotations

import warnings
from collections.abc import Callable, Iterable, Mapping
from typing import TYPE_CHECKING, Any, ClassVar, TypeVar, cast

from django.apps import apps as django_apps
from django.db import models

from .flags import *  # noqa: F403

if TYPE_CHECKING:
    from django.contrib.contenttypes.fields import GenericForeignKey
    from typing_extensions import TypeGuard

    from .typing import F, FieldSetter


def generate_default_value(field: F, unique: bool = False) -> FieldSetter[Any]:
    # The defaults module's imports use the Django settings so we
    # delay this import as long as possible
    from .defaults import generate_default_value as _generate_default_value

    return _generate_default_value(field, unique)


class ApplicationNamespaceDescriptor:
    """Descriptor for an application namespace on an instance factory.

    Each instance of this class dynamically generates a namespace
    class for the *models* its given.

    """

    def __init__(self, app_models: Iterable[type[models.Model]]) -> None:
        class ApplicationNamespace:
            def __init__(self, ifactory: InstanceFactory) -> None:
                self.ifactory = ifactory

        def make_create(model: type[models.Model]) -> Callable[..., models.Model]:
            def create(self: ApplicationNamespace, **attrs: Any) -> models.Model:
                return self.ifactory.create(model, **attrs)

            create.__name__ = model._meta.model_name  # type: ignore[assignment]
            return create

        for model in app_models:
            if model._meta.model_name:
                setattr(
                    ApplicationNamespace, model._meta.model_name, make_create(model)
                )

        self.namespace_class = ApplicationNamespace

    def __get__(
        self, obj: InstanceFactory, objtype: type[InstanceFactory] | None = None
    ) -> Any:
        return self.namespace_class(obj)


M = TypeVar("M", bound=models.Model)


class InstanceFactory:
    """A factory for Django model instances to use in unit tests."""

    Create = CreateRelatedInstance
    Lookup = LookupRelatedInstance
    Unique = Unique

    # Global defaults for all models in the format
    # {model_label_lower: {field_name: default_value, ...}, ...}.
    _defaults: ClassVar[dict[str, dict[str, Any]]] = {}

    @classmethod
    def register_all_models(cls) -> None:
        """Register all installed models for production at the factory."""
        if not django_apps.ready:
            raise RuntimeError(
                "InstanceFactory.register_models() must be called after Django has "
                "been initialized"
            )
        for app in django_apps.get_app_configs():
            models = list(app.get_models())
            for model in models:
                cls._set_initial_defaults(model)
            setattr(cls, app.label, ApplicationNamespaceDescriptor(models))

    @classmethod
    def _set_initial_defaults(cls, model: type[models.Model]) -> None:
        # Generate initial default values for the fields of a *model*.
        def needs_default(
            field: models.Field | models.ForeignObjectRel | GenericForeignKey,
        ) -> TypeGuard[models.Field]:
            return (
                isinstance(field, models.Field)
                and not field.many_to_many
                and not field.null
                and not field.has_default()
                and not isinstance(field, models.AutoField)
            )

        def generate_default(
            field: models.Field,
        ) -> CreateRelatedInstance | FieldSetter[Any]:
            if field.many_to_one or field.one_to_one:
                return InstanceFactory.Create
            return generate_default_value(field)

        cls._defaults[model._meta.label_lower] = {
            field.name: generate_default(field)
            for field in model._meta.get_fields()
            if needs_default(field)
        }

    @classmethod
    def configure_defaults(
        cls,
        model: str | type[models.Model],
        attrs: dict[str, Any] | None = None,
        /,
        **kwargs: Any,
    ) -> None:
        """Configure the default values for the given *model*.

        *model* can be an actual model class or a model label. *attrs*
        is deprecated. Use keyword arguments to map field names to
        default values.

        """
        if isinstance(attrs, Mapping) and not kwargs:
            warnings.warn(
                "Passing the default field values in a dictionary to "
                "ifactory.configure_defaults() is deprecated. Use kwargs instead.",
                DeprecationWarning,
                stacklevel=2,
            )
            kwargs = attrs
        elif attrs is not None:
            kwargs["attrs"] = attrs

        if isinstance(model, str):
            model = django_apps.get_model(model)
        if not cls._defaults:  # make sure the factory is initialized
            cls.register_all_models()

        def validate_attr(name: str, value: Any) -> Any:
            field = model._meta.get_field(name)
            if not isinstance(field, models.Field):
                raise TypeError(
                    f"Can't configure default value for `{model._meta.label}.{name}` "
                    f"since it's either a reverse or a generic relationship"
                )
            if (is_create(value) or is_lookup(value)) and field.related_model is None:
                raise TypeError(
                    f"Can't create related instance for `{model._meta.label}.{name}` "
                    f"since it's not a field with a related model"
                )
            if is_unique(value):
                value = generate_default_value(field, unique=True)
            return (name, value)

        cls._defaults[model._meta.label_lower].update(
            validate_attr(name, value) for name, value in kwargs.items()
        )

    def __init__(self) -> None:
        if not self._defaults:  # make sure the factory is initialized
            self.register_all_models()

    def create(
        self, model: type[M], attrs: dict[str, Any] | None = None, /, **kwargs: Any
    ) -> M:
        """Create an instance of the given model."""
        if isinstance(attrs, Mapping) and not kwargs:
            warnings.warn(
                "Passing the model instance field values in a dictionary to "
                "ifactory.create() is deprecated. Use kwargs instead.",
                DeprecationWarning,
                stacklevel=2,
            )
            kwargs = attrs
        elif attrs is not None:
            kwargs["attrs"] = attrs

        def get_default_value(name: str, value: Any) -> Any:
            # _set_initial_defaults() and configure_defaults() should
            # make sure that there's only valid attributes
            # (corresponding to models.Field) in self._defaults.  They
            # should also make sure that Create and Lookup defaults
            # have a related model.
            field = cast("models.Field", model._meta.get_field(name))
            if value is self.Create:
                related_model = cast("type[models.Model]", field.related_model)
                value = self.create(related_model)
            elif isinstance(value, self.Create):
                related_model = cast("type[models.Model]", field.related_model)
                value = self.create(related_model, **value.attrs)
            elif value is self.Lookup:
                related_model = cast("type[models.Model]", field.related_model)
                value = related_model._default_manager.first()
            elif isinstance(value, self.Lookup):
                related_model = cast("type[models.Model]", field.related_model)
                value = related_model._default_manager.get(**value.attrs)
            elif callable(value):
                value = value()
            return value

        defaults = {
            k: get_default_value(k, v)
            for k, v in self._defaults[model._meta.label_lower].items()
            if k not in kwargs
        }
        defaults.update(kwargs)
        instance = model(**defaults)
        instance.clean()
        instance.save()
        return instance
