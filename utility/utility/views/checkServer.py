# =========================================================================================
#                                       DOCUMENTATION
# =========================================================================================


# =========================================================================================
#                                       LIBRARY
# =========================================================================================
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from datetime import datetime
from django.conf import settings

from utilUtilities.views.utility.utility import Utility


# =========================================================================================
#                                       CONSTANT
# =========================================================================================

# =========================================================================================
#                                       CODE
# =========================================================================================
@api_view(["GET"])
def check_server_status(request):
    data = {
        "SERVER NAME": settings.SERVER_NAME,
        "SERVER TIME": Utility.datetimeToStr(datetime.now()),
        "SERVER TIMEZONE": settings.TIME_ZONE,
    }
    return JsonResponse(data=data, status=status.HTTP_200_OK)
