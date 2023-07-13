from django.db import models
from django.apps import apps

from rest_framework import fields, serializers

app_config = apps.get_app_config("dynamic")


def get_field(field_type: str) -> models.Field:
    """Returns model field base on the provided type string

    Args:
        field_type (str): provided type in string format

    Returns:
        models.Field: field type
    """

    match field_type:
        case "str":
            return models.CharField(max_length=255)
        case "int":
            return models.IntegerField()
        case "bool":
            return models.BooleanField()


def get_field_serializer(field_type: models.Field) -> fields.Field:
    """Returns model field base on the provided type string

    Args:
        field_type (str): provided type in string format

    Returns:
        models.Field: field type
    """

    match field_type:
        case models.CharField:
            return serializers.CharField()
        case models.IntegerField:
            return serializers.IntegerField()
        case models.BooleanField:
            return serializers.BooleanField()
