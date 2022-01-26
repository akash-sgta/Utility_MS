# --------------------------------------------------------------------------
# DOCUMENTATION
# --------------------------------------------------------------------------
"""api URL Configuration

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

# --------------------------------------------------------------------------
# LIRARY
# --------------------------------------------------------------------------
from django.conf import settings
from django.urls import include, re_path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.static import serve
from api.views.checkServer import check_server_status


# --------------------------------------------------------------------------
# CODE
# --------------------------------------------------------------------------
urlpatterns = [
    re_path(r"^api-admin/", admin.site.urls, name="DJANGO_ADMIN"),
    # ----------------------------------------------------------
    re_path(r"^checkserver/", check_server_status, name="CHECK_SERVER_STATUS"),
    re_path(r"^access/", include("access.urls"), name="API_ACCESS_HEADER"),
    re_path(r"^utility/", include("utility.urls"), name="UTILITIES_HEADER"),
]
