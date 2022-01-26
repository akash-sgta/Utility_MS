# --------------------------------------------------------------------------
# DOCUMENTATION
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# LIRARY
# --------------------------------------------------------------------------
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.response import Response
from django.db.utils import IntegrityError
from rest_framework.views import APIView
from access.security.authenticate import Authentication
from access.security.authorization import Authorization
from utility.models import State, City
from utility.serializers import City_Serializer


# --------------------------------------------------------------------------
# CONSTANTS
# --------------------------------------------------------------------------
from utility.extra.constant import INVALID_ID

# --------------------------------------------------------------------------
# CODE
# ---------------------------------------------------------------------------
class City_View(APIView):

    renderer_classes = [JSONRenderer]
    authentication_classes = [Authentication]
    permission_classes = [Authorization]

    def __initialize(self, pk=None, pkk=None):
        self.pk = None if pk in (None, "") else int(pk)
        self.pkk = None if pkk in (None, "") else int(pkk)
        self.data_returned = None
        self.status_returned = status.HTTP_404_NOT_FOUND

    def __post_city(self, data):
        data["name"] = data["name"].upper()
        serialized = U_City_Serializer(data=data)
        if serialized.is_valid():
            if serialized.save():
                self.data_returned = serialized.data
                self.status_returned = status.HTTP_201_CREATED
            else:
                self.data_returned = "[CRUD] CREATE ERROR"
                self.status_returned = status.HTTP_417_EXPECTATION_FAILED
        else:
            self.data_returned = serialized.errors
            if (
                "name" in self.data_returned.keys()
                and self.data_returned["name"][0] == "u_ city with this name already exists."
            ):
                self.status_returned = status.HTTP_409_CONFLICT
            else:
                self.status_returned = status.HTTP_400_BAD_REQUEST
        return

    def post(self, request, pk=None, pkk=None):
        self.__initial(pk, pkk)
        self.__post_city(data=request.data)
        return Response(data=self.data_returned, status=self.status_returned)

    def __get_city_all(self):
        city_ref = U_City.objects.all().order_by("state_id", "name")
        serialized = U_City_Serializer(city_ref, many=True).data
        self.data_returned = serialized
        self.status_returned = status.HTTP_200_OK
        return

    def __get_city_sel(self, pk=None):
        try:
            city_ref = U_City.objects.get(id=pk)
            serialized = U_City_Serializer(city_ref, many=False).data
            self.data_returned = serialized
            self.status_returned = status.HTTP_200_OK
        except U_City.DoesNotExist:
            self.data_returned = INVALID_ID
            self.status_returned = status.HTTP_404_NOT_FOUND
        return

    def __get_state_sel(self, pk=None):
        city_ref = U_City.objects.filter(state_id=pk).order_by("name")
        serialized = U_City_Serializer(city_ref, many=True).data
        self.data_returned = serialized
        self.status_returned = status.HTTP_200_OK
        return

    def get(self, request, pk=None, pkk=None):
        self.__initial(pk, pkk)
        if self.pk == None:
            if self.pkk == None:
                self.__get_city_all()
            else:
                self.__get_city_sel(pk=pkk)
        else:
            self.__get_state_sel(pk=pk)
        return Response(data=self.data_returned, status=self.status_returned)

    def __edit_city(self, pk, data):
        data["name"] = data["name"].upper()
        try:
            city_ref = U_City.objects.get(id=pk)
            city_ref.name = data["name"]
            try:
                city_ref.state_id = U_State.objects.get(id=data["state_id"])
            except U_State.DoesNotExist:
                self.data_returned = INVALID_ID
                self.status_returned = status.HTTP_404_NOT_FOUND
            else:
                try:
                    city_ref.save()
                    data["id"] = pk
                    self.data_returned = data
                    self.status_returned = status.HTTP_201_CREATED
                except IntegrityError as e:
                    if str(e) == "UNIQUE constraint failed: utilities_u_city.name":
                        self.data_returned = "NON UNIQUE NAME"
                    self.status_returned = status.HTTP_409_CONFLICT
        except U_City.DoesNotExist:
            self.data_returned = INVALID_ID
            self.status_returned = status.HTTP_404_NOT_FOUND
        return

    def put(self, request, pk=None, pkk=None):
        self.__initial(pk, pkk)
        if self.pkk == None:
            self.data_returned = "/utilities/city//<id>"
            self.status_returned = status.HTTP_400_BAD_REQUEST
        else:
            self.__edit_city(pk=pkk, data=request.data)
        return Response(data=self.data_returned, status=self.status_returned)

    def __delete_city(self, pk=None):
        try:
            city_ref = U_City.objects.get(id=pk)
            try:
                city_ref.delete()
                self.data_returned = "DELETED"
                self.status_returned = status.HTTP_200_OK
            except:
                self.data_returned = "[CRUD] DELETED ERROR"
                self.status_returned = status.HTTP_400_BAD_REQUEST
        except U_City.DoesNotExist:
            self.data_returned = INVALID_ID
            self.status_returned = status.HTTP_404_NOT_FOUND
        return

    def delete(self, request, pk=None, pkk=None):
        self.__initial(pk, pkk)
        if self.pkk == None:
            data_returned = "/utilities/city//<id>"
            status_returned = status.HTTP_400_BAD_REQUEST
        else:
            self.__delete_city(pk=pkk)
        return Response(data=self.data_returned, status=self.status_returned)
