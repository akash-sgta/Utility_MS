# --------------------------------------------------------------------------
# DOCUMENTATION
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# LIRARY
# --------------------------------------------------------------------------
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from utility.extra.pool import b64ToDict

from access.models import Identity
from access.serializers import Identity_Serializer


# --------------------------------------------------------------------------
# CONSTANTS
# --------------------------------------------------------------------------
from utility.extra.constant import TOKEN_HEADER, SPACE_1, AUTHORIZATION, INVALID_API_KEY, ERROR_CRUD_GEN

ERROR = "ERROR"
# --------------------------------------------------------------------------
# CODE
# --------------------------------------------------------------------------
class Authentication(BaseAuthentication):
    def __verify(self, token):
        data = b64ToDict(token)
        if data is None:
            return False, None
        else:
            identity_ser = Identity_Serializer(data=data)
            if identity_ser.is_valid():
                identity_ser = identity_ser.initial_data
                try:
                    identity_ref = Identity.objects.get(
                        name=identity_ser["name"], email=identity_ser["email"].upper(), key=identity_ser["key"]
                    )
                    return True, identity_ref
                except Identity.DoesNotExist:
                    return False, None
            else:
                return False, None

    def authenticate(self, request):
        headers = request.headers
        if AUTHORIZATION not in headers.keys():
            raise AuthenticationFailed(
                detail="{} Token".format("/".join(TOKEN_HEADER)), code=status.HTTP_403_FORBIDDEN
            )
        else:
            access_token = headers[AUTHORIZATION].split(SPACE_1)
            if len(access_token) != 2 or access_token[0].upper() not in TOKEN_HEADER:
                raise AuthenticationFailed(detail="{}".format("/".join(TOKEN_HEADER)), code=status.HTTP_403_FORBIDDEN)
            else:
                has_access = self.__verify(token=access_token[1])
                if has_access[0]:
                    return has_access[1], None
                else:
                    error = ERROR_CRUD_GEN
                    error[ERROR] = "Not Authorized"
                    raise AuthenticationFailed(detail=error, code=status.HTTP_401_UNAUTHORIZED)
