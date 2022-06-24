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
from math import fabs
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import FieldError
from django.urls import reverse

# --------------------------------------------------

from utility.views.authenticator import Authenticator
from api.models import Api
from api.serializers import Api_Serializer
from utilities.util.constant import Constant
from utilities.util.utility import Utility
from utilities.views.notification import NotificationView_asAdmin
from utilities.views.urlShort import UrlShortView_asAdmin
from utilities.util.batchJob import BatchJob


# =========================================================================================
#                                       CONSTANT
# =========================================================================================
SUBJECT = "DO NOT REPLY | UTILITY | API ACCESS GRANTED"
BODY_HEADER = """
==========[This is an auto generated email]==========
"""
BODY_MAIN = """
Greetings,

Your API access request has been granted.

Description:
"""
BODY_FOOTER = """
==========[ This is a unmonitored mailbox ]==========
==========[      Please do not reply      ]==========
"""
# ------------------------------------------
DIRECTION = dict((key, value) for key, value in Constant.DIRECTION_CHOICE)
# ------------------------------------------
THREAD_M = "MAIL_TRG_REQ"
THREAD_T = "TG_TRG_REQ"
# ------------------------------------------
VNAME_URL = "utilities:URLSHORT_AS_USER"
VNAME_API = "api:API_AS_ADMIN"
# ------------------------------------------
# =========================================================================================
#                                       CODE
# =========================================================================================
class ApiView(APIView):
    renderer_classes = [JSONRenderer]
    authentication_classes = [Authenticator]

    def __init__(self, query1=None, query2=None):
        super(ApiView, self).__init__()
        self.DB_KEYS = (
            "id",
            "name",
            "email",
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


class ApiView_asUser(ApiView):
    permission_classes = []

    def __init__(self, query1=None, query2=None):
        super(ApiView_asUser, self).__init__(query1=query1, query2=query2)

    # =============================================================
    def __create_specific(self, data: dict) -> None:
        self.data_returned[Constant.STATUS] = False
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


class ApiView_asAdmin(ApiView_asUser):
    permission_classes = []

    def __init__(self, query1=None, query2=None):
        super(ApiView_asAdmin, self).__init__(query1=query1, query2=query2)

    # =============================================================
    def __create_specific(self, data: dict) -> None:
        api_ser = Api_Serializer(data=data)
        if api_ser.is_valid():
            try:
                api_ser.save()
            except Exception as e:
                self.data_returned[Constant.STATUS] = False
                self.data_returned[Constant.MESSAGE] = str(e)
                self.status_returned = status.HTTP_406_NOT_ACCEPTABLE
            else:
                api_ser = api_ser.data
                self.data_returned[Constant.STATUS] = True
                self.data_returned[Constant.DATA].append(api_ser)
                self.status_returned = status.HTTP_201_CREATED
        else:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = api_ser.errors
            self.status_returned = status.HTTP_406_NOT_ACCEPTABLE
        return

    def __post_notification(self, request) -> tuple:
        try:
            request_tmp = request
            notification_data = Constant.NOTIFICATION_DICT
            notification_data[Constant.NOTIFICATION_SUBJECT] = SUBJECT
            body = f"""
            NAME        : {self.data_returned[Constant.DATA][0]["name"]}
            EMAIL       : {self.data_returned[Constant.DATA][0]["email"]}
            TG          : {self.data_returned[Constant.DATA][0]["tg_id"]}
            DIRECTION   : {DIRECTION[self.data_returned[Constant.DATA][0]["direction"]]}
            CREATED ON  : {Utility.msToStr(self.data_returned[Constant.DATA][0]["created_on"])}
            TIMEZONE    : {Constant.SETTINGS_TIMEZONE}
            """
            body = f"{BODY_HEADER}\n{BODY_MAIN}{body}"
            notification_data[Constant.NOTIFICATION_BODY] = body
            notification_data[Constant.NOTIFICATION_MAILER][
                Constant.NOTIFICATION_RECEIVER
            ] = f'{self.data_returned[Constant.DATA][0]["email"]}'
            notification_data[Constant.NOTIFICATION_TELEGRAM][
                Constant.NOTIFICATION_RECEIVER
            ] = f'{self.data_returned[Constant.DATA][0]["tg_id"]}'
            request_tmp.data.clear()
            request_tmp.data.update(notification_data)
            notif_post = NotificationView_asAdmin().post(
                request=request_tmp,
                word=Constant.ID,
                pk=Constant.BLANK_STR,
            )
            notif_post = deepcopy(notif_post.data)
            if notif_post[Constant.DATA]:
                notif_id = notif_post[Constant.DATA][0]["id"]
                if notif_post[Constant.DATA][0][Constant.NOTIFICATION_MAILER] is None:
                    mailer_id = None
                else:
                    mailer_id = notif_post[Constant.DATA][0][
                        Constant.NOTIFICATION_MAILER
                    ]["id"]
                if notif_post[Constant.DATA][0][Constant.NOTIFICATION_TELEGRAM] is None:
                    tg_id = None
                else:
                    tg_id = notif_post[Constant.DATA][0][
                        Constant.NOTIFICATION_TELEGRAM
                    ]["id"]
            else:
                return Exception("Failed Notification Post")
        except Exception as e:
            print(f"ERROR : {str(e)}")
            notif_id = mailer_id = tg_id = None
        return (notif_id, mailer_id, tg_id)

    def __post_urlShort(self, request, viewname: str, request_id: int) -> str:
        url_txt = f"\nLINK : {Constant.BLANK_STR}"
        url_id = None
        try:
            request_tmp = request
            try:
                url_data = {
                    "url": reverse(
                        viewname=viewname,
                        kwargs={
                            "word": "id",
                            "pk": f"{request_id}",
                        },
                    ),
                }
            except Exception as e:
                raise Exception("URL post failed")
            else:
                request_tmp.data.clear()
                request_tmp.data.update(url_data)
                url_post = UrlShortView_asAdmin().post(
                    request=request_tmp,
                    word=Constant.ID,
                    pk=Constant.BLANK_STR,
                )
                url_post = deepcopy(url_post.data)
                url_id = url_post[Constant.DATA][0]["id"]
                if url_post[Constant.STATUS]:
                    try:
                        rev_url = reverse(
                            viewname=VNAME_URL,
                            kwargs={
                                "word": "key",
                                "pk": f'{url_post[Constant.DATA][0]["key"]}',
                            },
                        )
                    except Exception as e:
                        raise Exception("URL post failed")
                    else:
                        url_txt = f"\nLINK : {rev_url}"
        except Exception as e:
            print(f"ERROR : {str(e)}")
        return (url_id, url_txt)

    def __update_notification(
        self, request, notification_id: int, body_ext: str
    ) -> bool:
        request_tmp = request
        stat = True
        try:
            notif_get = NotificationView_asAdmin().get(
                request=request_tmp, word="id", pk=f"{notification_id}"
            )
            notif_get = notif_get.data
            if notif_get[Constant.STATUS]:
                body = f'{notif_get[Constant.DATA][0]["body"]}{body_ext}'
                request_tmp.data.clear()
                request_tmp.data.update({"body": body})
                notif_put = NotificationView_asAdmin().put(
                    request=request_tmp,
                    word="id",
                    pk=f"{notification_id}",
                )
                notif_put = deepcopy(notif_put.data)
                if not notif_put[Constant.STATUS]:
                    raise Exception("Notificaiton update failed")
            else:
                raise Exception("Notificaiton read failed")
        except Exception as e:
            print(f"ERROR : {str(e)}")
            stat = False
        return stat

    def __trigger(
        self, request, notification_id: int, mailer_id: int, telegram_id: int
    ) -> None:
        request_tmp = request
        if mailer_id is not None:
            try:
                BatchJob(
                    tname=THREAD_M,
                    mailer=True,
                    api=request_tmp.user.id,
                    status=Constant.PARTIAL,
                    obj_id=(notification_id, mailer_id),
                ).start()
            except Exception as e:
                print(f"ERROR : {str(e)}")
        if telegram_id is not None:
            try:
                BatchJob(
                    tname=THREAD_T,
                    mailer=False,
                    status=Constant.PARTIAL,
                    api=request_tmp.user.id,
                    obj_id=(notification_id, telegram_id),
                ).start()
            except Exception as e:
                print(f"ERROR : {str(e)}")
        return

    def __delete_notification(self, request, notificaiton_id: int) -> None:
        request_tmp = request
        request_tmp.data.clear()
        notif_del = NotificationView_asAdmin().delete(
            request=request_tmp,
            word="id",
            pk=f"{notificaiton_id}",
        )
        return

    def __delete_urlShort(self, request, url_id: int) -> None:
        request_tmp = request
        request_tmp.data.clear()
        url_del = UrlShortView_asAdmin().delete(
            request=request_tmp,
            word="id",
            pk=f"{url_id}",
        )
        return

    def _send_notification(self, request) -> bool:
        request_tmp = request
        return_stat = True
        try:
            api_ref = Api.objects.filter(
                sys=Constant.SETTINGS_SYSTEM,
                direction=Constant.SELF,
            )
            if len(api_ref) == 0:
                raise Exception("API Self dock not found")
            else:
                api_ref = api_ref[0]
            request_tmp.user = api_ref
            notif_id, mailer_id, tg_id = self.__post_notification(request=request_tmp)
            if notif_id is not None:
                request_id = self.data_returned[Constant.DATA][0]["id"]
                url_id, url_txt = self.__post_urlShort(
                    request=request_tmp,
                    viewname=VNAME_API,
                    request_id=request_id,
                )
                body_ext = f"{url_txt}\n{BODY_FOOTER}"
                update_bool = self.__update_notification(
                    request=request_tmp,
                    notification_id=notif_id,
                    body_ext=body_ext,
                )
                if not update_bool:
                    if url_id is not None:
                        self.__delete_urlShort(request=request_tmp, url_id=url_id)
                    self.__delete_notification(
                        request=request_tmp, notificaiton_id=notif_id
                    )
                    raise Exception("Notificaiton post failed")
                else:
                    self.__trigger(
                        request=request_tmp,
                        notification_id=notif_id,
                        mailer_id=mailer_id,
                        telegram_id=tg_id,
                    )
            else:
                raise Exception("Notificaiton post failed")
        except Exception as e:
            print(f"ERROR : {str(e)}")
            return_stat = False
        return return_stat

    def post(self, request, word: str, pk: str):
        self.__init__(query1=word, query2=pk)
        self.__create_specific(data=request.data)
        if self.data_returned[Constant.STATUS]:
            try:
                self._send_notification(request=request)
            except Exception as e:
                pass
        return Response(data=self.data_returned, status=self.status_returned)

    # =============================================================
    def __read_specific(self) -> None:
        try:
            api_ref = Api.objects.get(sys=Constant.SETTINGS_SYSTEM, id=int(self.query2))
        except Api.DoesNotExist:
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
            api_ser = Api_Serializer(api_ref, many=False).data
            self.data_returned[Constant.STATUS] = True
            self.data_returned[Constant.DATA].append(api_ser)
            self.status_returned = status.HTTP_200_OK
        return

    def __read_all(self) -> None:
        try:
            api_ref = Api.objects.all().order_by("id")
            if len(api_ref) == 0:
                raise Api.DoesNotExist
        except Api.DoesNotExist:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.NO_CONTENT
            self.status_returned = status.HTTP_204_NO_CONTENT
        else:
            api_ser = Api_Serializer(api_ref, many=True).data
            self.data_returned[Constant.STATUS] = True
            self.data_returned[Constant.DATA] = api_ser
            self.status_returned = status.HTTP_200_OK
        return

    def __read_search(self) -> None:
        try:
            try:
                api_ref = eval(
                    f'Api.objects.filter({self._create_query()}).order_by("id")'
                )
            except NameError:
                self.data_returned[Constant.STATUS] = False
                self.data_returned[Constant.MESSAGE] = Constant.INVALID_SPARAMS
                self.status_returned = status.HTTP_400_BAD_REQUEST
            except FieldError:
                try:
                    api_ref = eval(
                        f'Api.objects.filter({self._create_query(flag=False)}).order_by("id")'
                    )
                except NameError:
                    self.data_returned[Constant.STATUS] = False
                    self.data_returned[Constant.MESSAGE] = Constant.INVALID_SPARAMS
                    self.status_returned = status.HTTP_400_BAD_REQUEST
            if len(api_ref) == 0:
                raise Api.DoesNotExist
        except Api.DoesNotExist:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.NO_CONTENT
            self.status_returned = status.HTTP_204_NO_CONTENT
        else:
            api_ser = Api_Serializer(api_ref, many=True).data
            self.data_returned[Constant.STATUS] = True
            self.data_returned[Constant.DATA] = api_ser
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
            api_ref = Api.objects.get(sys=Constant.SETTINGS_SYSTEM, id=int(self.query2))
        except Api.DoesNotExist:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.INVALID_SPARAMS
            self.status_returned = status.HTTP_404_NOT_FOUND
        except ValueError:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.INVALID_SPARAMS
            self.status_returned = status.HTTP_404_NOT_FOUND
        else:
            api_ser = Api_Serializer(instance=api_ref, data=data, partial=True)
            if api_ser.is_valid():
                try:
                    api_ser.save()
                except Exception as e:
                    self.data_returned[Constant.STATUS] = False
                    self.data_returned[Constant.MESSAGE] = str(e)
                    self.status_returned = status.HTTP_406_NOT_ACCEPTABLE
                else:
                    api_ser = api_ser.data
                    self.data_returned[Constant.STATUS] = True
                    self.data_returned[Constant.DATA].append(api_ser)
                    self.status_returned = status.HTTP_201_CREATED
            else:
                self.data_returned[Constant.STATUS] = False
                self.data_returned[Constant.MESSAGE] = api_ser.errors
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
            api_ref = Api.objects.get(sys=Constant.SETTINGS_SYSTEM, id=int(self.query2))
        except Api.DoesNotExist:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.INVALID_SPARAMS
            self.status_returned = status.HTTP_404_NOT_FOUND
        except ValueError:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.INVALID_SPARAMS
            self.status_returned = status.HTTP_404_NOT_FOUND
        else:
            api_ser = Api_Serializer(api_ref, many=False).data
            api_ref.delete()
            self.data_returned[Constant.STATUS] = True
            self.data_returned[Constant.DATA].append(api_ser)
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
