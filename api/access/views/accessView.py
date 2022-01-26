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
from access.serializers import Identity_Serializer
from access.models import Identity

# --------------------------------------------------------------------------
# CONSTANTS
# --------------------------------------------------------------------------
from utility.extra.constant import ERROR_CRUD_C, INVALID_ID, ERROR_CRUD_GEN

ERROR = "ERROR"

# --------------------------------------------------------------------------
# CODE
# --------------------------------------------------------------------------
class AccessView(APIView):

    renderer_classes = [JSONRenderer]
    authentication_classes = [Authentication]
    permission_classes = [Authorization]

    def __initialize(self, pk=None):
        self.data_returned = ERROR_CRUD_C
        self.status_returned = status.HTTP_400_BAD_REQUEST
        self.pk = pk if pk not in (None, "", 0) else None
        return

    # =============================================================
    def __create_identity(self, data):
        identity_ser = Identity_Serializer(data=data)
        if identity_ser.is_valid():
            try:
                identity_ser.save()
                self.data_returned = identity_ser.data
                self.status_returned = status.HTTP_201_CREATED
            except Exception as e:
                self.data_returned = ERROR_CRUD_GEN
                self.data_returned[ERROR] = str(e)
                self.status_returned = status.HTTP_400_BAD_REQUEST
        return

    def post(self, request, pk=None):
        self.__initialize()
        self.__create_identity(data=request.data)
        return Response(data=self.data_returned, status=self.status_returned)

    # =============================================================
    def __read_all(self):
        identity_ref = Identity.objects.all()
        identity_ser = Identity_Serializer(identity_ref, many=True).data
        self.data_returned = identity_ser
        self.status_returned = status.HTTP_200_OK
        return

    def __read_specific(self):
        try:
            identity_ref = Identity.objects.get(id=self.pk)
            identity_ser = Identity_Serializer(identity_ref, many=False).data
            self.data_returned = identity_ser
            self.status_returned = status.HTTP_200_OK
        except Identity.DoesNotExist:
            self.data_returned = INVALID_ID
            self.status_returned = status.HTTP_400_BAD_REQUEST
        return

    def get(self, request, pk=None):
        self.__initialize(pk=pk)
        if self.pk == None:
            self.__read_all()
        else:
            self.__read_specific()
        return Response(data=self.data_returned, status=self.status_returned)

    # =============================================================
    def __edit_identity(self, data):
        try:
            identity_ref = Identity.objects.get(id=self.pk)
            identity_ser = Identity_Serializer(identity_ref, data=data)
            if identity_ser.is_valid():
                try:
                    identity_ser.save()
                    self.data_returned = identity_ser.data
                    self.status_returned = status.HTTP_201_CREATED
                except Exception as e:
                    self.data_returned = ERROR_CRUD_GEN
                    self.data_returned[ERROR] = str(e)
                    self.status_returned = status.HTTP_400_BAD_REQUEST
        except Identity.DoesNotExist:
            self.data_returned = INVALID_ID
            self.status_returned = status.HTTP_404_NOT_FOUND
        return

    def put(self, request, pk=None):
        self.__initialize(pk=pk)
        if self.pk == None:
            self.data_returned = ERROR_CRUD_GEN
            self.data_returned[ERROR] = "/access/api/<id>"
            self.status_returned = status.HTTP_400_BAD_REQUEST
        else:
            self.__edit_identity(data=request.data)
        return Response(data=self.data_returned, status=self.status_returned)

    # =============================================================
    def __delete_identity(self):
        try:
            identity_ref = Identity.objects.get(id=self.pk)
            if identity_ref.is_admin:
                self.data_returned = ERROR_CRUD_GEN
                self.data_returned[ERROR] = "Unauthorized"
                self.status_returned = status.HTTP_401_UNAUTHORIZED
        except Identity.DoesNotExist:
            self.data_returned = INVALID_ID
            status_returned = status.HTTP_404_NOT_FOUND
        return

    def delete(self, request, pk=None):
        self.__initialize(pk=pk)
        if self.pk == None:
            self.data_returned = ERROR_CRUD_GEN
            self.data_returned[ERROR] = "/access/api/<id>"
            status_returned = status.HTTP_400_BAD_REQUEST
        else:
            self.__delete_identity()
        return Response(data=self.data_returned, status=self.status_returned)
