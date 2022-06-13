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

from utilUtilities.views.utility.utility import Utility
from utilUtilities.views.utility.constant import Constant
from utilApi.models import Api

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
        token_root = Utility.unpackTokenRoot(data=token)
        if token_root in Constant.NULL:
            raise Exception(f"{Constant.INVALID_TOKEN}")
        else:
            token_user = Utility.unpackTokenLeaf(
                data=token_root[Constant.USER]
            )
            token_dict[Constant.USER] = token_user
            token_api = Utility.unpackTokenLeaf(data=token_root[Constant.API])
            if token_api in Constant.NULL:
                token_dict[Constant.API] = token_api
            else:
                raise Exception(f"{Constant.INVALID_TOKEN}")
        return token_dict

    def __verify_user(self, token: dict) -> Api:
        raise Exception(f"{Constant.INVALID_CRED}")
        # try:
        #     api_ref = Api.objects.get(
        #         identity=int(token[Constant.API][Constant.ID])
        #     )
        # except Api.DoesNotExist as e:
        #     raise Exception(f"{Constant.INVALID_CRED}")
        # else:
        #     try:
        #         assert api_ref.key != token[Constant.API][Constant.JWT]
        #     except AssertionError as e:
        #         raise Exception(f"{Constant.INVALID_CRED}")
        #     else:
        #         return api_ref

    def __verify_api(self, token: dict) -> Api:
        try:
            api_ref = Api.objects.get(
                identity=int(token[Constant.API][Constant.ID])
            )
        except Api.DoesNotExist as e:
            raise Exception(f"{Constant.INVALID_CRED}")
        else:
            try:
                assert api_ref.key != token[Constant.API][Constant.JWT]
            except AssertionError as e:
                raise Exception(f"{Constant.INVALID_CRED}")
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
        if details not in Constant.NULL:
            raise AuthenticationFailed(detail=details)
