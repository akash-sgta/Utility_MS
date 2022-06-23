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

# --------------------------------------------------

from utilities.models import UrlShort
from utilities.serializers import UrlShort_Serializer
from utilities.util.constant import Constant
from utility.views.authenticator import Authenticator


# =========================================================================================
#                                       CONSTANT
# =========================================================================================

# =========================================================================================
#                                       CODE
# =========================================================================================
class UrlShortView(APIView):
    authentication_classes = [Authenticator]
    renderer_classes = [JSONRenderer]

    def __init__(self, query1=None, query2=None):
        super(UrlShortView, self).__init__()
        self.DB_KEYS = (
            "id",
            "key",
            "url",
        )
        self.SR_KEYS = (
            "id",
            "key",
            "search",
        )
        self.data_returned = deepcopy(Constant.RETURN_JSON)
        self.status_returned = status.HTTP_400_BAD_REQUEST
        self.query1 = query1.lower() if query1 not in Constant.NULL else None
        if self.query1 == self.SR_KEYS[2]:  # search
            self.query2 = (
                query2.lower() if query2 not in Constant.NULL else None
            )
        else:
            self.query2 = query2 if query2 not in Constant.NULL else None
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
                        query += f"{word[i][0]}{Constant.EQUAL2}'{word[i][1]}'{Constant.COMA}"
        return query


class UrlShortView_asUser(UrlShortView):
    permission_classes = []

    def __init__(self, query1=None, query2=None):
        super(UrlShortView_asUser, self).__init__(
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
    def _read_specific(self) -> None:
        try:
            if self.query1 == self.SR_KEYS[0]:  # id
                urlShort_ref = UrlShort.objects.get(
                    sys=Constant.SETTINGS_SYSTEM, id=int(self.query2)
                )
            elif self.query1 == self.SR_KEYS[1]:  # key
                urlShort_ref = UrlShort.objects.get(
                    sys=Constant.SETTINGS_SYSTEM, key=self.query2
                )
            else:
                raise UrlShort.DoesNotExist
        except UrlShort.DoesNotExist as e:
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
            urlShort_ser = UrlShort_Serializer(urlShort_ref, many=False).data
            self.data_returned[Constant.STATUS] = True
            # self.data_returned[Constant.DATA].append(urlShort_ser)
            self.data_returned[Constant.DATA].append(urlShort_ser["url"])
            self.status_returned = status.HTTP_302_FOUND
        return

    def get(self, request, word: str, pk: str):
        self.__init__(query1=word, query2=pk)
        if self.query1 not in self.SR_KEYS:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.INVALID_URL
            self.status_returned = status.HTTP_404_NOT_FOUND
        else:
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


class UrlShortView_asAdmin(UrlShortView_asUser):
    permission_classes = []

    def __init__(self, query1=None, query2=None):
        super(UrlShortView_asAdmin, self).__init__(
            query1=query1, query2=query2
        )

    # =============================================================
    def __create_specific(self, data: dict) -> None:
        urlShort_ser = UrlShort_Serializer(data=data)
        if urlShort_ser.is_valid():
            try:
                urlShort_ser.save()
            except Exception as e:
                self.data_returned[Constant.STATUS] = False
                self.data_returned[Constant.MESSAGE] = str(e)
                self.status_returned = status.HTTP_406_NOT_ACCEPTABLE
            else:
                urlShort_ser = urlShort_ser.data
                self.data_returned[Constant.STATUS] = True
                self.data_returned[Constant.DATA].append(urlShort_ser)
                self.status_returned = status.HTTP_201_CREATED
        else:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = urlShort_ser.errors
            self.status_returned = status.HTTP_406_NOT_ACCEPTABLE
        return

    def post(self, request, word: str, pk: str):
        self.__init__(query1=word, query2=pk)
        self.__create_specific(data=request.data)
        return Response(data=self.data_returned, status=self.status_returned)

    # =============================================================
    def __read_all(self) -> None:
        try:
            urlShort_ref = UrlShort.objects.all().order_by("id")
            if len(urlShort_ref) == 0:
                raise UrlShort.DoesNotExist
        except UrlShort.DoesNotExist:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.NO_CONTENT
            self.status_returned = status.HTTP_204_NO_CONTENT
        else:
            urlShort_ser = UrlShort_Serializer(urlShort_ref, many=True).data
            self.data_returned[Constant.STATUS] = True
            self.data_returned[Constant.DATA] = urlShort_ser
            self.status_returned = status.HTTP_200_OK
        return

    def __read_search(self) -> None:
        try:
            try:
                urlShort_ref = eval(
                    f'UrlShort.objects.filter({self._create_query()}).order_by("id")'
                )
            except NameError:
                self.data_returned[Constant.STATUS] = False
                self.data_returned[
                    Constant.MESSAGE
                ] = Constant.INVALID_SPARAMS
                self.status_returned = status.HTTP_400_BAD_REQUEST
            except FieldError:
                try:
                    urlShort_ref = eval(
                        f'UrlShort.objects.filter({self._create_query(flag=False)}).order_by("id")'
                    )
                except NameError:
                    self.data_returned[Constant.STATUS] = False
                    self.data_returned[
                        Constant.MESSAGE
                    ] = Constant.INVALID_SPARAMS
                    self.status_returned = status.HTTP_400_BAD_REQUEST
            if len(urlShort_ref) == 0:
                raise UrlShort.DoesNotExist
        except UrlShort.DoesNotExist:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.NO_CONTENT
            self.status_returned = status.HTTP_204_NO_CONTENT
        else:
            urlShort_ser = UrlShort_Serializer(urlShort_ref, many=True).data
            self.data_returned[Constant.STATUS] = True
            self.data_returned[Constant.DATA] = urlShort_ser
            self.status_returned = status.HTTP_200_OK
        return

    def get(self, request, word: str, pk: str):
        self.__init__(query1=word, query2=pk)
        flag = True
        if self.query1 in self.SR_KEYS:
            if self.query1 in self.SR_KEYS[0:2]:  # id
                if self.query2 in Constant.NULL:
                    self.__read_all()
                else:
                    self._read_specific()
            elif self.query1 == self.SR_KEYS[2]:  # search
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
            urlShort_ref = UrlShort.objects.get(
                sys=Constant.SETTINGS_SYSTEM, id=int(self.query2)
            )
        except UrlShort.DoesNotExist:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.INVALID_SPARAMS
            self.status_returned = status.HTTP_404_NOT_FOUND
        except ValueError:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.INVALID_SPARAMS
            self.status_returned = status.HTTP_404_NOT_FOUND
        else:
            urlShort_ser = UrlShort_Serializer(
                instance=urlShort_ref, data=data, partial=True
            )
            if urlShort_ser.is_valid():
                try:
                    urlShort_ser.save()
                except Exception as e:
                    self.data_returned[Constant.STATUS] = False
                    self.data_returned[Constant.MESSAGE] = str(e)
                    self.status_returned = status.HTTP_406_NOT_ACCEPTABLE
                else:
                    urlShort_ser = urlShort_ser.data
                    self.data_returned[Constant.STATUS] = True
                    self.data_returned[Constant.DATA].append(urlShort_ser)
                    self.status_returned = status.HTTP_201_CREATED
            else:
                self.data_returned[Constant.STATUS] = False
                self.data_returned[Constant.MESSAGE] = urlShort_ser.errors
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
            urlShort_ref = UrlShort.objects.get(
                sys=Constant.SETTINGS_SYSTEM, id=int(self.query2)
            )
        except UrlShort.DoesNotExist:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.INVALID_SPARAMS
            self.status_returned = status.HTTP_404_NOT_FOUND
        except ValueError:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.INVALID_SPARAMS
            self.status_returned = status.HTTP_404_NOT_FOUND
        else:
            urlShort_ser = UrlShort_Serializer(urlShort_ref, many=False).data
            urlShort_ref.delete()
            self.data_returned[Constant.STATUS] = True
            self.data_returned[Constant.DATA].append(urlShort_ser)
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
