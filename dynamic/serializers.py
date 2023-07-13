from rest_framework import serializers


class TableSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=["str", "int", "bool"])
    name = serializers.CharField()


def dynamic_model_serializer(model):
    Meta = type("Meta", (), {"model": model, "fields": "__all__"})
    return type(
        "DynamicModelSerializer", (serializers.ModelSerializer,), {"Meta": Meta}
    )
