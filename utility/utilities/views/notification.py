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

from utility.views.authenticator import Authenticator
from utilities.models import Notification
from utilities.serializers import Notification_Serializer
from utilities.views.utility.constant import Constant
from utilities.views.utility.batchJob import BatchJob, TGBot
from utilities.views.mailer import MailerView_asUser
from utilities.views.telegram import TelegramView_asUser

# =========================================================================================
#                                       CONSTANT
# =========================================================================================
BOT_THREAD = TGBot()
NOTIFICATION = "notification"
MAILER = "mailer"
TELEGRAM = "telegram"

# =========================================================================================
#                                       CODE
# =========================================================================================
class NotificationView(APIView):
    renderer_classes = [JSONRenderer]
    authentication_classes = [Authenticator]

    def __init__(self, query1=None, query2=None):
        super(NotificationView, self).__init__()
        self.DB_KEYS = (
            "id",
            "api",
            "subject",
        )
        self.SR_KEYS = (
            "id",
            "search",
            "trigger",
            "bot",
        )
        self.data_returned = deepcopy(Constant.RETURN_JSON)
        self.status_returned = status.HTTP_400_BAD_REQUEST
        self.query1 = query1.lower() if query1 not in Constant.NULL else None
        self.query2 = query2.lower() if query2 not in Constant.NULL else None
        return

    def _create_query(self, flag=True) -> str:
        query = f"sys={Constant.SETTINGS_SYSTEM}{Constant.COMA}"
        if self.query2 not in Constant.NULL:
            word = self.query2.split(Constant.COMA)
            for i in range(len(word)):
                word[i] = word[i].split(Constant.EQUAL)
                if len(word[i]) != 2:
                    raise NameError
                word[i][0] = word[i][0].strip()
                word[i][1] = word[i][1].strip()
                if word[i][0] in self.DB_KEYS:
                    if flag:
                        query += f"{word[i][0]}__icontains{Constant.EQUAL2}'{word[i][1]}'{Constant.COMA}"
                    else:
                        query += f"{word[i][0]}__in{Constant.EQUAL2}'{word[i][1]}'{Constant.COMA}"
        return query


class NotificationView_asUser(NotificationView):
    permission_classes = []

    def __init__(self, query1=None, query2=None):
        super(NotificationView_asUser, self).__init__(
            query1=query1, query2=query2
        )

    # =============================================================
    def __create_specific(self, data: dict) -> None:
        notification_ser = Notification_Serializer(data=data)
        if notification_ser.is_valid():
            try:
                notification_ser.save()
            except Exception as e:
                self.data_returned[Constant.STATUS] = False
                self.data_returned[Constant.MESSAGE] = str(e)
                self.status_returned = status.HTTP_406_NOT_ACCEPTABLE
            else:
                notification_ser = notification_ser.data
                self.data_returned[Constant.STATUS] = True
                self.data_returned[Constant.DATA].append(notification_ser)
                self.status_returned = status.HTTP_201_CREATED
        else:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = notification_ser.errors
            self.status_returned = status.HTTP_406_NOT_ACCEPTABLE
        return

    def post(self, request, word: str, pk: str, internal: bool = False):
        self.__init__(query1=word, query2=pk)
        try:
            mailer_data = deepcopy(request.data["mailer"])
            telegram_data = deepcopy(request.data["telegram"])
            request.data["api"] = request.user.id
            if request.data["api"] is None:
                raise Exception(Constant.INVALID_API)
        except Exception as e:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = str(e)
            self.status_returned = status.HTTP_400_BAD_REQUEST
        else:
            self.__create_specific(data=request.data)
            try:
                if self.data_returned[Constant.STATUS]:
                    notification_id = self.data_returned[Constant.DATA][0][
                        "id"
                    ]
                else:
                    notification_id = None

                if notification_id is not None:
                    # -------------------------------------
                    # Mailer Post
                    # -------------------------------------
                    if mailer_data not in Constant.NULL:
                        mailer_data[NOTIFICATION] = notification_id
                        request.data.clear()
                        request.data.update(mailer_data)
                        mailer = MailerView_asUser().post(
                            request=request, word=word, pk=pk, internal=True
                        )
                        if mailer.data[Constant.STATUS]:
                            self.data_returned[Constant.DATA][0][
                                MAILER
                            ] = mailer.data[Constant.DATA][0]
                        else:
                            self.data_returned[Constant.DATA][0][
                                MAILER
                            ] = None
                    # -------------------------------------
                    # Telegram Post
                    # -------------------------------------
                    if telegram_data not in Constant.NULL:
                        telegram_data[NOTIFICATION] = notification_id
                        request.data.clear()
                        request.data.update(telegram_data)
                        telegram = TelegramView_asUser().post(
                            request=request, word=word, pk=pk, internal=True
                        )
                        if telegram.data[Constant.STATUS]:
                            self.data_returned[Constant.DATA][0][
                                TELEGRAM
                            ] = telegram.data[Constant.DATA][0]
                        else:
                            self.data_returned[Constant.DATA][0][
                                TELEGRAM
                            ] = None
                    # -------------------------------------
                    # Check if any leaf is created
                    # -------------------------------------
                    if (
                        self.data_returned[Constant.DATA][0][MAILER]
                        == self.data_returned[Constant.DATA][0][TELEGRAM]
                        == None
                    ):
                        raise Exception("Notification not generated")
            except Exception as e:
                # -------------------------------------
                # Rollback
                # -------------------------------------
                if notification_id is not None:
                    self.delete(
                        request=request,
                        word="id",
                        pk=str(notification_id),
                        internal=True,
                    )
                self.data_returned[Constant.STATUS] = False
                self.data_returned[Constant.DATA] = Constant.BLANK_LIST
                self.data_returned[Constant.MESSAGE] = str(e)
                self.status_returned = status.HTTP_400_BAD_REQUEST
        return Response(data=self.data_returned, status=self.status_returned)

    # =============================================================
    def _read_specific(self) -> None:
        try:
            notification_ref = Notification.objects.get(
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
        except TypeError:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.INVALID_URL
            self.status_returned = status.HTTP_404_NOT_FOUND
        else:
            notification_ser = Notification_Serializer(
                notification_ref, many=False
            ).data
            self.data_returned[Constant.STATUS] = True
            self.data_returned[Constant.DATA].append(notification_ser)
            self.status_returned = status.HTTP_200_OK
        return

    def get(self, request, word: str, pk: str):
        self.__init__(query1=word, query2=pk)
        self._read_specific()
        return Response(data=self.data_returned, status=self.status_returned)

    # =============================================================
    def __update_specific(self, data: dict):
        self.data_returned[Constant.STATUS] = False
        self.data_returned[Constant.MESSAGE] = Constant.METHOD_NOT_ALLOWED
        self.status_returned = status.HTTP_405_METHOD_NOT_ALLOWED
        return

    def put(self, request, word: str, pk: str, internal: bool = False):
        self.__init__(query1=word, query2=pk)
        if not internal:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.METHOD_NOT_ALLOWED
            self.status_returned = status.HTTP_405_METHOD_NOT_ALLOWED
        else:
            self.__update_specific(data=request.data)
        return Response(data=self.data_returned, status=self.status_returned)

    # =============================================================
    def __delete_specific(self):
        try:
            notification_ref = Notification.objects.get(
                sys=Constant.SETTINGS_SYSTEM, id=int(self.query2)
            )
        except Notification.DoesNotExist:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.INVALID_SPARAMS
            self.status_returned = status.HTTP_404_NOT_FOUND
        else:
            notification_ser = Notification_Serializer(
                notification_ref, many=False
            ).data
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.DATA].append(notification_ser)
            notification_ref.delete()
        return

    def delete(self, request, word: str, pk: str, internal: bool = False):
        self.__init__(query1=word, query2=pk)
        if not internal:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.METHOD_NOT_ALLOWED
            self.status_returned = status.HTTP_405_METHOD_NOT_ALLOWED
        else:
            self.__delete_specific()
        return Response(data=self.data_returned, status=self.status_returned)


class NotificationView_asAdmin(NotificationView_asUser):
    permission_classes = []

    def __init__(self, query1=None, query2=None):
        super(NotificationView_asAdmin, self).__init__(
            query1=query1, query2=query2
        )

    # =============================================================
    def post(self, request, word: str, pk: str):
        return super(NotificationView_asAdmin, self).post(
            request=request, word=word, pk=pk
        )

    # =============================================================
    def __read_all(self) -> None:
        try:
            notification_ref = Notification.objects.all().order_by("id")
            if len(notification_ref) == 0:
                raise Notification.DoesNotExist
        except Notification.DoesNotExist:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.NO_CONTENT
            self.status_returned = status.HTTP_204_NO_CONTENT
        else:
            notification_ser = Notification_Serializer(
                notification_ref, many=True
            ).data
            self.data_returned[Constant.STATUS] = True
            self.data_returned[Constant.DATA] = notification_ser
            self.status_returned = status.HTTP_200_OK
        return

    def __read_search(self) -> None:
        try:
            notification_ref = eval(
                f'Notification.objects.filter({self._create_query()}).order_by("id")'
            )
            if len(notification_ref) == 0:
                raise Notification.DoesNotExist
        except Notification.DoesNotExist:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.NO_CONTENT
            self.status_returned = status.HTTP_204_NO_CONTENT
        except NameError:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.INVALID_SPARAMS
            self.status_returned = status.HTTP_400_BAD_REQUEST
        else:
            notification_ser = Notification_Serializer(
                notification_ref, many=True
            ).data
            self.data_returned[Constant.STATUS] = True
            self.data_returned[Constant.DATA] = notification_ser
            self.status_returned = status.HTTP_200_OK
        return

    def get(self, request, word: str, pk: str):
        self.__init__(query1=word, query2=pk)
        try:
            if self.query1 in self.SR_KEYS:
                if self.query1 == self.SR_KEYS[0]:  # id
                    if self.query2 in Constant.NULL:
                        self.__read_all()
                    else:
                        self._read_specific()
                elif self.query1.lower() == self.SR_KEYS[1]:  # search
                    if self.query2 in Constant.NULL:
                        raise Exception(Constant.INVALID_SPARAMS)
                    else:
                        self.__read_search()
                elif self.query1 == self.SR_KEYS[2]:  # trigger
                    try:
                        _status = int(self.query2)
                    except Exception as e:
                        _status = Constant.PENDING
                    finally:
                        self.query2 = f"statuseq{_status}"
                        self.__read_search()
                        # ---------------------------------
                        batch_thread = BatchJob(
                            mailer=False, api=1, status=_status
                        )
                        batch_thread.start()
                    self.status_returned = status.HTTP_202_ACCEPTED
                elif self.query1 == self.SR_KEYS[3]:  # bot
                    if not BOT_THREAD.is_alive():
                        BOT_THREAD.start()
                    else:
                        BOT_THREAD.stop()
                    self.status_returned = status.HTTP_202_ACCEPTED
                else:
                    raise Exception(Constant.INVALID_SPARAMS)
            else:
                raise Exception(Constant.INVALID_SPARAMS)
        except Exception as e:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = str(e)
            self.status_returned = status.HTTP_400_BAD_REQUEST
        else:
            self.data_returned[Constant.STATUS] = True

        return Response(data=self.data_returned, status=self.status_returned)

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
