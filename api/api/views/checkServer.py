# --------------------------------------------------------------------------
# DOCUMENTATION
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# LIRARY
# --------------------------------------------------------------------------
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from api.settings import TIME_ZONE as TZ

# --------------------------------------------------------------------------
# CODE
# --------------------------------------------------------------------------
@api_view(["GET"])
def check_server_status(request):
    date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    message = f"| Server Name : UTILITY"
    message += f" | Server Time : {date}"
    message += f" | Server Timezone : {TZ} | "
    return Response(data=message, status=status.HTTP_200_OK)
