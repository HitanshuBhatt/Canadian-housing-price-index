from django.contrib import admin
from .models import HousingData


@admin.register(HousingData)
class HousingDataAdmin(admin.ModelAdmin):
    list_display = ("date", "geo", "category", "value")
    list_filter = ("geo", "category", "date")
    search_fields = ("geo", "category")
    ordering = ("-date", "geo")