# =========================================================================================
#                                       DOCUMENTATION
# =========================================================================================

# =========================================================================================
#                                       LIBRARY
# =========================================================================================
from django.contrib import admin

# -------------------------------------------------

from api.models import Request, Api
from utilities.views.utility.utility import Utility


# =========================================================================================
#                                       CONSTANT
# =========================================================================================
NULL = (None, "", 0)

# =========================================================================================
#                                       CODE
# =========================================================================================
@admin.register(Request)
class Request_AdminPanel(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "phone",
        "telegram",
        "status",
        "creation",
    )
    list_display_links = (
        "id",
        "email",
        "phone",
        "telegram",
        "status",
        "creation",
    )
    ordering = ("status", "created_on")
    search_fields = ["email", "phone_no"]
    empty_value_display = "NULL"
    list_per_page = 25

    def telegram(self, obj):
        if obj.tg_id in NULL:
            _return = False
        else:
            _return = True
        return _return

    def phone(self, obj):
        if obj.country in NULL:
            _return = f"{obj.phone_no}"
        else:
            _return = f"+{obj.country.isd}-{obj.phone_no}"
        return _return

    def creation(self, obj):
        return Utility.epochMsToDatetime(obj.created_on)


@admin.register(Api)
class Api_AdminPanel(admin.ModelAdmin):
    list_display = (
        "id",
        "direction",
        "email",
        "name",
        "updated",
    )
    list_display_links = (
        "id",
        "direction",
        "email",
        "name",
        "updated",
    )
    ordering = ("direction", "name")
    search_fields = ("name", "email", "phone_no")
    empty_value_display = "NULL"
    list_per_page = 25

    def updated(self, obj):
        return Utility.epochMsToDatetime(obj.last_update)
