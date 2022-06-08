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
from copy import deepcopy
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# --------------------------------------------------

from utilUtilities.models import Notification
from utilUtilities.serializers import Notification_Serializer
from utilUtilities.views.utility.constant import Constant


# =========================================================================================
#                                       CONSTANT
# =========================================================================================

# =========================================================================================
#                                       CODE
# =========================================================================================
class NotificationView(APIView):
    renderer_classes = [JSONRenderer]
    authentication_classes = []

    def __init__(self, query1=None, query2=None):
        super(NotificationView, self).__init__()
        self.DB_KEYS = (
            "id",
            "country",
            "name",
        )
        self.SR_KEYS = (
            "ID",
            "SEARCH",
        )
        self.data_returned = deepcopy(Constant.RETURN_JSON)
        self.status_returned = status.HTTP_400_BAD_REQUEST
        self.query1 = query1.upper() if query1 not in Constant.NULL else None
        self.query2 = query2.upper() if query2 not in Constant.NULL else None
        return

    def _create_query(self, flag=True) -> str:
        _return = f"sys={Constant.SETTINGS_SYSTEM}{Constant.COMA}"
        if self.query2 not in Constant.NULL:
            word = self.query2.split(Constant.COMA)
            for i in range(len(word)):
                word[i] = word[i].split(Constant.EQUAL)
                word[i][0] = word[i][0].strip().lower()
                word[i][1] = word[i][1].strip()
                if word[i][0] in self.DB_KEYS:
                    if flag:
                        _return += f"{word[i][0]}__icontains{Constant.EQUAL2}'{word[i][1]}'{Constant.COMA}"
                    else:
                        _return += f"{word[i][0]}__in{Constant.EQUAL2}'{word[i][1]}'{Constant.COMA}"
        return _return


class NotificationView_asUser(NotificationView):
    permission_classes = []

    def __init__(self, query1=None, query2=None):
        super(NotificationView_asUser, self).__init__(
            query1=query1, query2=query2
        )

    # =============================================================
    def __create_specific(self, data: dict) -> None:
        self.data_returned[Constant.MESSAGE] = Constant.METHOD_NOT_ALLOWED
        self.status_returned = status.HTTP_405_METHOD_NOT_ALLOWED
        return

    def post(self, request, word: str, pk: str):
        self.__init__(query1=word, query2=pk)
        self.__create_specific(data=request.data)
        return Response(data=self.data_returned, status=self.status_returned)

    # =============================================================
    def __read_specific(self) -> None:
        self.data_returned[Constant.STATUS] = False
        self.data_returned[Constant.MESSAGE] = Constant.METHOD_NOT_ALLOWED
        self.status_returned = status.HTTP_405_METHOD_NOT_ALLOWED
        return

    def get(self, request, word: str, pk: str):
        self.__init__(query1=word, query2=pk)
        self.__read_specific()
        return Response(data=self.data_returned, status=self.status_returned)

    # =============================================================
    def __update_specific(self, data: dict):
        self.data_returned[Constant.STATUS] = False
        self.data_returned[Constant.MESSAGE] = Constant.METHOD_NOT_ALLOWED
        self.status_returned = status.HTTP_405_METHOD_NOT_ALLOWED
        return

    def put(self, request, word: str, pk: str):
        self.__init__(query1=word, query2=pk)
        self.__update_specific(data=request.data)
        return Response(data=self.data_returned, status=self.status_returned)

    # =============================================================
    def __delete_specific(self):
        self.data_returned[Constant.STATUS] = False
        self.data_returned[Constant.MESSAGE] = Constant.METHOD_NOT_ALLOWED
        self.status_returned = status.HTTP_405_METHOD_NOT_ALLOWED
        return

    def delete(self, request, word: str, pk: str):
        self.__init__(query1=word, query2=pk)
        self.__delete_specific()
        return Response(data=self.data_returned, status=self.status_returned)


class NotificationView_asAdmin(NotificationView_asUser):
    permission_classes = []

    def __init__(self, query1=None, query2=None):
        super(NotificationView_asAdmin, self).__init__(
            query1=query1, query2=query2
        )

    # =============================================================
    def __create_specific(self, data: dict) -> None:
        Notification_ser = Notification_Serializer(data=data)
        if Notification_ser.is_valid():
            try:
                Notification_ser.save()
            except Exception as e:
                self.data_returned[Constant.STATUS] = False
                self.data_returned[Constant.MESSAGE] = str(e)
                self.status_returned = status.HTTP_406_NOT_ACCEPTABLE
            else:
                Notification_ser = Notification_ser.data
                self.data_returned[Constant.STATUS] = True
                self.data_returned[Constant.DATA].append(Notification_ser)
                self.status_returned = status.HTTP_201_CREATED
        else:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Notification_ser.errors
            self.status_returned = status.HTTP_406_NOT_ACCEPTABLE
        return

    def post(self, request, word: str, pk: str):
        self.__init__(query1=word, query2=pk)
        self.__create_specific(data=request.data)
        return Response(data=self.data_returned, status=self.status_returned)

    # =============================================================
    def get(self, request, word: str, pk: str):
        return super(NotificationView_asAdmin, self).get(
            request=request, word=word, pk=pk
        )

    # =============================================================
    def __update_specific(self, data: dict) -> None:
        try:
            Notification_ref = Notification.objects.get(
                sys=Constant.SETTINGS_SYSTEM, id=int(self.query2)
            )
        except Notification.DoesNotExist:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.INVALID_SPARAMS
            self.status_returned = status.HTTP_404_NOT_FOUND
        except ValueError:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.INVALID_SPARAMS
            self.status_returned = status.HTTP_404_NOT_FOUND
        else:
            Notification_ser = Notification_Serializer(
                instance=Notification_ref, data=data, partial=True
            )
            if Notification_ser.is_valid():
                try:
                    Notification_ser.save()
                except Exception as e:
                    self.data_returned[Constant.STATUS] = False
                    self.data_returned[Constant.MESSAGE] = str(e)
                    self.status_returned = status.HTTP_406_NOT_ACCEPTABLE
                else:
                    Notification_ser = Notification_ser.data
                    self.data_returned[Constant.STATUS] = True
                    self.data_returned[Constant.DATA].append(Notification_ser)
                    self.status_returned = status.HTTP_201_CREATED
            else:
                self.data_returned[Constant.STATUS] = False
                self.data_returned[Constant.MESSAGE] = Notification_ser.errors
                self.status_returned = status.HTTP_406_NOT_ACCEPTABLE
        return

    def put(self, request, word: str, pk: str):
        self.__init__(query1=word, query2=pk)
        if self.query2 in Constant.NULL:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.INVALID_SPARAMS
            self.status_returned = status.HTTP_400_BAD_REQUEST
        else:
            self.__update_specific(data=request.data)
        return Response(data=self.data_returned, status=self.status_returned)

    # =============================================================
    def __delete_specific(self):
        try:
            Notification_ref = Notification.objects.get(
                sys=Constant.SETTINGS_SYSTEM, id=int(self.query2)
            )
        except Notification.DoesNotExist:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.INVALID_SPARAMS
            self.status_returned = status.HTTP_404_NOT_FOUND
        except ValueError:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.INVALID_SPARAMS
            self.status_returned = status.HTTP_404_NOT_FOUND
        else:
            Notification_ser = Notification_Serializer(
                Notification_ref, many=False
            ).data
            Notification_ref.delete()
            self.data_returned[Constant.STATUS] = True
            self.data_returned[Constant.DATA].append(Notification_ser)
            self.status_returned = status.HTTP_200_OK
        return

    def delete(self, request, word: str, pk: str):
        self.__init__(query1=word, query2=pk)
        if self.query2 in Constant.NULL:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.INVALID_SPARAMS
            self.status_returned = status.HTTP_400_BAD_REQUEST
        else:
            self.__delete_specific()
        return Response(data=self.data_returned, status=self.status_returned)