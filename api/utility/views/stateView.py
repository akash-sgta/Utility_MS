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
from utility.models import State
from utility.serializers import State_Serializer
from access.security.authenticate import Authentication
from access.security.authorization import Authorization


# --------------------------------------------------------------------------
# CONSTANTS
# --------------------------------------------------------------------------
from utility.extra.constant import INVALID_ID, ERROR_CRUD_GEN, ERROR_CRUD_U, ERROR_CRUD_D, SUCCESS_CRUD_D, ERROR_CRUD_C

ERROR = "ERROR"

# --------------------------------------------------------------------------
# CODE
# ---------------------------------------------------------------------------
class State_View(APIView):

    renderer_classes = [JSONRenderer]
    authentication_classes = [Authentication]
    permission_classes = [Authorization]

    def __initial(self, pk=None, pkk=None):
        self.pk = None if pk in (None, "", 0) else int(pk)
        self.pkk = None if pkk in (None, "", 0) else int(pkk)
        self.data_returned = None
        self.status_returned = status.HTTP_404_NOT_FOUND

    # ====================================================================
    def __create_state(self, data):
        data["name"] = data["name"].upper()
        serialized = State_Serializer(data=data)
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

    def post(self, request, pk=None, pkk=None):
        self.__initial(pk, pkk)
        self.__create_state(data=request.data)
        return Response(data=self.data_returned, status=self.status_returned)

    # ====================================================================
    def __read_state_all(self):
        state_ref = State.objects.all().order_by("country_id", "name")
        serialized = State_Serializer(state_ref, many=True).data
        self.data_returned = serialized
        self.status_returned = status.HTTP_200_OK
        return

    def __read_state_sel(self):
        try:
            state_ref = State.objects.get(id=self.pkk)
            serialized = State_Serializer(state_ref, many=False).data
            self.data_returned = serialized
            self.status_returned = status.HTTP_200_OK
        except State.DoesNotExist:
            self.data_returned = INVALID_ID
            self.status_returned = status.HTTP_404_NOT_FOUND
        return

    def __read_country_sel(self):
        state_ref = State.objects.filter(country_id=self.pk).order_by("name")
        serialized = State_Serializer(state_ref, many=True).data
        self.data_returned = serialized
        self.status_returned = status.HTTP_200_OK
        return

    def get(self, request, pk=None, pkk=None):
        self.__initial(pk, pkk)
        if self.pk == None:
            if self.pkk == None:
                self.__read_state_all()
            else:
                self.__read_state_sel()
        else:
            self.__read_country_sel()
        return Response(data=self.data_returned, status=self.status_returned)

    # ====================================================================
    def __update_state(self, data):
        data["name"] = data["name"].upper()
        try:
            state_ref = State.objects.get(id=self.pkk)
            state_ser = State_Serializer(state_ref, data=data)
            if state_ser.is_valid():
                try:
                    state_ser.save()
                    self.data_returned = state_ser.data
                    self.status_returned = status.HTTP_201_CREATED
                except Exception as e:
                    self.data_returned = ERROR_CRUD_GEN
                    self.data_returned[ERROR] = str(e)
                    self.status_returned = status.HTTP_400_BAD_REQUEST
            else:
                self.data_returned = ERROR_CRUD_GEN
                self.data_returned[ERROR] = state_ser.errors
                self.status_returned = status.HTTP_400_BAD_REQUEST
        except State.DoesNotExist:
            self.data_returned = INVALID_ID
            self.status_returned = status.HTTP_404_NOT_FOUND
        return

    def put(self, request, pk=None, pkk=None):
        self.__initial(pk, pkk)
        if self.pkk == None:
            self.data_returned = ERROR_CRUD_GEN
            self.data_returned[ERROR] = "/utility/state/<id>"
            self.status_returned = status.HTTP_400_BAD_REQUEST
        else:
            self.__update_state(data=request.data)
        return Response(data=self.data_returned, status=self.status_returned)

    # ====================================================================
    def __delete_state(self):
        try:
            state_ref = State.objects.get(id=self.pkk)
            try:
                state_ref.delete()
                self.data_returned = SUCCESS_CRUD_D
                self.status_returned = status.HTTP_200_OK
            except:
                self.data_returned = ERROR_CRUD_D
                self.status_returned = status.HTTP_400_BAD_REQUEST
        except State.DoesNotExist:
            self.data_returned = INVALID_ID
            self.status_returned = status.HTTP_404_NOT_FOUND
        return

    def delete(self, request, pk=None, pkk=None):
        self.__initial(pk, pkk)
        if self.pkk == None:
            self.data_returned = ERROR_CRUD_GEN
            self.data_returned[ERROR] = "/utility/state/<id>"
            status_returned = status.HTTP_400_BAD_REQUEST
        else:
            self.__delete_state()
        return Response(data=self.data_returned, status=self.status_returned)
