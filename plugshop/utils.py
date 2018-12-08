from django.core.cache import cache
from django.apps import apps
from django.conf import settings
from importlib import import_module


def load_class(path):
    module_path, class_name = path.rsplit('.', 1)
    module = import_module(module_path)
    cl = getattr(module, class_name)
    return cl


def serialize_model(instance):
    data = {}
    for field in instance._meta.fields:
        data[field.name] = field.value_to_string(instance)
    return data


def serialize_queryset(queryset):
    return [serialize_model(item) for item in queryset]


def get_categories(*args, **kwargs):
    categories = cache.get('plugshop_categories')
    if categories is None:
        categories = apps.get_model(settings.CATEGORY_MODEL).objects.all()
        cache.set('plugshop_categories', categories)
    return categories
