# =========================================================================================
#                                       DOCUMENTATION
# =========================================================================================

# =========================================================================================
#                                       LIBRARY
# =========================================================================================
from copy import deepcopy
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

# --------------------------------------------------

from utilities.views.utility.utility import Utility
from utilities.views.utility.constant import Constant
from api.models import Api

# =========================================================================================
#                                       CONSTANT
# =========================================================================================


# =========================================================================================
#                                       CODE
# =========================================================================================
class Authenticator(BaseAuthentication):
    def __init__(self):
        super(Authenticator, self).__init__()

    def __extract_token(self, headers) -> str:
        if Constant.AUTHORIZATION not in headers.keys():
            raise Exception(f"{Constant.AUTHORIZATION} : Header Missing")
        else:
            access_token = headers[Constant.AUTHORIZATION].split(
                Constant.SPACE
            )
            if len(access_token) != 2:
                raise Exception(
                    f"{Constant.BEARER} Token:string / {Constant.JWT} Token:string"
                )
            else:
                return access_token[1]

    def __unpack_token(self, token: str) -> dict:
        token_dict = dict()
        try:
            token_dict = Utility.unpackToken(data=token, enc=True)
        except Exception as e:
            print(str(e))
            raise Exception(Constant.INVALID_TOKEN)
        return token_dict

    def __verify_user(self, token: dict) -> bool:
        """
        Microservice call to IAM
        ------------------------
        """
        try:
            pass
        except Exception as e:
            return False
        else:
            return True

    def __verify_api(self, token: dict) -> Api:
        try:
            token = token[Constant.API]
            api_ref = Api.objects.get(identity=int(token[Constant.ID]))
        except Api.DoesNotExist as e:
            raise Exception(f"{Constant.INVALID_CRED}")
        else:
            try:
                assert api_ref.key == token[Constant.JWT]
            except AssertionError as e:
                raise Exception(f"{Constant.INVALID_CRED}")
            else:
                return api_ref

    def authenticate(self, request):
        try:
            details = Constant.BLANK_STR
            token_str = self.__extract_token(headers=request.headers)
            token_dict = self.__unpack_token(token=token_str)
            api = self.__verify_api(token=token_dict)
            # user = self.__verify_user(token=token_dict)
        except Exception as e:
            details = str(e)
        finally:
            if details != Constant.BLANK_STR:
                raise AuthenticationFailed(detail=details)
            else:
                return api, None
