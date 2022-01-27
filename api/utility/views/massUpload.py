# --------------------------------------------------------------------------
# DOCUMENTATION
# --------------------------------------------------------------------------
"""
Mass upload of data related to utility class
POST only
"""

# --------------------------------------------------------------------------
# LIRARY
# --------------------------------------------------------------------------
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from utility.views.countryView import Country_View
from utility.views.stateView import State_View
from utility.views.cityView import City_View
from access.security.authenticate import Authentication
from access.security.authorization import Authorization


# --------------------------------------------------------------------------
# CONSTANTS
# --------------------------------------------------------------------------
from utility.extra.constant import (
    INVALID_FORMATTING,
    COUNTRY,
    STATE,
    CITY,
    ERROR_CRUD_GEN,
)

ERROR = "ERROR"

# --------------------------------------------------------------------------
# CODE
# ---------------------------------------------------------------------------
class Mass_View(APIView):

    renderer_classes = [JSONRenderer]
    authentication_classes = [Authentication]
    permission_classes = [Authorization]

    def __initial(self, request=None, wprd=None):
        self.wprd = None if wprd in (None, "") else wprd.upper()
        self.request = None if request in (None, "") else request
        self.data_returned = None
        self.status_returned = status.HTTP_404_NOT_FOUND

    # =================================================================
    def __create(self, _data_list):
        self.data_returned = list()
        flag = False
        if self.wprd == COUNTRY:
            post_ref = Country_View()
        elif self.wprd == STATE:
            post_ref = State_View()
        elif self.wprd == CITY:
            post_ref = City_View()
        else:
            self.data_returned = ERROR_CRUD_GEN
            self.data_returned[ERROR] = "/utility/mass/<word>"
            self.status_returned = status.HTTP_400_BAD_REQUEST
            return

        if "mass" in _data_list.keys():
            for data in _data_list["mass"]:
                self.request.data.update(data)
                post_ret = post_ref.post(self.request)
                if post_ret.status_code != 201:
                    self.data_returned.append(post_ret.data)
                    flag = False
                else:
                    self.data_returned.append(post_ret.data)
                    flag = True
            if flag:
                self.status_returned = status.HTTP_201_CREATED
            else:
                self.status_returned = status.HTTP_400_BAD_REQUEST
        else:
            self.data_returned = INVALID_FORMATTING
            self.status_returned = status.HTTP_400_BAD_REQUEST
        return

    def post(self, request, word=None):
        self.__initial(request=request, wprd=word)
        self.__create(_data_list=request.data)
        return Response(data=self.data_returned, status=self.status_returned)
