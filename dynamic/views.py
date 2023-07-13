from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import models, connection
from django.db.models.base import ModelBase
from django.contrib.contenttypes.models import ContentType

from dynamic.serializers import TableSerializer, dynamic_model_serializer
from dynamic.models import DynamicRelation, ModelPopulator
from dynamic.utils import get_field


@api_view(["GET"])
def tables_get(request, id):
    try:
        dynamicModel = DynamicRelation.objects.get(
            object_id=id
        ).content_type.model_class()
        results = dynamic_model_serializer(dynamicModel)(
            dynamicModel.objects.all(), many=True
        )
        return Response(results.data)
    except Exception:
        return Response({"message": "No model found with provided id"})


@api_view(["POST"])
def table_add(request, id):
    if request.method == "POST":
        try:
            dynamicModel = DynamicRelation.objects.get(
                object_id=id
            ).content_type.model_class()
            serializer = dynamic_model_serializer(dynamicModel)(data=request.data)
            if serializer.is_valid():
                data = serializer.data
                dynamicModel.objects.create(**data)
                return Response(
                    {
                        "message": f"New table row successfully created for {dynamicModel.__name__}"
                    }
                )
            else:
                return Response({"message": "Something went wrong"})
        except Exception:
            return Response({"message": "Something went wrong"})


@api_view(["POST"])
def table_create(request):
    if request.method == "POST":
        serializer = TableSerializer(data=request.data, many=True)
        if serializer.is_valid():
            new_id = getattr(DynamicRelation.objects.last(), "object_id", 0) + 1
            model_name = f"DynamicModel{new_id}"
            data = {
                field["name"]: get_field(field["type"]) for field in serializer.data
            }
            ModelPopulator.objects.create(
                name=model_name,
                fields={field["name"]: field["type"] for field in serializer.data},
            )
            for field in data.values():
                field.null = True
            newModel = ModelBase.__new__(
                ModelBase,
                model_name,
                (models.Model,),
                {"__module__": "dynamic.models", **data},
            )
            with connection.schema_editor() as schema:
                schema.create_model(newModel)
            contenttype = ContentType.objects.create(
                app_label="dynamic", model=model_name.lower()
            )
            DynamicRelation.objects.create(
                tag=model_name.lower(),
                content_type=contenttype,
                object_id=new_id,
            )
            return Response(
                {"message": f"New model successfully created with id {new_id}"}
            )
        else:
            return Response(serializer.errors, status=400)


@api_view(["PUT"])
def table_update(request, id):
    if request.method == "PUT":
        serializer = TableSerializer(data=request.data, many=True)
        if serializer.is_valid():
            data = {
                field["name"]: get_field(field["type"]) for field in serializer.data
            }
            for k, v in data.items():
                v.name = k
                v.column = k
            updated_fields = [field for field in data.values()]
            dynamicModel = DynamicRelation.objects.get(
                object_id=id
            ).content_type.model_class()

            added_fields = [
                f
                for f in updated_fields
                if (f.name, f.__class__)
                not in [(f.name, f.__class__) for f in dynamicModel._meta.fields]
            ]
            deleted_fields = [
                f
                for f in dynamicModel._meta.fields
                if (
                    (f.name, f.__class__)
                    not in [(f.name, f.__class__) for f in updated_fields]
                    and f.name != "id"
                )
            ]

            ModelPopulator.objects.filter(name=dynamicModel.__name__).update(
                fields={field["name"]: field["type"] for field in serializer.data}
            )
            with connection.schema_editor() as schema:
                try:
                    [
                        schema.remove_field(dynamicModel, field)
                        for field in deleted_fields
                    ]
                except Exception:
                    ...
                try:
                    [schema.add_field(dynamicModel, field) for field in added_fields]
                except Exception:
                    ...
            return Response({"message": f"Successfully updated model with id {id}"})
        else:
            return Response(serializer.errors, status=400)
