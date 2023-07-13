from django.contrib import admin
from dynamic.models import DynamicRelation, ModelPopulator


@admin.register(DynamicRelation)
class DynamicAdmin(admin.ModelAdmin):
    pass


@admin.register(ModelPopulator)
class PopulatorAdmin(admin.ModelAdmin):
    pass
