from django.apps import AppConfig
from django.db.models.base import ModelBase
from django.db.models import Model


class TablesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dynamic"

    def ready(self):
        from dynamic.models import ModelPopulator
        from dynamic.utils import get_field

        for model in ModelPopulator.objects.all():
            data = {k: get_field(v) for k, v in model.fields.items()}
            ModelBase.__new__(
                ModelBase,
                model.name,
                (Model,),
                {"__module__": "dynamic.models", **data},
            )
