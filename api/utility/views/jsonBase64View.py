# --------------------------------------------------------------------------
# DOCUMENTATION
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# LIRARY
# --------------------------------------------------------------------------
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from utility.extra.pool import b64ToDict, dictTob64

# --------------------------------------------------------------------------
# CONSTANTS
# --------------------------------------------------------------------------
B64 = "B64"

# --------------------------------------------------------------------------
# CODE
# --------------------------------------------------------------------------
@api_view(["POST"])
def jsonToBase64(request):
    data = request.data
    if len(data.keys()) == 0:
        return_data = {"B64": None}
        return_status = status.HTTP_400_BAD_REQUEST
    else:
        try:
            data = dictTob64(data)
            return_data = {"B64": data}
            return_status = status.HTTP_201_CREATED
        except:
            return_data = {"B64": None}
            return_status = status.HTTP_400_BAD_REQUEST
    return JsonResponse(data=return_data, status=return_status)


@api_view(["POST"])
def base64ToJson(request):
    data = request.data
    if len(data.keys()) == 0:
        return_data = {"JSON": None}
        return_status = status.HTTP_400_BAD_REQUEST
    else:
        try:
            data = b64ToDict(data[B64])
            return_data = {"JSON": data}
            return_status = status.HTTP_201_CREATED
        except:
            return_data = {"JSON": None}
            return_status = status.HTTP_400_BAD_REQUEST
    return JsonResponse(data=return_data, status=return_status)
