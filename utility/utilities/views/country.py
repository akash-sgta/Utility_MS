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

from utilities.models import Country
from utilities.serializers import Country_Serializer
from utilities.util.constant import Constant
from utility.views.authenticator import Authenticator
from utility.views.authorizer import (
    Authoriser_asUser,
    Authoriser_asAdmin,
)

# =========================================================================================
#                                       CONSTANT
# =========================================================================================

# =========================================================================================
#                                       CODE
# =========================================================================================
class CountryView(APIView):
    renderer_classes = [JSONRenderer]
    authentication_classes = [Authenticator]

    def __init__(self, query1=None, query2=None):
        super(CountryView, self).__init__()
        self.DB_KEYS = (
            "id",
            "isd",
            "iso",
            "name",
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
        """
        Create args string for filter() from the provided search query
        """
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


class CountryView_asUser(CountryView):
    permission_classes = [Authoriser_asUser]

    def __init__(self, query1=None, query2=None):
        super(CountryView_asUser, self).__init__(query1=query1, query2=query2)

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
        try:
            country_ref = Country.objects.get(
                sys=Constant.SETTINGS_SYSTEM, id=int(self.query2)
            )
        except Country.DoesNotExist:
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
            country_ser = Country_Serializer(country_ref, many=False).data
            self.data_returned[Constant.STATUS] = True
            self.data_returned[Constant.DATA].append(country_ser)
            self.status_returned = status.HTTP_200_OK
        return

    def __read_all(self) -> None:
        try:
            country_ref = Country.objects.all().order_by("id")
            if len(country_ref) == 0:
                raise Country.DoesNotExist
        except Country.DoesNotExist:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.NO_CONTENT
            self.status_returned = status.HTTP_204_NO_CONTENT
        else:
            country_ser = Country_Serializer(country_ref, many=True).data
            self.data_returned[Constant.STATUS] = True
            self.data_returned[Constant.DATA] = country_ser
            self.status_returned = status.HTTP_200_OK
        return

    def __read_search(self) -> None:
        try:
            country_ref = eval(
                f'Country.objects.filter({self._create_query()}).order_by("id")'
            )
            if len(country_ref) == 0:
                raise Country.DoesNotExist
        except Country.DoesNotExist:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.NO_CONTENT
            self.status_returned = status.HTTP_204_NO_CONTENT
        except NameError:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.INVALID_SPARAMS
            self.status_returned = status.HTTP_400_BAD_REQUEST
        else:
            country_ser = Country_Serializer(country_ref, many=True).data
            self.data_returned[Constant.STATUS] = True
            self.data_returned[Constant.DATA] = country_ser
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


class CountryView_asAdmin(CountryView_asUser):
    permission_classes = [Authoriser_asAdmin]

    def __init__(self, query1=None, query2=None):
        super(CountryView_asAdmin, self).__init__(
            query1=query1, query2=query2
        )

    # =============================================================
    def __create_specific(self, data: dict) -> None:
        country_ser = Country_Serializer(data=data)
        if country_ser.is_valid():
            try:
                country_ser.save()
            except Exception as e:
                self.data_returned[Constant.STATUS] = False
                self.data_returned[Constant.MESSAGE] = str(e)
                self.status_returned = status.HTTP_406_NOT_ACCEPTABLE
            else:
                country_ser = country_ser.data
                self.data_returned[Constant.STATUS] = True
                self.data_returned[Constant.DATA].append(country_ser)
                self.status_returned = status.HTTP_201_CREATED
        else:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = country_ser.errors
            self.status_returned = status.HTTP_406_NOT_ACCEPTABLE
        return

    def post(self, request, word: str, pk: str):
        self.__init__(query1=word, query2=pk)
        self.__create_specific(data=request.data)
        return Response(data=self.data_returned, status=self.status_returned)

    # =============================================================
    def get(self, request, word: str, pk: str):
        return super(CountryView_asAdmin, self).get(
            request=request, word=word, pk=pk
        )

    # =============================================================
    def __update_specific(self, data: dict) -> None:
        try:
            country_ref = Country.objects.get(
                sys=Constant.SETTINGS_SYSTEM, id=int(self.query2)
            )
        except Country.DoesNotExist:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.INVALID_SPARAMS
            self.status_returned = status.HTTP_404_NOT_FOUND
        except ValueError:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.INVALID_SPARAMS
            self.status_returned = status.HTTP_404_NOT_FOUND
        else:
            country_ser = Country_Serializer(
                instance=country_ref, data=data, partial=True
            )
            if country_ser.is_valid():
                try:
                    country_ser.save()
                except Exception as e:
                    self.data_returned[Constant.STATUS] = False
                    self.data_returned[Constant.MESSAGE] = str(e)
                    self.status_returned = status.HTTP_406_NOT_ACCEPTABLE
                else:
                    country_ser = country_ser.data
                    self.data_returned[Constant.STATUS] = True
                    self.data_returned[Constant.DATA].append(country_ser)
                    self.status_returned = status.HTTP_201_CREATED
            else:
                self.data_returned[Constant.STATUS] = False
                self.data_returned[Constant.MESSAGE] = country_ser.errors
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
            country_ref = Country.objects.get(
                sys=Constant.SETTINGS_SYSTEM, id=int(self.query2)
            )
        except Country.DoesNotExist:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.INVALID_SPARAMS
            self.status_returned = status.HTTP_404_NOT_FOUND
        except ValueError:
            self.data_returned[Constant.STATUS] = False
            self.data_returned[Constant.MESSAGE] = Constant.INVALID_SPARAMS
            self.status_returned = status.HTTP_404_NOT_FOUND
        else:
            country_ser = Country_Serializer(country_ref, many=False).data
            country_ref.delete()
            self.data_returned[Constant.STATUS] = True
            self.data_returned[Constant.DATA].append(country_ser)
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
