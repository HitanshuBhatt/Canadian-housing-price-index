from django.contrib import admin
from .models import HousingData

#  register housing data model
@admin.register(HousingData)
class HousingDataAdmin(admin.ModelAdmin):
    #  show columns in admin table view 
    list_display = ("date", "geo", "category", "value")
    #  add filter on the right side in admin panel 
    list_filter = ("geo", "category", "date")
    #  add serach fieled
    search_fields = ("geo", "category")
    #  show latest data first with date first 
    ordering = ("-date", "geo")