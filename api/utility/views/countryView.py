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
from utilities.models import U_Country
from utilities.serializers import U_Country_Serializer


# --------------------------------------------------------------------------
# CONSTANTS
# --------------------------------------------------------------------------
from utilities.views.constants import INVALID_ID

# --------------------------------------------------------------------------
# CODE
# ---------------------------------------------------------------------------
class Country_View(APIView):

    renderer_classes = [JSONRenderer]
    # authentication_classes = [UserAuthentication]
    # permission_classes = [UserAuthorization]
    def __initial(self, pk=None):
        self.pk = None if pk in (None, "") else int(pk)
        self.data_returned = None
        self.status_returned = status.HTTP_404_NOT_FOUND

    def __post_country(self, data):
        data["name"] = data["name"].upper()
        serialized = U_Country_Serializer(data=data)
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
                and self.data_returned["name"][0] == "u_ country with this name code already exists."
            ) or (
                "isd_code" in self.data_returned.keys()
                and self.data_returned["isd_code"][0] == "u_ country with this isd code already exists."
            ):
                self.status_returned = status.HTTP_409_CONFLICT
            else:
                self.status_returned = status.HTTP_400_BAD_REQUEST
        return

    def post(self, request, pk=None):
        self.__initial(pk)
        self.__post_country(data=request.data)
        return Response(data=self.data_returned, status=self.status_returned)

    def __get_country_all(self):
        country_ref = U_Country.objects.all().order_by("name")
        serialized = U_Country_Serializer(country_ref, many=True).data
        self.data_returned = serialized
        self.status_returned = status.HTTP_200_OK
        return

    def __get_country_sel(self, pk=None):
        try:
            country_ref = U_Country.objects.get(id=pk)
            serialized = U_Country_Serializer(country_ref, many=False).data
            self.data_returned = serialized
            self.status_returned = status.HTTP_200_OK
        except U_Country.DoesNotExist:
            self.data_returned = INVALID_ID
            self.status_returned = status.HTTP_404_NOT_FOUND
        return

    def get(self, request, pk=None):
        self.__initial(pk)
        if self.pk == None:
            self.__get_country_all()
        else:
            self.__get_country_sel(pk=pk)
        return Response(data=self.data_returned, status=self.status_returned)

    def __edit_country(self, pk, data):
        data["name"] = data["name"].upper()
        try:
            country_ref = U_Country.objects.get(id=pk)
            country_ref.name = data["name"]
            country_ref.isd_code = data["isd_code"]
            try:
                country_ref.save()
                data["id"] = pk
                self.data_returned = data
                self.status_returned = status.HTTP_201_CREATED
            except IntegrityError as e:
                if str(e) == "UNIQUE constraint failed: utilities_u_country.isd_code":
                    self.data_returned = "NON UNIQUE ISD CODE"
                if str(e) == "UNIQUE constraint failed: utilities_u_country.name":
                    self.data_returned = "NON UNIQUE NAME"
                self.status_returned = status.HTTP_409_CONFLICT
        except U_Country.DoesNotExist:
            self.data_returned = INVALID_ID
            self.status_returned = status.HTTP_404_NOT_FOUND
        return

    def put(self, request, pk=None):
        self.__initial(pk)
        if self.pk == None:
            self.data_returned = "/utilities/country/<id>"
            self.status_returned = status.HTTP_400_BAD_REQUEST
        else:
            self.__edit_country(pk=pk, data=request.data)
        return Response(data=self.data_returned, status=self.status_returned)

    def __delete_country(self, pk=None):
        try:
            country_ref = U_Country.objects.get(id=pk)
            try:
                country_ref.delete()
                self.data_returned = "DELETED"
                self.status_returned = status.HTTP_200_OK
            except:
                self.data_returned = "[CRUD] DELETED ERROR"
                self.status_returned = status.HTTP_400_BAD_REQUEST
        except U_Country.DoesNotExist:
            self.data_returned = INVALID_ID
            self.status_returned = status.HTTP_404_NOT_FOUND
        return

    def delete(self, request, pk=None):
        self.__initial(pk)
        if self.pk == None:
            data_returned = "/utilities/country/<id>"
            status_returned = status.HTTP_400_BAD_REQUEST
        else:
            self.__delete_country(pk=pk)

        return Response(data=self.data_returned, status=self.status_returned)
