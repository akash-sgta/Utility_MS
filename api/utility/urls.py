# --------------------------------------------------------------------------
# DOCUMENTATION
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# LIRARY
# --------------------------------------------------------------------------
from django.urls import re_path
from utility.views.jsonBase64View import jsonToBase64, base64ToJson


# --------------------------------------------------------------------------
# CONSTANTS
# --------------------------------------------------------------------------
app_name = "utility"

# --------------------------------------------------------------------------
# CODE
# --------------------------------------------------------------------------
urlpatterns = [
    re_path(r"^j2b/", jsonToBase64, name="JSON_TO_B64"),
    re_path(r"^b2j/", base64ToJson, name="B64_TO_JSON"),
    # re_path(r"^country/(?P<pk>\d*)", Country_View.as_view(), name="COUNTRY"),
    # re_path(r"^state/(?P<pk>\d*)/(?P<pkk>\d*)", State_View.as_view(), name="STATE"),
    # re_path(r"^city/(?P<pk>\d*)/(?P<pkk>\d*)", City_View.as_view(), name="CITY"),
    # re_path(r"^mass/(?P<word>\w*)", Mass_View.as_view(), name="MASS_UPLOAD"),
]
