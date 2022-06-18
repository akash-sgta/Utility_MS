# =========================================================================================
#                                       DOCUMENTATION
# =========================================================================================


# =========================================================================================
#                                       LIBRARY
# =========================================================================================
from copy import deepcopy
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from datetime import datetime

from utilities.views.utility.utility import Utility
from utilities.views.utility.constant import Constant


# =========================================================================================
#                                       CONSTANT
# =========================================================================================
GET = "GET"
# =========================================================================================
#                                       CODE
# =========================================================================================
@api_view([GET])
def check_server_status(request):
    data = deepcopy(Constant.RETURN_JSON)
    data[Constant.STATUS] = True
    data[Constant.DATA] = {
        "SERVER NAME": Constant.SETTINGS_SYSTEM_NAME,
        "SERVER TIME": Utility.datetimeToStr(datetime.now()),
        "SERVER TIMEZONE": Constant.SETTINGS_TIMEZONE,
    }
    return JsonResponse(data=data, status=status.HTTP_200_OK)
