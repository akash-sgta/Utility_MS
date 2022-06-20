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

from utilities.models import Mailer
from utilities.serializers import Mailer_Serializer
from utilities.views.utility.constant import Constant
from utilities.views.utility.batchJob import BatchJob


# =========================================================================================
#                                       CONSTANT
# =========================================================================================

# =========================================================================================
#                                       CODE
# =========================================================================================
class MailerView(APIView):
    renderer_classes = [JSONRenderer]
    authentication_classes = []

    def __init__(self, query1=None, query2=None):
        super(MailerView, self).__init__()
        self.DB_KEYS = (
            "id",
            "subject",
            "sender",
        )
        self.SR_KEYS = (
            "id",
            "search",
            "trigger",
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


class MailerView_asUser(MailerView):
    permission_classes = []

    def __init__(self, query1=None, query2=None):
        super(MailerView_asUser, self).__init__(query1=query1, query2=query2)

    # =============================================================
    def __create_specific(self, data: dict) -> None:
        mailer_ser = Mailer_Serializer(data=data)
        if mailer_ser.is_valid():
            try:
                mailer_ser.save()
            except Exception as e:
                self.data_returned[Constant.STATUS] = False
                self.data_returned[Constant.MESSAGE] = str(e)
                self.status_returned = status.HTTP_406_NOT_ACCEPTABLE
            else:
                mailer_ser = mailer_ser.data
                self.data_returned[Constant.STATUS] = True
                self.data_returned[Constant.DATA].append(mailer_ser)
                self.status_returned = status.HTTP_201_CREATED
        else:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = mailer_ser.errors
            self.status_returned = status.HTTP_406_NOT_ACCEPTABLE
        return

    def post(self, request, word: str, pk: str, internal: bool = False):
        self.__init__(query1=word, query2=pk)
        if not internal:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.METHOD_NOT_ALLOWED
            self.status_returned = status.HTTP_405_METHOD_NOT_ALLOWED
        else:
            self.__create_specific(data=request.data)
        return Response(data=self.data_returned, status=self.status_returned)

    # =============================================================
    def _read_specific(self) -> None:
        try:
            mailer_ref = Mailer.objects.get(
                sys=Constant.SETTINGS_SYSTEM, id=int(self.query2)
            )
        except Mailer.DoesNotExist:
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
            mailer_ser = Mailer_Serializer(mailer_ref, many=False).data
            self.data_returned[Constant.STATUS] = True
            self.data_returned[Constant.DATA].append(mailer_ser)
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


class MailerView_asAdmin(MailerView_asUser):
    permission_classes = []

    def __init__(self, query1=None, query2=None):
        super(MailerView_asAdmin, self).__init__(query1=query1, query2=query2)

    # =============================================================
    def post(self, request, word: str, pk: str):
        return super(MailerView_asAdmin, self).post(request=request, word=word, pk=pk)

    # =============================================================
    def __read_all(self) -> None:
        try:
            mailer_ref = Mailer.objects.all().order_by("id")
            if len(mailer_ref) == 0:
                raise Mailer.DoesNotExist
        except Mailer.DoesNotExist:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.NO_CONTENT
            self.status_returned = status.HTTP_204_NO_CONTENT
        else:
            mailer_ser = Mailer_Serializer(mailer_ref, many=True).data
            self.data_returned[Constant.STATUS] = True
            self.data_returned[Constant.DATA] = mailer_ser
            self.status_returned = status.HTTP_200_OK
        return

    def __read_search(self) -> None:
        try:
            mailer_ref = eval(
                f'Mailer.objects.filter({self._create_query()}).order_by("id")'
            )
            if len(mailer_ref) == 0:
                raise Mailer.DoesNotExist
        except Mailer.DoesNotExist:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.NO_CONTENT
            self.status_returned = status.HTTP_204_NO_CONTENT
        except NameError:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.INVALID_SPARAMS
            self.status_returned = status.HTTP_400_BAD_REQUEST
        else:
            mailer_ser = Mailer_Serializer(mailer_ref, many=True).data
            self.data_returned[Constant.STATUS] = True
            self.data_returned[Constant.DATA] = mailer_ser
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
                    self._read_specific()
            elif self.query1 == self.SR_KEYS[1]:  # search
                if self.query2 in Constant.NULL:
                    flag = False
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
                    batch_thread = BatchJob(mailer=True, api=1, status=_status)
                    batch_thread.start()
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
            mailer_ref = Mailer.objects.get(
                sys=Constant.SETTINGS_SYSTEM, id=int(self.query2)
            )
        except Mailer.DoesNotExist:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.INVALID_SPARAMS
            self.status_returned = status.HTTP_404_NOT_FOUND
        except ValueError:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.INVALID_SPARAMS
            self.status_returned = status.HTTP_404_NOT_FOUND
        else:
            mailer_ser = Mailer_Serializer(instance=mailer_ref, data=data, partial=True)
            if mailer_ser.is_valid():
                try:
                    mailer_ser.save()
                except Exception as e:
                    self.data_returned[Constant.STATUS] = False
                    self.data_returned[Constant.MESSAGE] = str(e)
                    self.status_returned = status.HTTP_406_NOT_ACCEPTABLE
                else:
                    mailer_ser = mailer_ser.data
                    self.data_returned[Constant.STATUS] = True
                    self.data_returned[Constant.DATA].append(mailer_ser)
                    self.status_returned = status.HTTP_201_CREATED
            else:
                self.data_returned[Constant.STATUS] = False
                self.data_returned[Constant.MESSAGE] = mailer_ser.errors
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
            mailer_ref = Mailer.objects.get(
                sys=Constant.SETTINGS_SYSTEM, id=int(self.query2)
            )
        except Mailer.DoesNotExist:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.INVALID_SPARAMS
            self.status_returned = status.HTTP_404_NOT_FOUND
        except ValueError:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.INVALID_SPARAMS
            self.status_returned = status.HTTP_404_NOT_FOUND
        else:
            mailer_ser = Mailer_Serializer(mailer_ref, many=False).data
            mailer_ref.delete()
            self.data_returned[Constant.STATUS] = True
            self.data_returned[Constant.DATA].append(mailer_ser)
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
