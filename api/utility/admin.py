# --------------------------------------------------------------------------
# DOCUMENTATION
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# LIRARY
# --------------------------------------------------------------------------
from django.contrib import admin
from utility.models import Country, State, City


# --------------------------------------------------------------------------
# CODE
# ---------------------------------------------------------------------------
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("id", "iso", "isd", "name")
    list_display_links = ("id", "iso", "isd", "name")
    ordering = ["name"]
    search_fields = ["name"]
    empty_value_display = "NULL"
    list_per_page = 25


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ("id", "country_id", "name")
    list_display_links = ("id", "country_id", "name")
    ordering = ["country_id", "name"]
    search_fields = ["name"]
    empty_value_display = "NULL"
    list_per_page = 25


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("id", "state_id", "name")
    list_display_links = ("id", "state_id", "name")
    ordering = ["state_id", "name"]
    search_fields = ["name"]
    empty_value_display = "NULL"
    list_per_page = 25
