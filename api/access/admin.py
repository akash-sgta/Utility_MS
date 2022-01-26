# --------------------------------------------------------------------------
# DOCUMENTATION
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# LIRARY
# --------------------------------------------------------------------------
from django.contrib import admin
from django.utils.html import format_html
from access.models import Identity
from utility.extra.pool import epochms2datetime

# --------------------------------------------------------------------------
# CODE
# ---------------------------------------------------------------------------
@admin.register(Identity)
class IdentityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "cr_date", "is_active", "is_admin")
    list_display_links = ("id", "name", "email", "cr_date", "is_active", "is_admin")
    ordering = ["-is_active", "-is_admin", "name"]
    search_fields = ["name", "email"]
    empty_value_display = "NULL"
    list_per_page = 25

    def cr_date(self, obj):
        return f"{epochms2datetime(obj.created_on)}"
