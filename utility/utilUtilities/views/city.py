# =========================================================================================
#                                       DOCUMENTATION
# =========================================================================================
"""
Naming Convention
<ModelName>View
<ModelName>View_as_<Entity>
"""

# =========================================================================================
#                                       LIBRARY
# =========================================================================================
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings

# --------------------------------------------------

from utilUtilities.models import City
from utilUtilities.serializers import City_Serializer


# =========================================================================================
#                                       CONSTANT
# =========================================================================================
STATUS = "STATUS"
DATA = "DATA"
MESSAGE = "MESSAGE"
TIMEZONE = "TIMEZONE"
RETURN_JSON = {STATUS: False, DATA: dict(), MESSAGE: "", TIMEZONE: settings.TIME_ZONE}
SYS = "sys"
# --------------------------------------------------
NULL = (None, "", 0)
SETTINGS_SYSTEM = settings.SYSTEM
COMA = ","
EQUAL = "EQ"
EQUAL2 = "="
CHECK = "CHECK"
REFRESH = "REFRESH"
# --------------------------------------------------
INVALID_URL = "INVALID URL"
METHOD_NOT_ALLOWED = "METHOD NOT ALLOWED"
INVALID_SPARAMS = "INVALID SEARCH PARAMETERS"
NO_CONTENT = "NO CONTENT FOUND"
INVALID_PAYLOAD = "INVALID DATA POSTED"
# --------------------------------------------------

# --------------------------------------------------


# =========================================================================================
#                                       CODE
# =========================================================================================
class CityView(APIView):
    renderer_classes = [JSONRenderer]
    authentication_classes = []

    def __init__(self, query1=None, query2=None):
        super(CityView, self).__init__()
        self.data_returned = RETURN_JSON
        self.status_returned = status.HTTP_400_BAD_REQUEST
        self.query1 = int(query1) if query1 not in NULL else None
        self.query2 = query2.upper() if query2 not in NULL else None
        return

    def _create_query(self) -> str:
        query = ""
        if self.query2 not in NULL:
            word = self.query2.split(COMA)
            for i in range(len(word)):
                word[i] = word[i].split(EQUAL)
                word[i][0] = word[i][0].strip()
                word[i][1] = word[i][1].strip()
                if word[i][0] in self.KEYS:
                    query += f"{word[i][0]}{EQUAL2}{word[i][1]}{COMA}"
            query = query[:-1]
        return query


class CityView_asUser(CityView):
    permission_classes = []

    def __init__(self, query1=None, query2=None):
        super(CityView_asUser, self).__init__(query1=query1, query2=query2)

    # =============================================================
    def __create_specific(self, data: dict) -> None:
        self.data_returned[MESSAGE] = METHOD_NOT_ALLOWED
        self.status_returned = status.HTTP_405_METHOD_NOT_ALLOWED
        return

    def post(self, request, pk: int, word: str):
        self.__init__(query1=pk, query2=word)
        self.__create_specific(data=request.data)
        return Response(data=self.data_returned, status=self.status_returned)

    # =============================================================
    def __read_specific(self) -> None:
        try:
            country_ref = exec(f'City.objects.filter(sys={self.sys},{self._create_query()}).order_by("name")')
            if len(country_ref) == 0:
                raise City.DoesNotExist
        except City.DoesNotExist:
            self.data_returned[STATUS] = False
            self.data_returned[MESSAGE] = INVALID_SPARAMS
            self.status_returned = status.HTTP_404_NOT_FOUND
        else:
            country_ser = City_Serializer(country_ref, many=False).data
            self.data_returned[STATUS] = True
            self.data_returned[DATA] = country_ser
            self.status_returned = status.HTTP_200_OK
        return

    def __read_all(self) -> None:
        try:
            country_ref = City.objects.filter(sys=SETTINGS_SYSTEM).order_by("name")
            if len(country_ref) == 0:
                raise City.DoesNotExist
        except City.DoesNotExist:
            self.data_returned[STATUS] = False
            self.data_returned[MESSAGE] = NO_CONTENT
            self.status_returned = status.HTTP_204_NO_CONTENT
        else:
            country_ser = City_Serializer(country_ref, many=False).data
            self.data_returned[STATUS] = True
            self.data_returned[DATA] = country_ser
            self.status_returned = status.HTTP_200_OK
        return

    def get(self, request, pk: int, word: str):
        self.__init__(query1=pk, query2=word)
        if self.query2 in NULL:
            self.__read_all()
        else:
            self.__read_specific()
        return Response(data=self.data_returned, status=self.status_returned)

    # =============================================================
    def __update_specific(self, data: dict):
        self.data_returned[STATUS] = False
        self.data_returned[MESSAGE] = METHOD_NOT_ALLOWED
        self.status_returned = status.HTTP_405_METHOD_NOT_ALLOWED
        return

    def edit(self, request, pk: int, word: str):
        self.__init__(query1=pk, query2=word)
        self.__update_specific(data=request.data)
        return Response(data=self.data_returned, status=self.status_returned)

    # =============================================================
    def __delete_specific(self):
        self.data_returned[STATUS] = False
        self.data_returned[MESSAGE] = METHOD_NOT_ALLOWED
        self.status_returned = status.HTTP_405_METHOD_NOT_ALLOWED
        return

    def delete(self, request, pk: int, word: str):
        self.__init__(query1=pk, query2=word)
        self.__delete_specific()
        return Response(data=self.data_returned, status=self.status_returned)


class CityView_asAdmin(CityView):
    permission_classes = []

    def __init__(self, query1=None, query2=None):
        super(CityView_asAdmin, self).__init__(query1=query1, query2=query2)

    # =============================================================
    def __create_specific(self, data: dict) -> None:
        data[SYS] = SETTINGS_SYSTEM
        country_ser = City_Serializer(data=data)
        if country_ser.is_valid():
            try:
                country_ser.save()
            except Exception as e:
                self.data_returned[STATUS] = False
                self.data_returned[MESSAGE] = str(e)
                self.status_returned = status.HTTP_406_NOT_ACCEPTABLE
            else:
                self.data_returned[STATUS] = True
                self.data_returned[DATA] = country_ser.data
                self.status_returned = status.HTTP_201_CREATED
        else:
            self.data_returned[STATUS] = False
            self.data_returned[MESSAGE] = country_ser.errors
            self.status_returned = status.HTTP_406_NOT_ACCEPTABLE
        return

    def post(self, request, pk: int, word: str):
        self.__init__(query1=pk, query2=word)
        self.__create_specific(data=request.data)
        return Response(data=self.data_returned, status=self.status_returned)

    # =============================================================
    def __read_specific(self) -> None:
        try:
            country_ref = exec(f'City.objects.filter(sys={self.sys},{self._create_query()}).order_by("name")')
            if len(country_ref) == 0:
                raise City.DoesNotExist
        except City.DoesNotExist:
            self.data_returned[STATUS] = False
            self.data_returned[MESSAGE] = INVALID_SPARAMS
            self.status_returned = status.HTTP_404_NOT_FOUND
        else:
            country_ser = City_Serializer(country_ref, many=True).data
            self.data_returned[STATUS] = True
            self.data_returned[DATA] = country_ser
            self.status_returned = status.HTTP_200_OK
        return

    def __read_all(self) -> None:
        try:
            country_ref = City.objects.filter(sys=SETTINGS_SYSTEM).order_by("name")
            if len(country_ref) == 0:
                raise City.DoesNotExist
        except City.DoesNotExist:
            self.data_returned[STATUS] = False
            self.data_returned[MESSAGE] = NO_CONTENT
            self.status_returned = status.HTTP_204_NO_CONTENT
        else:
            country_ser = City_Serializer(country_ref, many=False).data
            self.data_returned[STATUS] = True
            self.data_returned[DATA] = country_ser
            self.status_returned = status.HTTP_200_OK
        return

    def get(self, request, pk: int, word: str):
        self.__init__(query1=pk, query2=word)
        if self.query2 in NULL:
            self.__read_all()
        else:
            self.__read_specific()
        return Response(data=self.data_returned, status=self.status_returned)

    # =============================================================
    def __update_specific(self, data: dict) -> None:
        data[SYS] = SETTINGS_SYSTEM
        try:
            country_ref = exec(f'City.objects.filter(sys={SETTINGS_SYSTEM},{self._create_query()}).order_by("name")')
            if len(country_ref) == 0:
                raise City.DoesNotExist
        except City.DoesNotExist:
            self.data_returned[STATUS] = False
            self.data_returned[MESSAGE] = INVALID_SPARAMS
            self.status_returned = status.HTTP_404_NOT_FOUND
        else:
            country_ref = country_ref[0]
            country_ser = City_Serializer(country_ref, data=data)
            if country_ser.is_valid():
                try:
                    country_ser.save()
                except Exception as e:
                    self.data_returned[STATUS] = False
                    self.data_returned[MESSAGE] = str(e)
                    self.status_returned = status.HTTP_406_NOT_ACCEPTABLE
                else:
                    self.data_returned[STATUS] = True
                    self.data_returned[DATA] = country_ser.data
                    self.status_returned = status.HTTP_201_CREATED
            else:
                self.data_returned[STATUS] = False
                self.data_returned[MESSAGE] = country_ser.errors
                self.status_returned = status.HTTP_406_NOT_ACCEPTABLE
        return

    def edit(self, request, pk: int, word: str):
        self.__init__(query1=pk, query2=word)
        if self.query2 in None:
            self.data_returned[STATUS] = False
            self.data_returned[MESSAGE] = INVALID_URL
            self.status_returned = status.HTTP_400_BAD_REQUEST
        else:
            self.__update_specific(data=request.data)
        return Response(data=self.data_returned, status=self.status_returned)

    # =============================================================
    def __delete_specific(self):
        try:
            country_ref = exec(f'City.objects.filter(sys={self.sys},{self._create_query()}).order_by("name")')
            if len(country_ref) == 0:
                raise City.DoesNotExist
        except City.DoesNotExist:
            self.data_returned[STATUS] = False
            self.data_returned[MESSAGE] = INVALID_SPARAMS
            self.status_returned = status.HTTP_404_NOT_FOUND
        else:
            country_ref = country_ref[0]
            country_ser = City_Serializer(country_ref, many=False).data
            country_ref.delete()
            self.data_returned[STATUS] = True
            self.data_returned[DATA] = country_ser
            self.status_returned = status.HTTP_200_OK
        return

    def delete(self, request, pk: int, word: str):
        self.__init__(query1=pk, query2=word)
        if self.query2 in None:
            self.data_returned[STATUS] = False
            self.data_returned[MESSAGE] = INVALID_URL
            self.status_returned = status.HTTP_400_BAD_REQUEST
        else:
            self.__delete_specific()
        return Response(data=self.data_returned, status=self.status_returned)
