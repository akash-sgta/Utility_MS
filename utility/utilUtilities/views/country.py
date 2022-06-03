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

from utilUtilities.models import Country
from utilUtilities.serializers import Country_Serializer


# =========================================================================================
#                                       CONSTANT
# =========================================================================================
STATUS = "STATUS"
DATA = "DATA"
MESSAGE = "MESSAGE"
TIMEZONE = "TIMEZONE"
BLANK_LIST = []
BLANK_STR = ""
RETURN_JSON = {STATUS: False, DATA: BLANK_LIST, MESSAGE: BLANK_STR, TIMEZONE: settings.TIME_ZONE}
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
class CountryView(APIView):
    renderer_classes = [JSONRenderer]
    authentication_classes = []

    KEYS = (
        "id",
        "isd",
        "iso",
        "name",
    )

    def __init__(self, query1=None, query2=None):
        super(CountryView, self).__init__()
        self.data_returned = RETURN_JSON.copy()
        self.status_returned = status.HTTP_400_BAD_REQUEST
        self.query1 = query1.upper() if query1 not in NULL else None
        self.query2 = query2.upper() if query2 not in NULL else None
        return

    def _create_query(self, flag=True) -> str:
        _return = f"sys={SETTINGS_SYSTEM}{COMA}"
        if self.query2 not in NULL:
            word = self.query2.split(COMA)
            for i in range(len(word)):
                word[i] = word[i].split(EQUAL)
                word[i][0] = word[i][0].strip().lower()
                word[i][1] = word[i][1].strip()
                if word[i][0] in self.KEYS:
                    if flag:
                        _return += f"{word[i][0]}__icontains{EQUAL2}'{word[i][1]}'{COMA}"
                    else:
                        _return += f"{word[i][0]}__in{EQUAL2}'{word[i][1]}'{COMA}"
        return _return


class CountryView_asUser(CountryView):
    permission_classes = []

    def __init__(self, query1=None, query2=None):
        super(CountryView_asUser, self).__init__(query1=query1, query2=query2)

    # =============================================================
    def __create_specific(self, data: dict) -> None:
        self.data_returned[MESSAGE] = METHOD_NOT_ALLOWED
        self.status_returned = status.HTTP_405_METHOD_NOT_ALLOWED
        return

    def post(self, request, word: str, pk: str):
        self.__init__(query1=word, query2=pk)
        self.__create_specific(data=request.data)
        return Response(data=self.data_returned, status=self.status_returned)

    # =============================================================
    def __read_specific(self) -> None:
        try:
            country_ref = Country.objects.get(sys=SETTINGS_SYSTEM, id=int(self.query2))
        except Country.DoesNotExist:
            self.data_returned[STATUS] = False
            self.data_returned[MESSAGE] = INVALID_SPARAMS
            self.status_returned = status.HTTP_404_NOT_FOUND
        except ValueError:
            self.data_returned[STATUS] = False
            self.data_returned[MESSAGE] = INVALID_SPARAMS
            self.status_returned = status.HTTP_404_NOT_FOUND
        else:
            country_ser = Country_Serializer(country_ref, many=False).data
            self.data_returned[STATUS] = True
            self.data_returned[DATA].append(country_ser)
            self.status_returned = status.HTTP_200_OK
        return

    def __read_all(self) -> None:
        try:
            country_ref = Country.objects.all().order_by("id")
            if len(country_ref) == 0:
                raise Country.DoesNotExist
        except Country.DoesNotExist:
            self.data_returned[STATUS] = False
            self.data_returned[MESSAGE] = NO_CONTENT
            self.status_returned = status.HTTP_204_NO_CONTENT
        else:
            country_ser = Country_Serializer(country_ref, many=True).data
            self.data_returned[STATUS] = True
            self.data_returned[DATA] = country_ser
            self.status_returned = status.HTTP_200_OK
        return

    def __read_search(self) -> None:
        try:
            country_ref = eval(f'Country.objects.filter({self._create_query()}).order_by("id")')
            if len(country_ref) == 0:
                raise Country.DoesNotExist
        except Country.DoesNotExist:
            self.data_returned[STATUS] = False
            self.data_returned[MESSAGE] = NO_CONTENT
            self.status_returned = status.HTTP_204_NO_CONTENT
        except NameError:
            self.data_returned[STATUS] = False
            self.data_returned[MESSAGE] = INVALID_SPARAMS
            self.status_returned = status.HTTP_400_BAD_REQUEST
        else:
            country_ser = Country_Serializer(country_ref, many=True).data
            self.data_returned[STATUS] = True
            self.data_returned[DATA] = country_ser
            self.status_returned = status.HTTP_200_OK
        return

    def get(self, request, word: str, pk: str):
        self.__init__(query1=word, query2=pk)
        if self.query1 in NULL:
            if self.query2 in NULL:
                self.__read_all()
            else:
                self.__read_specific()
        else:
            if self.query2 in NULL:
                self.data_returned[STATUS] = False
                self.data_returned[MESSAGE] = INVALID_SPARAMS
                self.status_returned = status.HTTP_400_BAD_REQUEST
            else:
                self.__read_search()

        return Response(data=self.data_returned, status=self.status_returned)

    # =============================================================
    def __update_specific(self, data: dict):
        self.data_returned[STATUS] = False
        self.data_returned[MESSAGE] = METHOD_NOT_ALLOWED
        self.status_returned = status.HTTP_405_METHOD_NOT_ALLOWED
        return

    def put(self, request, word: str, pk: str):
        self.__init__(query1=word, query2=pk)
        self.__update_specific(data=request.data)
        return Response(data=self.data_returned, status=self.status_returned)

    # =============================================================
    def __delete_specific(self):
        self.data_returned[STATUS] = False
        self.data_returned[MESSAGE] = METHOD_NOT_ALLOWED
        self.status_returned = status.HTTP_405_METHOD_NOT_ALLOWED
        return

    def delete(self, request, word: str, pk: str):
        self.__init__(query1=word, query2=pk)
        self.__delete_specific()
        return Response(data=self.data_returned, status=self.status_returned)


class CountryView_asAdmin(CountryView_asUser):
    permission_classes = []

    def __init__(self, query1=None, query2=None):
        super(CountryView_asAdmin, self).__init__(query1=query1, query2=query2)

    # =============================================================
    def __create_specific(self, data: dict) -> None:
        data[SYS] = SETTINGS_SYSTEM
        country_ser = Country_Serializer(data=data)
        if country_ser.is_valid():
            try:
                country_ser.save()
            except Exception as e:
                self.data_returned[STATUS] = False
                self.data_returned[MESSAGE] = str(e)
                self.status_returned = status.HTTP_406_NOT_ACCEPTABLE
            else:
                country_ser = country_ser.data
                self.data_returned[STATUS] = True
                self.data_returned[DATA].append(country_ser)
                self.status_returned = status.HTTP_201_CREATED
        else:
            self.data_returned[STATUS] = False
            self.data_returned[MESSAGE] = country_ser.errors
            self.status_returned = status.HTTP_406_NOT_ACCEPTABLE
        return

    def post(self, request, word: str, pk: str):
        self.__init__(query1=word, query2=pk)
        self.__create_specific(data=request.data)
        return Response(data=self.data_returned, status=self.status_returned)

    # =============================================================
    def get(self, request, word: str, pk: str):
        return super(CountryView_asAdmin, self).get(word=word, pk=pk)

    # =============================================================
    def __update_specific(self, data: dict) -> None:
        data[SYS] = SETTINGS_SYSTEM
        try:
            country_ref = Country.objects.get(sys=SETTINGS_SYSTEM, id=int(self.query2))
        except Country.DoesNotExist:
            self.data_returned[STATUS] = False
            self.data_returned[MESSAGE] = INVALID_SPARAMS
            self.status_returned = status.HTTP_404_NOT_FOUND
        except ValueError:
            self.data_returned[STATUS] = False
            self.data_returned[MESSAGE] = INVALID_SPARAMS
            self.status_returned = status.HTTP_404_NOT_FOUND
        else:
            country_ser = Country_Serializer(country_ref, data=data)
            if country_ser.is_valid():
                try:
                    country_ser.save()
                except Exception as e:
                    self.data_returned[STATUS] = False
                    self.data_returned[MESSAGE] = str(e)
                    self.status_returned = status.HTTP_406_NOT_ACCEPTABLE
                else:
                    country_ser = country_ser.data
                    self.data_returned[STATUS] = True
                    self.data_returned[DATA].append(country_ser)
                    self.status_returned = status.HTTP_201_CREATED
            else:
                self.data_returned[STATUS] = False
                self.data_returned[MESSAGE] = country_ser.errors
                self.status_returned = status.HTTP_406_NOT_ACCEPTABLE
        return

    def put(self, request, word: str, pk: str):
        self.__init__(query1=word, query2=pk)
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
            country_ref = Country.objects.get(sys=SETTINGS_SYSTEM, id=int(self.query2))
        except Country.DoesNotExist:
            self.data_returned[STATUS] = False
            self.data_returned[MESSAGE] = INVALID_SPARAMS
            self.status_returned = status.HTTP_404_NOT_FOUND
        except ValueError:
            self.data_returned[STATUS] = False
            self.data_returned[MESSAGE] = INVALID_SPARAMS
            self.status_returned = status.HTTP_404_NOT_FOUND
        else:
            country_ser = Country_Serializer(country_ref, many=False).data
            country_ref.delete()
            self.data_returned[STATUS] = True
            self.data_returned[DATA].append(country_ser)
            self.status_returned = status.HTTP_200_OK
        return

    def delete(self, request, word: str, pk: str):
        self.__init__(query1=word, query2=pk)
        if self.query2 in None:
            self.data_returned[STATUS] = False
            self.data_returned[MESSAGE] = INVALID_URL
            self.status_returned = status.HTTP_400_BAD_REQUEST
        else:
            self.__delete_specific()
        return Response(data=self.data_returned, status=self.status_returned)
