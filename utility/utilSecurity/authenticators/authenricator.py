# =========================================================================================
#                                       DOCUMENTATION
# =========================================================================================

# =========================================================================================
#                                       LIBRARY
# =========================================================================================
from schemadict import schemadict
from json import JSONDecodeError
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status

# --------------------------------------------------

from utilUtilities.views.utility import Utility
from utilApi.models import Api

# =========================================================================================
#                                       CONSTANT
# =========================================================================================
API = "API"
USER = "USER"
schema_root = schemadict(
    {
        "API": {
            "type": str,
            "min_len": 15,
            "max_len": 255,
        },
        "USER": {
            "type": str,
            "min_len": 15,
            "max_len": 255,
        },
    }
)
ID = "ID"
TOKEN = "TOKEN"
schema_leaf = schemadict(
    {
        "ID": {
            "type": int,
            ">": 0,
        },
        "TOKEN": {
            "type": str,
            "min_len": 15,
            "max_len": 255,
        },
    }
)


# --------------------------------------------------
AUTHORIZATION = "Authorization"
BEARER = "Bearer"
JWT = "Jwt"
SPACE = " "
NULL = (None, "", 0)
# --------------------------------------------------
INVALID_TOKEN = "INVALID API TOKEN"
INVALID_CRED = "INVALID API CREDENTIALS"


# =========================================================================================
#                                       CODE
# =========================================================================================
class Authenticator(BaseAuthentication):
    def __init__(self):
        super(Authenticator, self).__init__()

    def __extract_token(self, headers) -> str:
        if AUTHORIZATION not in headers.keys():
            raise Exception(f"{AUTHORIZATION} : Header Missing")
        else:
            access_token = headers[AUTHORIZATION].split(SPACE)
            if len(access_token) != 2:
                raise Exception(f"{BEARER} Token:string / {JWT} Token:string")
            else:
                return access_token[1]

    def __unpack_token(self, token: str) -> dict:
        try:
            token_dict = Utility.b64ToDict(token)
            schema_root.validate(token_dict)
        except Exception as e:
            raise Exception(f"{INVALID_TOKEN}")
        else:
            temp = token_dict.copy()
            for key in token_dict.keys():
                try:
                    token_dict_l2 = Utility.b64ToDict(token_dict[key])
                    schema_root.validate(token_dict_l2)
                except Exception as e:
                    temp[key] = None
                else:
                    temp[key] = token_dict_l2
        return temp

    def __verify_api(self, token: dict) -> Api:
        try:
            api_ref = Api.objects.get(identity=int(token[API][ID]))
        except Api.DoesNotExist as e:
            raise Exception(f"{INVALID_CRED}")
        else:
            try:
                assert api_ref.key != token[API][TOKEN]
            except AssertionError as e:
                raise Exception(f"{INVALID_CRED}")
            else:
                return api_ref

    def authenticate(self, request):
        try:
            token_str = self.__extract_token(headers=request.headers)
        except Exception as e:
            details = str(e)
        else:
            try:
                token_dict = self.__unpack_token(token=token_str)
            except Exception as e:
                details = str(e)
            else:
                try:
                    api = self.__verify_api(token=token_dict)
                except Exception as e:
                    details = str(e)
                else:
                    return api, None
        if details not in NULL:
            raise AuthenticationFailed(detail=details)
