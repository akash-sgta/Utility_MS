# =========================================================================================
#                                       DOCUMENTATION
# =========================================================================================
"""
utility URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# =========================================================================================
#                                       LIBRARY
# =========================================================================================
from django.contrib import admin
from django.urls import re_path, include

# --------------------------------
from utility.views.checkServer import check_server_status
from utility.views.token import token

# =========================================================================================
#                                       CONSTANT
# =========================================================================================

# =========================================================================================
#                                       CODE
# =========================================================================================
urlpatterns = [
    re_path(
        r"^django-admin/",
        admin.site.urls,
        name="DJANGO_ADMIN",
    ),
    # ----------------------------------------------------------
    re_path(
        r"^checkserver/",
        check_server_status,
        name="CHECK_SERVER_STATUS",
    ),
    re_path(
        r"^token/(?P<word>(enc){0,1})/(?P<pk>(1|2){1})",
        token,
        name="TOKEN",
    ),
    # ----------------------------------------------------------
    re_path(
        r"^utilities/",
        include("utilities.urls"),
        name="UTILITIES",
    ),
    re_path(
        r"^api/",
        include("api.urls"),
        name="API",
    ),
    # ----------------------------------------------------------
]
