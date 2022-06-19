# =========================================================================================
#                                       DOCUMENTATION
# =========================================================================================


# =========================================================================================
#                                       LIBRARY
# =========================================================================================
from copy import deepcopy
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from datetime import datetime

# --------------------------------------------
from utilities.views.utility.utility import Utility
from utilities.views.utility.constant import Constant


# =========================================================================================
#                                       CONSTANT
# =========================================================================================
POST = "POST"
ENC = "ENC"
JSON_2_STR = 1
STR_2_JSON = 2
# =========================================================================================
#                                       CODE
# =========================================================================================


def encToken(token_dict: dict, enc: bool = False) -> tuple:
    """
    Encrypt Json Token
    ------------------
    """
    ret_data = deepcopy(Constant.RETURN_JSON)
    details = Constant.BLANK_STR
    try:
        Constant.DICT_TOKEN_ROOT.validate(token_dict)
        Constant.TOKEN_LEAF.validate(token_dict[Constant.API])
        Constant.TOKEN_LEAF.validate(token_dict[Constant.USER])
        token_str = Utility.packToken(
            api_ser=token_dict[Constant.API],
            user_ser=token_dict[Constant.USER],
            enc=enc,
        )
    except Exception as e:
        return e
    else:
        ret_data[Constant.STATUS] = True
        ret_data[Constant.DATA] = token_str
        ret_status = status.HTTP_200_OK
    return (ret_data, ret_status)


def decToken(token_str: dict, enc: bool = False) -> dict:
    """
    Decrypt Json Token
    ------------------
    """
    ret_data = deepcopy(Constant.RETURN_JSON)
    details = Constant.BLANK_STR
    try:
        token_str = token_str[Constant.TOKEN]
        token_dict = Utility.unpackToken(
            data=token_str,
            enc=enc,
        )
    except Exception as e:
        return e
    else:
        ret_data[Constant.STATUS] = True
        ret_data[Constant.DATA] = token_dict
        ret_status = status.HTTP_200_OK
    return (ret_data, ret_status)


@api_view([POST])
def token(request, word: str, pk: int):
    ret_data = deepcopy(Constant.RETURN_JSON)
    ret_data[Constant.STATUS] = False
    ret_status = status.HTTP_400_BAD_REQUEST
    try:
        if int(pk) == JSON_2_STR:
            if word.upper() == ENC:
                ret_data, ret_status = encToken(
                    token_dict=request.data, enc=True
                )
            else:
                ret_data, ret_status = encToken(
                    token_dict=request.data, enc=False
                )
        else:
            if word.upper() == ENC:
                ret_data, ret_status = decToken(
                    token_str=request.data, enc=True
                )
            else:
                ret_data, ret_status = decToken(
                    token_str=request.data, enc=False
                )
    except Exception as e:
        ret_data[Constant.STATUS] = False
        ret_data[Constant.MESSAGE] = str(e)
        ret_status = status.HTTP_400_BAD_REQUEST
    return JsonResponse(data=ret_data, status=ret_status)
