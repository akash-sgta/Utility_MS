# --------------------------------------------------------------------------
# DOCUMENTATION
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# LIRARY
# --------------------------------------------------------------------------
from django.urls import re_path
from access.views.accessView import AccessView


# --------------------------------------------------------------------------
# CONSTANTS
# --------------------------------------------------------------------------
app_name = "access"

# --------------------------------------------------------------------------
# CODE
# --------------------------------------------------------------------------
urlpatterns = [
    re_path(r"^api/(?P<pk>\d*)", AccessView.as_view(), name="API_ACCESS"),
]
