# =========================================================================================
#                                       DOCUMENTATION
# =========================================================================================

# =========================================================================================
#                                       LIBRARY
# =========================================================================================
from django.contrib import admin

# -----------------------------------------
from utilUtilities.models import Country, State, City, Mailer, Notification
from utilUtilities.views.utility.utility import Utility
from utilUtilities.views.utility.constant import Constant


# =========================================================================================
#                                       CONSTANT
# =========================================================================================


# =========================================================================================
#                                       CODE
# =========================================================================================
@admin.register(Country)
class Country_AdminPanel(admin.ModelAdmin):

    list_display = (
        "id",
        "isd",
        "iso",
        "name",
        "updated_on",
    )
    list_display_links = (
        "id",
        "isd",
        "iso",
        "name",
        "updated_on",
    )
    ordering = ("name",)
    search_fields = ("name", "iso", "isd")
    empty_value_display = "NULL"
    list_per_page = 25

    def updated_on(self, obj):
        return Utility.epochMsToDatetime(obj.last_update)

    def get_queryset(self, request):
        query = super(Country_AdminPanel, self).get_queryset(request)
        filtered_query = query.filter(sys=Constant.SETTINGS_SYSTEM)
        return filtered_query


@admin.register(State)
class State_AdminPanel(admin.ModelAdmin):

    list_display = (
        "id",
        "country_name",
        "name",
        "updated_on",
    )
    list_display_links = (
        "id",
        "country_name",
        "name",
        "updated_on",
    )
    ordering = ("country", "name")
    search_fields = ["name"]
    empty_value_display = "NULL"
    list_per_page = 25

    def updated_on(self, obj):
        return Utility.epochMsToDatetime(obj.last_update)

    def country_name(self, obj):
        if obj.country in Constant.NULL:
            _return = None
        else:
            _return = obj.country.name
        return _return

    def get_queryset(self, request):
        query = super(State_AdminPanel, self).get_queryset(request)
        filtered_query = query.filter(sys=Constant.SETTINGS_SYSTEM)
        return filtered_query


@admin.register(City)
class City_AdminPanel(admin.ModelAdmin):

    list_display = (
        "id",
        "state_name",
        "name",
        "updated_on",
    )
    list_display_links = (
        "id",
        "state_name",
        "name",
        "updated_on",
    )
    ordering = ("state__country__name", "state__name", "name")
    search_fields = ["name"]
    empty_value_display = "NULL"
    list_per_page = 25

    def updated_on(self, obj):
        return Utility.epochMsToDatetime(obj.last_update)

    def state_name(self, obj):
        if obj.state in Constant.NULL:
            _return = None
        else:
            _return = obj.state.name
        return _return

    def get_queryset(self, request):
        query = super(City_AdminPanel, self).get_queryset(request)
        filtered_query = query.filter(sys=Constant.SETTINGS_SYSTEM)
        return filtered_query


# -----------------------------------------
@admin.register(Mailer)
class Mailer_AdminPanel(admin.ModelAdmin):

    list_display = (
        "id",
        "api",
        "subject",
        "status",
        "updated_on",
    )
    list_display_links = (
        "id",
        "api",
        "subject",
        "status",
        "updated_on",
    )
    ordering = ("api", "status")
    search_fields = ["subject"]
    empty_value_display = "NULL"
    list_per_page = 25

    def updated_on(self, obj):
        return Utility.epochMsToDatetime(obj.last_update)

    def get_queryset(self, request):
        query = super(City_AdminPanel, self).get_queryset(request)
        filtered_query = query.filter(sys=Constant.SETTINGS_SYSTEM)
        return filtered_query


@admin.register(Notification)
class Notificaiton_AdminPanel(admin.ModelAdmin):

    list_display = (
        "id",
        "api",
        "subject",
        "status",
        "updated_on",
    )
    list_display_links = (
        "id",
        "api",
        "subject",
        "status",
        "updated_on",
    )
    ordering = ("api", "status")
    search_fields = ["subject"]
    empty_value_display = "NULL"
    list_per_page = 25

    def updated_on(self, obj):
        return Utility.epochMsToDatetime(obj.last_update)

    def get_queryset(self, request):
        query = super(City_AdminPanel, self).get_queryset(request)
        filtered_query = query.filter(sys=Constant.SETTINGS_SYSTEM)
        return filtered_query
