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
from django.core.exceptions import FieldError
from django.urls import reverse

# --------------------------------------------------

from api.models import Request
from utilities.models import Mailer, Telegram
from api.serializers import Request_Serializer
from utilities.views.notification import NotificationView_asAdmin
from utilities.views.urlShort import UrlShortView_asAdmin
from utilities.util.constant import Constant
from utilities.util.utility import Utility
from utilities.util.batchJob import BatchJob

# =========================================================================================
#                                       CONSTANT
# =========================================================================================
SUBJECT = "DO NOT REPLY | UTILITY | API ACCESS REQUEST"
BODY_HEADER = """
==========[This is an auto generated email]==========
"""
BODY_MAIN = """
Greetings,

Your API access request has been generated.
Description:
"""
BODY_FOOTER = """
==========[ This is a unmonitored mailbox ]==========
==========[      Please do not reply      ]==========
"""
STATUS = dict(map(reversed, Constant.STATUS_CHOICE))
THREAD_M = "MAIL_TRG_REQ"
THREAD_T = "TG_TRG_REQ"
# =========================================================================================
#                                       CODE
# =========================================================================================
class RequestView(APIView):
    renderer_classes = [JSONRenderer]
    authenticnotifation_classes = []

    def __init__(self, query1=None, query2=None):
        super(RequestView, self).__init__()
        self.DB_KEYS = (
            "id",
            "email",
            "phone_no",
        )
        self.SR_KEYS = (
            "id",
            "search",
        )
        self.data_returned = deepcopy(Constant.RETURN_JSON)
        self.status_returned = status.HTTP_400_BAD_REQUEST
        self.query1 = query1.lower() if query1 not in Constant.NULL else None
        self.query2 = query2.lower() if query2 not in Constant.NULL else None
        return

    def _create_query(self, flag=True) -> str:
        _return = f"sys={Constant.SETTINGS_SYSTEM}{Constant.COMA}"
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
                        _return += f"{word[i][0]}__icontains{Constant.EQUAL2}'{word[i][1]}'{Constant.COMA}"
                    else:
                        _return += f"{word[i][0]}__in{Constant.EQUAL2}'{word[i][1]}'{Constant.COMA}"
        return _return


class RequestView_asUser(RequestView):
    permission_classes = []

    def __init__(self, query1=None, query2=None):
        super(RequestView_asUser, self).__init__(query1=query1, query2=query2)

    # =============================================================
    def _create_specific(self, data: dict) -> None:
        request_ser = Request_Serializer(data=data)
        if request_ser.is_valid():
            try:
                request_ser.save()
            except Exception as e:
                self.data_returned[Constant.STATUS] = False
                self.data_returned[Constant.MESSAGE] = str(e)
                self.status_returned = status.HTTP_406_NOT_ACCEPTABLE
            else:
                request_ser = request_ser.data
                self.data_returned[Constant.STATUS] = True
                self.data_returned[Constant.DATA].append(request_ser)
                self.status_returned = status.HTTP_201_CREATED
        else:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = request_ser.errors
            self.status_returned = status.HTTP_406_NOT_ACCEPTABLE
        return

    def _send_notification(self, request) -> bool:
        request_tmp = request
        # ------------------------------------
        # Post Notification
        # ------------------------------------
        notification_data = Constant.NOTIFICATION_DICT
        notification_data[Constant.NOTIFICATION_SUBJECT] = SUBJECT
        body = f"""
        EMAIL       : {self.data_returned[Constant.DATA][0]["email"]}
        TG          : {self.data_returned[Constant.DATA][0]["tg_id"]}
        REASON      : {self.data_returned[Constant.DATA][0]["reason"]}
        STATUS      : {STATUS[self.data_returned[Constant.DATA][0]["status"]]}
        DATE        : {Utility.msToStr(self.data_returned[Constant.DATA][0]["created_on"])}
        TIMEZONE    : {Constant.SETTINGS_TIMEZONE}
        """
        url_txt = Constant.BLANK_STR
        try:
            url_data = {
                "url": reverse(
                    viewname="REQUEST_AS_ADMIN",
                    kwargs={
                        "word": "id",
                        "pk": f'{request_tmp.data[Constant.DATA][0]["id"]}',
                    },
                ),
            }
        except Exception as e:
            pass
        else:
            request_tmp.data.clear()
            request_tmp.data.update(url_data)
            url_post = UrlShortView_asAdmin().post(
                request=request_tmp,
                word=Constant.ID,
                pk=Constant.BLANK_STR,
            )
            if url_post[Constant.STATUS]:
                try:
                    rev_url = reverse(
                        viewname="URLSHORT_AS_ADMIN",
                        kwargs={
                            "word": "key",
                            "pk": f'{url_post[Constant.DATA][0]["key"]}',
                        },
                    )
                except Exception as e:
                    pass
                else:
                    url_txt = f"\nLINK : {rev_url}"
        body = f"{BODY_HEADER}\n{BODY_MAIN}\n{body}{url_txt}\n{BODY_FOOTER}"
        notification_data[Constant.NOTIFICATION_BODY] = body
        notification_data[Constant.NOTIFICATION_MAILER][
            Constant.NOTIFICATION_RECEIVER
        ] = f'{self.data_returned[Constant.DATA][0]["email"]}'
        notification_data[Constant.NOTIFICATION_TELEGRAM][
            Constant.NOTIFICATION_RECEIVER
        ] = f'{self.data_returned[Constant.DATA][0]["tg_id"]}'
        request_tmp.data.clear()
        request_tmp.data.update(notification_data)
        notif = NotificationView_asAdmin().post(
            request=request_tmp,
            word=Constant.ID,
            pk=Constant.BLANK_STR,
        )
        return_stat = notif.data[Constant.STATUS]
        if return_stat:
            notif_id = notif.data[Constant.DATA][0]["id"]
            # ------------------------------------
            # Direct Mail through Thread
            # ------------------------------------
            if (
                notif.data[Constant.DATA][0][Constant.NOTIFICATION_MAILER]
                is not None
            ):
                mailer_id = notif.data[Constant.DATA][0][
                    Constant.NOTIFICATION_MAILER
                ][Constant.ID]
                try:
                    BatchJob(
                        tname=THREAD_M,
                        mailer=True,
                        api=request.user.id,
                        obj_id=(notif_id, mailer_id),
                    ).start()
                except Exception as e:
                    print(f"ERROR : {str(e)}")
                    pass  # TODO : Nothing to do at this point
            if (
                notif.data[Constant.DATA][0][Constant.NOTIFICATION_TELEGRAM]
                is not None
            ):
                telegram_id = notif.data[Constant.DATA][0][
                    Constant.NOTIFICATION_TELEGRAM
                ][Constant.ID]
                try:
                    BatchJob(
                        tname=THREAD_T,
                        mailer=False,
                        api=request.user.id,
                        obj_id=(notif_id, telegram_id),
                    ).start()
                except Exception as e:
                    print(f"ERROR : {str(e)}")
                    pass  # TODO : Nothing to do at this point
        return return_stat

    def post(self, request, word: str, pk: str):
        self.__init__(query1=word, query2=pk)
        self._create_specific(data=request.data)
        if self.data_returned[Constant.STATUS]:
            try:
                self._send_notification()
            except Exception as e:
                pass
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


class RequestView_asAdmin(RequestView_asUser):
    permission_classes = []

    def __init__(self, query1=None, query2=None):
        super(RequestView_asAdmin, self).__init__(
            query1=query1, query2=query2
        )

    # =============================================================
    def post(self, request, word: str, pk: str):
        return super(RequestView_asAdmin, self).post(
            request=request, word=word, pk=pk
        )

    # =============================================================
    def __read_all(self) -> None:
        try:
            request_ref = Request.objects.all().order_by("id")
            if len(request_ref) == 0:
                raise Request.DoesNotExist
        except Request.DoesNotExist:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.NO_CONTENT
            self.status_returned = status.HTTP_204_NO_CONTENT
        else:
            request_ser = Request_Serializer(request_ref, many=True).data
            self.data_returned[Constant.STATUS] = True
            self.data_returned[Constant.DATA] = request_ser
            self.status_returned = status.HTTP_200_OK
        return

    def __read_specific(self) -> None:
        try:
            request_ref = Request.objects.get(
                sys=Constant.SETTINGS_SYSTEM, id=int(self.query2)
            )
        except Request.DoesNotExist:
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
            request_ser = Request_Serializer(request_ref, many=False).data
            self.data_returned[Constant.STATUS] = True
            self.data_returned[Constant.DATA].append(request_ser)
            self.status_returned = status.HTTP_200_OK
        return

    def __read_search(self) -> None:
        try:
            try:
                request_ref = eval(
                    f'Request.objects.filter({self._create_query()}).order_by("id")'
                )
            except NameError:
                self.data_returned[Constant.STATUS] = False
                self.data_returned[
                    Constant.MESSAGE
                ] = Constant.INVALID_SPARAMS
                self.status_returned = status.HTTP_400_BAD_REQUEST
            except FieldError:
                try:
                    request_ref = eval(
                        f'Request.objects.filter({self._create_query(flag=False)}).order_by("id")'
                    )
                except NameError:
                    self.data_returned[Constant.STATUS] = False
                    self.data_returned[
                        Constant.MESSAGE
                    ] = Constant.INVALID_SPARAMS
                    self.status_returned = status.HTTP_400_BAD_REQUEST
            if len(request_ref) == 0:
                raise Request.DoesNotExist
        except Request.DoesNotExist:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.NO_CONTENT
            self.status_returned = status.HTTP_204_NO_CONTENT
        else:
            request_ser = Request_Serializer(request_ref, many=True).data
            self.data_returned[Constant.STATUS] = True
            self.data_returned[Constant.DATA] = request_ser
            self.status_returned = status.HTTP_200_OK
        return

    def get(self, request, word: str, pk: str):
        self.__init__(query1=word, query2=pk)
        flag = True
        if self.query1 in self.SR_KEYS:
            if self.query1 == self.SR_KEYS[0]:  # id
                if self.query2 in Constant.NULL:
                    self.__read_all()
                else:
                    self.__read_specific()
            elif self.query1 == self.SR_KEYS[1]:  # search
                if self.query2 in Constant.NULL:
                    flag = False
                else:
                    self.__read_search()
            else:
                flag = False
        else:
            flag = False

        if not flag:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.INVALID_SPARAMS
            self.status_returned = status.HTTP_400_BAD_REQUEST

        return Response(data=self.data_returned, status=self.status_returned)

    # =============================================================
    def __update_specific(self, data: dict) -> None:
        try:
            request_ref = Request.objects.get(
                sys=Constant.SETTINGS_SYSTEM, id=int(self.query2)
            )
        except Request.DoesNotExist:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.INVALID_SPARAMS
            self.status_returned = status.HTTP_404_NOT_FOUND
        except ValueError:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.INVALID_SPARAMS
            self.status_returned = status.HTTP_404_NOT_FOUND
        else:
            request_ser = Request_Serializer(
                instance=request_ref, data=data, partial=True
            )
            if request_ser.is_valid():
                try:
                    request_ser.save()
                except Exception as e:
                    self.data_returned[Constant.STATUS] = False
                    self.data_returned[Constant.MESSAGE] = str(e)
                    self.status_returned = status.HTTP_406_NOT_ACCEPTABLE
                else:
                    request_ser = request_ser.data
                    self.data_returned[Constant.STATUS] = True
                    self.data_returned[Constant.DATA].append(request_ser)
                    self.status_returned = status.HTTP_201_CREATED
            else:
                self.data_returned[Constant.STATUS] = False
                self.data_returned[Constant.MESSAGE] = request_ser.errors
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
            request_ref = Request.objects.get(
                sys=Constant.SETTINGS_SYSTEM, id=int(self.query2)
            )
        except Request.DoesNotExist:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.INVALID_SPARAMS
            self.status_returned = status.HTTP_404_NOT_FOUND
        except ValueError:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.INVALID_SPARAMS
            self.status_returned = status.HTTP_404_NOT_FOUND
        else:
            request_ser = Request_Serializer(request_ref, many=False).data
            request_ref.delete()
            self.data_returned[Constant.STATUS] = True
            self.data_returned[Constant.DATA].append(request_ser)
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
