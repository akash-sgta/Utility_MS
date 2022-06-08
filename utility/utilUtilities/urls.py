# =========================================================================================
#                                       DOCUMENTATION
# =========================================================================================

# =========================================================================================
#                                       LIBRARY
# =========================================================================================
from django.urls import re_path

# --------------------------------------------------
from utilUtilities.views.country import (
    CountryView_asUser,
    CountryView_asAdmin,
)
from utilUtilities.views.state import (
    StateView_asUser,
    StateView_asAdmin,
)
from utilUtilities.views.city import (
    CityView_asUser,
    CityView_asAdmin,
)
from utilUtilities.views.mailer import (
    MailerView_asUser,
    MailerView_asAdmin,
)
from utilUtilities.views.notification import (
    NotificationView_asUser,
    NotificationView_asAdmin,
)

# =========================================================================================
#                                       CONSTANT
# =========================================================================================
app_name = "utilUtilities"
# --------------------------------------------------
WORD = r"(search|id){0,1}"
PK = r"[A-Za-z0-9_@,\s]*"
# --------------------------------------------------


# =========================================================================================
#                                       CODE
# =========================================================================================
urlpatterns = [
    re_path(
        rf"u/country/(?P<word>{WORD})/(?P<pk>{PK})",
        CountryView_asUser.as_view(),
        name="COUNTRY_AS_USER",
    ),
    re_path(
        rf"a/country/(?P<word>{WORD})/(?P<pk>{PK})",
        CountryView_asAdmin.as_view(),
        name="COUNTRY_AS_ADMIN",
    ),
    # --------------------------------------------------
    re_path(
        rf"u/state/(?P<word>{WORD})/(?P<pk>{PK})",
        StateView_asUser.as_view(),
        name="STATE_AS_USER",
    ),
    re_path(
        rf"a/state/(?P<word>{WORD})/(?P<pk>{PK})",
        StateView_asAdmin.as_view(),
        name="STATE_AS_ADMIN",
    ),
    # --------------------------------------------------
    re_path(
        rf"u/city/(?P<word>{WORD})/(?P<pk>{PK})",
        CityView_asUser.as_view(),
        name="CITY_AS_USER",
    ),
    re_path(
        rf"a/city/(?P<word>{WORD})/(?P<pk>{PK})",
        CityView_asAdmin.as_view(),
        name="CITY_AS_ADMIN",
    ),
    # --------------------------------------------------
    re_path(
        rf"u/city/(?P<word>{WORD})/(?P<pk>{PK})",
        CityView_asUser.as_view(),
        name="CITY_AS_USER",
    ),
    re_path(
        rf"a/city/(?P<word>{WORD})/(?P<pk>{PK})",
        CityView_asAdmin.as_view(),
        name="CITY_AS_ADMIN",
    ),
    # --------------------------------------------------
    re_path(
        rf"u/mailer/(?P<word>{WORD})/(?P<pk>{PK})",
        MailerView_asUser.as_view(),
        name="MAILER_AS_USER",
    ),
    re_path(
        rf"a/mailer/(?P<word>{WORD})/(?P<pk>{PK})",
        MailerView_asAdmin.as_view(),
        name="MAILER_AS_ADMIN",
    ),
    # --------------------------------------------------
    re_path(
        rf"u/mailer/(?P<word>{WORD})/(?P<pk>{PK})",
        NotificationView_asUser.as_view(),
        name="NOTIFICATION_AS_USER",
    ),
    re_path(
        rf"a/mailer/(?P<word>{WORD})/(?P<pk>{PK})",
        NotificationView_asAdmin.as_view(),
        name="NOTIFICATION_AS_ADMIN",
    ),
]