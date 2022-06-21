# =========================================================================================
#                                       DOCUMENTATION
# =========================================================================================

# =========================================================================================
#                                       LIBRARY
# =========================================================================================
from django.contrib import admin

# -------------------------------------------------

from api.models import Request, Api
from utilities.util.utility import Utility


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
        "updated",
    )
    list_display_links = (
        "id",
        "email",
        "phone",
        "telegram",
        "status",
        "updated",
    )
    ordering = ("status", "created_on")
    search_fields = ["email", "phone_no"]
    empty_value_display = "NULL"
    list_per_page = 25

    def telegram(self, obj):
        return obj.tg_id

    def phone(self, obj):
        if obj.isd == NULL:
            _return = f"{obj.phone_no}"
        else:
            _return = f"+{obj.isd}-{obj.phone_no}"
        return _return

    def updated(self, obj):
        return Utility.epochMsToDatetime(obj.last_update)


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
