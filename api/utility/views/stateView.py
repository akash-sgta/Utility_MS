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
from utilities.models import U_State, U_Country
from utilities.serializers import U_State_Serializer


# --------------------------------------------------------------------------
# CONSTANTS
# --------------------------------------------------------------------------
from utilities.views.constants import INVALID_ID

# --------------------------------------------------------------------------
# CODE
# ---------------------------------------------------------------------------
class State_View(APIView):

    renderer_classes = [JSONRenderer]
    # authentication_classes = [UserAuthentication]
    # permission_classes = [UserAuthorization]
    def __initial(self, pk=None, pkk=None):
        self.pk = None if pk in (None, "") else int(pk)
        self.pkk = None if pkk in (None, "") else int(pkk)
        self.data_returned = None
        self.status_returned = status.HTTP_404_NOT_FOUND

    def __post_state(self, data):
        data["name"] = data["name"].upper()
        serialized = U_State_Serializer(data=data)
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
                and self.data_returned["name"][0] == "u_ state with this name already exists."
            ):
                self.status_returned = status.HTTP_409_CONFLICT
            else:
                self.status_returned = status.HTTP_400_BAD_REQUEST
        return

    def post(self, request, pk=None, pkk=None):
        self.__initial(pk, pkk)
        self.__post_state(data=request.data)
        return Response(data=self.data_returned, status=self.status_returned)

    def __get_state_all(self):
        state_ref = U_State.objects.all().order_by("country_id", "name")
        serialized = U_State_Serializer(state_ref, many=True).data
        self.data_returned = serialized
        self.status_returned = status.HTTP_200_OK
        return

    def __get_state_sel(self, pk=None):
        try:
            state_ref = U_State.objects.get(id=pk)
            serialized = U_State_Serializer(state_ref, many=False).data
            self.data_returned = serialized
            self.status_returned = status.HTTP_200_OK
        except U_State.DoesNotExist:
            self.data_returned = INVALID_ID
            self.status_returned = status.HTTP_404_NOT_FOUND
        return

    def __get_country_sel(self, pk=None):
        state_ref = U_State.objects.filter(country_id=pk).order_by("name")
        serialized = U_State_Serializer(state_ref, many=True).data
        self.data_returned = serialized
        self.status_returned = status.HTTP_200_OK
        return

    def get(self, request, pk=None, pkk=None):
        self.__initial(pk, pkk)
        if self.pk == None:
            if self.pkk == None:
                self.__get_state_all()
            else:
                self.__get_state_sel(pk=pkk)
        else:
            self.__get_country_sel(pk=pk)
        return Response(data=self.data_returned, status=self.status_returned)

    def __edit_state(self, pk, data):
        data["name"] = data["name"].upper()
        try:
            state_ref = U_State.objects.get(id=pk)
            state_ref.name = data["name"]
            try:
                state_ref.country_id = U_Country.objects.get(id=data["country_id"])
            except U_Country.DoesNotExist:
                self.data_returned = INVALID_ID
                self.status_returned = status.HTTP_404_NOT_FOUND
            else:
                try:
                    state_ref.save()
                    data["id"] = pk
                    self.data_returned = data
                    self.status_returned = status.HTTP_201_CREATED
                except IntegrityError as e:
                    if str(e) == "UNIQUE constraint failed: utilities_u_state.name":
                        self.data_returned = "NON UNIQUE NAME"
                    self.status_returned = status.HTTP_409_CONFLICT
        except U_State.DoesNotExist:
            self.data_returned = INVALID_ID
            self.status_returned = status.HTTP_404_NOT_FOUND
        return

    def put(self, request, pk=None, pkk=None):
        self.__initial(pk, pkk)
        if self.pkk == None:
            self.data_returned = "/utilities/state//<id>"
            self.status_returned = status.HTTP_400_BAD_REQUEST
        else:
            self.__edit_state(pk=pkk, data=request.data)
        return Response(data=self.data_returned, status=self.status_returned)

    def __delete_state(self, pk=None):
        try:
            state_ref = U_State.objects.get(id=pk)
            try:
                state_ref.delete()
                self.data_returned = "DELETED"
                self.status_returned = status.HTTP_200_OK
            except:
                self.data_returned = "[CRUD] DELETED ERROR"
                self.status_returned = status.HTTP_400_BAD_REQUEST
        except U_State.DoesNotExist:
            self.data_returned = INVALID_ID
            self.status_returned = status.HTTP_404_NOT_FOUND
        return

    def delete(self, request, pk=None, pkk=None):
        self.__initial(pk, pkk)
        if self.pkk == None:
            data_returned = "/utilities/state//<id>"
            status_returned = status.HTTP_400_BAD_REQUEST
        else:
            self.__delete_state(pk=pkk)
        return Response(data=self.data_returned, status=self.status_returned)
