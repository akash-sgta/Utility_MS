# --------------------------------------------------------------------------
# DOCUMENTATION
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# LIRARY
# --------------------------------------------------------------------------
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from access.security.authenticate import Authentication
from access.security.authorization import Authorization
from utility.models import City
from utility.serializers import City_Serializer


# --------------------------------------------------------------------------
# CONSTANTS
# --------------------------------------------------------------------------
from utility.extra.constant import INVALID_ID, ERROR_CRUD_C, ERROR_CRUD_GEN, ERROR_CRUD_D, SUCCESS_CRUD_D

ERROR = "ERROR"
# --------------------------------------------------------------------------
# CODE
# ---------------------------------------------------------------------------
class City_View(APIView):

    renderer_classes = [JSONRenderer]
    authentication_classes = [Authentication]
    permission_classes = [Authorization]

    def __initial(self, pk=None, pkk=None):
        self.pk = None if pk in (None, "", 0) else int(pk)
        self.pkk = None if pkk in (None, "", 0) else int(pkk)
        self.data_returned = None
        self.status_returned = status.HTTP_404_NOT_FOUND

    # ====================================================================
    def __create_city(self, data):
        data["name"] = data["name"].upper()
        serialized = City_Serializer(data=data)
        if serialized.is_valid():
            if serialized.save():
                self.data_returned = serialized.data
                self.status_returned = status.HTTP_201_CREATED
            else:
                self.data_returned = ERROR_CRUD_C
                self.status_returned = status.HTTP_400_BAD_REQUEST
        else:
            self.data_returned = ERROR_CRUD_GEN
            self.data_returned[ERROR] = serialized.errors
            self.status_returned = status.HTTP_400_BAD_REQUEST
        return

    def post(self, request, pk=None, pkk=None):
        self.__initial(pk, pkk)
        self.__create_city(data=request.data)
        return Response(data=self.data_returned, status=self.status_returned)

    # ====================================================================
    def __read_city_all(self):
        city_ref = City.objects.all().order_by("state_id", "name")
        serialized = City_Serializer(city_ref, many=True).data
        self.data_returned = serialized
        self.status_returned = status.HTTP_200_OK
        return

    def __read_city_sel(self):
        try:
            city_ref = City.objects.get(id=self.pkk)
            serialized = City_Serializer(city_ref, many=False).data
            self.data_returned = serialized
            self.status_returned = status.HTTP_200_OK
        except City.DoesNotExist:
            self.data_returned = INVALID_ID
            self.status_returned = status.HTTP_404_NOT_FOUND
        return

    def __read_state_sel(self):
        city_ref = City.objects.filter(state_id=self.pk).order_by("name")
        serialized = City_Serializer(city_ref, many=True).data
        self.data_returned = serialized
        self.status_returned = status.HTTP_200_OK
        return

    def get(self, request, pk=None, pkk=None):
        self.__initial(pk, pkk)
        if self.pk == None:
            if self.pkk == None:
                self.__read_city_all()
            else:
                self.__read_city_sel()
        else:
            self.__read_state_sel()
        return Response(data=self.data_returned, status=self.status_returned)

    # ====================================================================
    def __update_city(self, pk, data):
        data["name"] = data["name"].upper()
        try:
            city_ref = City.objects.get(id=self.pkk)
            city_ser = City_Serializer(city_ref, data=data)
            if city_ser.is_valid():
                try:
                    city_ser.save()
                    self.data_returned = city_ser.data
                    self.status_returned = status.HTTP_201_CREATED
                except Exception as e:
                    self.data_returned = ERROR_CRUD_GEN
                    self.data_returned[ERROR] = str(e)
                    self.status_returned = status.HTTP_400_BAD_REQUEST
            else:
                self.data_returned = ERROR_CRUD_GEN
                self.data_returned[ERROR] = city_ser.errors
                self.status_returned = status.HTTP_400_BAD_REQUEST
        except City.DoesNotExist:
            self.data_returned = INVALID_ID
            self.status_returned = status.HTTP_404_NOT_FOUND
        return

    def put(self, request, pk=None, pkk=None):
        self.__initial(pk, pkk)
        if self.pkk == None:
            self.data_returned = ERROR_CRUD_GEN
            self.data_returned[ERROR] = "/utility/city//<id>"
            self.status_returned = status.HTTP_400_BAD_REQUEST
        else:
            self.__update_city(data=request.data)
        return Response(data=self.data_returned, status=self.status_returned)

    # ====================================================================
    def __delete_city(self):
        try:
            city_ref = City.objects.get(id=self.pkk)
            try:
                city_ref.delete()
                self.data_returned = SUCCESS_CRUD_D
                self.status_returned = status.HTTP_200_OK
            except:
                self.data_returned = ERROR_CRUD_D
                self.status_returned = status.HTTP_400_BAD_REQUEST
        except City.DoesNotExist:
            self.data_returned = INVALID_ID
            self.status_returned = status.HTTP_404_NOT_FOUND
        return

    def delete(self, request, pk=None, pkk=None):
        self.__initial(pk, pkk)
        if self.pkk == None:
            self.data_returned = ERROR_CRUD_GEN
            self.data_returned[ERROR] = "/utility/city//<id>"
            self.status_returned = status.HTTP_400_BAD_REQUEST
        else:
            self.__delete_city()
        return Response(data=self.data_returned, status=self.status_returned)
