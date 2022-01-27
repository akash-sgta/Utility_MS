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
from utility.models import Country
from utility.serializers import Country_Serializer
from access.security.authenticate import Authentication
from access.security.authorization import Authorization


# --------------------------------------------------------------------------
# CONSTANTS
# --------------------------------------------------------------------------
from utility.extra.constant import INVALID_ID, ERROR_CRUD_GEN, ERROR_CRUD_D, SUCCESS_CRUD_D

ERROR = "ERROR"
# --------------------------------------------------------------------------
# CODE
# ---------------------------------------------------------------------------
class Country_View(APIView):

    renderer_classes = [JSONRenderer]
    authentication_classes = [Authentication]
    permission_classes = [Authorization]

    def __initial(self, pk=None):
        self.pk = None if pk in (None, "", 0) else int(pk)
        self.data_returned = None
        self.status_returned = status.HTTP_404_NOT_FOUND

    # ====================================================================
    def __create_country(self, data):
        data["name"] = data["name"].upper()
        serialized = Country_Serializer(data=data)
        if serialized.is_valid():
            try:
                serialized.save()
                self.data_returned = serialized.data
                self.status_returned = status.HTTP_201_CREATED
            except Exception as e:
                self.data_returned = ERROR_CRUD_GEN
                self.data_returned[ERROR] = str(e)
                self.status_returned = status.HTTP_400_BAD_REQUEST
        else:
            self.data_returned = ERROR_CRUD_GEN
            self.data_returned[ERROR] = serialized.errors
            self.status_returned = status.HTTP_400_BAD_REQUEST
        return

    def post(self, request, pk=None):
        self.__initial(pk)
        self.__create_country(data=request.data)
        return Response(data=self.data_returned, status=self.status_returned)

    # ====================================================================
    def __read_country_all(self):
        country_ref = Country.objects.all().order_by("name")
        serialized = Country_Serializer(country_ref, many=True).data
        self.data_returned = serialized
        self.status_returned = status.HTTP_200_OK
        return

    def __read_country_sel(self):
        try:
            country_ref = Country.objects.get(id=self.pk)
            serialized = Country_Serializer(country_ref, many=False).data
            self.data_returned = serialized
            self.status_returned = status.HTTP_200_OK
        except Country.DoesNotExist:
            self.data_returned = INVALID_ID
            self.status_returned = status.HTTP_404_NOT_FOUND
        return

    def get(self, request, pk=None):
        self.__initial(pk)
        if self.pk == None:
            self.__read_country_all()
        else:
            self.__read_country_sel(pk=pk)
        return Response(data=self.data_returned, status=self.status_returned)

    # ====================================================================
    def __update_country(self, data):
        data["name"] = data["name"].upper()
        try:
            country_ref = Country.objects.get(id=self.pk)
            country_ser = Country_Serializer(country_ref, data=data)
            if country_ser.is_valid():
                try:
                    country_ser.save()
                    self.data_returned = country_ser.data
                    self.status_returned = status.HTTP_201_CREATED
                except Exception as e:
                    self.data_returned = ERROR_CRUD_GEN
                    self.data_returned[ERROR] = str(e)
                    self.status_returned = status.HTTP_400_BAD_REQUEST
            else:
                self.data_returned = ERROR_CRUD_GEN
                self.data_returned[ERROR] = country_ser.errors
                self.status_returned = status.HTTP_400_BAD_REQUEST
        except Country.DoesNotExist:
            self.data_returned = INVALID_ID
            self.status_returned = status.HTTP_404_NOT_FOUND
        return

    def put(self, request, pk=None):
        self.__initial(pk)
        if self.pk == None:
            self.data_returned = ERROR_CRUD_GEN
            self.data_returned[ERROR] = "/utility/country/<id>"
            self.status_returned = status.HTTP_400_BAD_REQUEST
        else:
            self.__update_country(pk=pk, data=request.data)
        return Response(data=self.data_returned, status=self.status_returned)

    # ====================================================================
    def __delete_country(self):
        try:
            country_ref = Country.objects.get(id=self.pk)
            try:
                country_ref.delete()
                self.data_returned = SUCCESS_CRUD_D
                self.status_returned = status.HTTP_200_OK
            except:
                self.data_returned = ERROR_CRUD_D
                self.status_returned = status.HTTP_400_BAD_REQUEST
        except Country.DoesNotExist:
            self.data_returned = INVALID_ID
            self.status_returned = status.HTTP_404_NOT_FOUND
        return

    def delete(self, request, pk=None):
        self.__initial(pk)
        if self.pk == None:
            self.data_returned = ERROR_CRUD_GEN
            self.data_returned[ERROR] = "/utility/country/<id>"
            status_returned = status.HTTP_400_BAD_REQUEST
        else:
            self.__delete_country()
        return Response(data=self.data_returned, status=self.status_returned)
