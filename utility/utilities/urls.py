# =========================================================================================
#                                       DOCUMENTATION
# =========================================================================================

# =========================================================================================
#                                       LIBRARY
# =========================================================================================
from django.urls import re_path

# --------------------------------------------------
from utilities.views.country import (
    CountryView_asUser,
    CountryView_asAdmin,
)
from utilities.views.state import (
    StateView_asUser,
    StateView_asAdmin,
)
from utilities.views.city import (
    CityView_asUser,
    CityView_asAdmin,
)
from utilities.views.mailer import (
    MailerView_asUser,
    MailerView_asAdmin,
)
from utilities.views.notification import (
    NotificationView_asUser,
    NotificationView_asAdmin,
)

# =========================================================================================
#                                       CONSTANT
# =========================================================================================
app_name = "utilities"
# --------------------------------------------------
WORD = r"(search|id){1}"
ID = r"(id){1}"
PK = r"[A-Za-z0-9_@,\s]*"
WORD_2 = r"(search|id|trigger){1}"
WORD_3 = r"(search|id|trigger|bot){1}"
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
        rf"u/mailer/(?P<word>{ID})/(?P<pk>{PK})",
        MailerView_asUser.as_view(),
        name="MAILER_AS_USER",
    ),
    re_path(
        rf"a/mailer/(?P<word>{WORD_2})/(?P<pk>{PK})",
        MailerView_asAdmin.as_view(),
        name="MAILER_AS_ADMIN",
    ),
    # --------------------------------------------------
    re_path(
        rf"u/notif/(?P<word>{ID})/(?P<pk>{PK})",
        NotificationView_asUser.as_view(),
        name="NOTIFICATION_AS_USER",
    ),
    re_path(
        rf"a/notif/(?P<word>{WORD_3})/(?P<pk>{PK})",
        NotificationView_asAdmin.as_view(),
        name="NOTIFICATION_AS_ADMIN",
    ),
]
