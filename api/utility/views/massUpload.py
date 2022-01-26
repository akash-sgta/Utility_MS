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
from utility.models import State, City
from utility.serializers import City_Serializer, Country_Serializer, State_Serializer
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
    ERROR_CRUD_C,
    U_CITY_NAME_CONF,
    U_COUNTRY_NAME_CONF,
    U_COUNTRY_ISD_CONF,
    U_COUNTRY_ISO_CONF,
    U_STATE_NAME_CONF,
)


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

    # def __post_country(self, _data_list):
    #     self.data_returned = list()
    #     flag = False
    #     if "mass" in _data_list.keys():
    #         for data in _data_list["mass"]:
    #             data["name"] = data["name"].upper()
    #             serialized = U_Country_Serializer(data=data)
    #             if serialized.is_valid():
    #                 if serialized.save():
    #                     self.data_returned.append(serialized.data)
    #                 else:
    #                     self.data_returned.append(ERROR_CRUD_C)
    #                     flag = True
    #             else:
    #                 self.data_returned.append(serialized.errors)
    #                 if (
    #                     (
    #                         "name" in self.data_returned[-1].keys()
    #                         and self.data_returned[-1]["name"][0] == U_COUNTRY_NAME_CONF
    #                     )
    #                     or (
    #                         "isd" in self.data_returned[-1].keys()
    #                         and self.data_returned[-1]["isd"][0] == U_COUNTRY_ISD_CONF
    #                     )
    #                     or (
    #                         "iso" in self.data_returned[-1].keys()
    #                         and self.data_returned[-1]["iso"][0] == U_COUNTRY_ISO_CONF
    #                     )
    #                 ):
    #                     flag = True
    #                 else:
    #                     flag = True
    #         if flag:
    #             self.status_returned = status.HTTP_400_BAD_REQUEST
    #         else:
    #             self.status_returned = status.HTTP_201_CREATED
    #     else:
    #         self.data_returned = INVALID_FORMATTING
    #         self.status_returned = status.HTTP_400_BAD_REQUEST
    #     return

    # def __post_state(self, _data_list):
    #     self.data_returned = list()
    #     flag = False
    #     if "mass" in _data_list.keys():
    #         for data in _data_list["mass"]:
    #             data["name"] = data["name"].upper()
    #             serialized = U_State_Serializer(data=data)
    #             if serialized.is_valid():
    #                 if serialized.save():
    #                     self.data_returned.append(serialized.data)
    #                 else:
    #                     self.data_returned.append(ERROR_CRUD_C)
    #                     flag = True
    #             else:
    #                 self.data_returned.append(serialized.errors)
    #                 if (
    #                     "name" in self.data_returned[-1].keys()
    #                     and self.data_returned[-1]["name"][0] == U_STATE_NAME_CONF
    #                 ):
    #                     flag = True
    #                 else:
    #                     flag = True
    #         if flag:
    #             self.status_returned = status.HTTP_400_BAD_REQUEST
    #         else:
    #             self.status_returned = status.HTTP_201_CREATED
    #     else:
    #         self.data_returned = INVALID_FORMATTING
    #         self.status_returned = status.HTTP_400_BAD_REQUEST
    #     return

    def __post_city(self, _data_list):
        self.data_returned = list()
        flag = False
        post_ref = City_View()
        if "mass" in _data_list.keys():
            for data in _data_list["mass"]:
                self.request.data = data
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
        self.__initial(request=request, word=word)
        if self.wprd == COUNTRY:
            self.__post_country(_data_list=request.data)
        elif self.wprd == STATE:
            self.__post_state(_data_list=request.data)
        elif self.wprd == CITY:
            self.__post_city(_data_list=request.data)
        else:
            self.data_returned = "/utilities/mass/<word>"
        return Response(data=self.data_returned, status=self.status_returned)
