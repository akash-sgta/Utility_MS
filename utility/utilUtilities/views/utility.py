# =========================================================================================
#                                       DOCUMENTATION
# =========================================================================================

# =========================================================================================
#                                       LIBRARY
# =========================================================================================
import re

from django.core.validators import RegexValidator
from django.conf import settings
import hashlib
import string
import json
import base64
import random
import math
from datetime import datetime, timedelta

from authUtilities.models import Country


class Utility(object):
    # ==========================================================================
    #                                       CONSTANT
    # ==========================================================================
    TZ = ("GMT", "+ 05:30")
    MAINTENANCE = "UNDER MAINTENANCE"
    BLANK = ""
    SPACE = " "
    COLON = ":"
    COMA = ","
    EQUAL = "EQ"
    EQUAL2 = "="
    EQUAL_CONTAINS = "__icontains="

    UTF8 = "utf-8"
    REDACTED = "********"
    CHECK = "CHECK"
    CREATE = "POST"
    READ = "GET"
    UPDATE = "EDIT"
    DELETE = "DELETE"
    ADMIN = "ADMIN"
    NULL = (None, "", 0)
    FNAME = "fname"
    LNAME = "lname"
    EMAIL = "email"
    PHONE = "phone"
    SEARCH = "SEARCH"
    TRUE = "TRUE"
    REFRESH = "REFRESH"
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    S_AUTH = "AUTH"
    SERVER_NAME = {
        S_AUTH: "authenticator",
    }
    # --------------------------------------------------------------------------
    DOC_TYPE = (
        (0, "UNIDENTIFIED"),
        (1, "IMAGE"),
        (2, "EXCEL"),
        (3, "PDF"),
        (4, "WORD"),
        (5, "OTHERS"),
    )
    IMG_SIZE = {"L": "1280x1024", "M": "1024x786", "S": "320x240"}
    # --------------------------------------------------------------------------
    UNAUTHORISED_ACTION = "UNAUTHORIZED ACTION"
    UNAUTHORISED_USER = "UNAUTHORIZED USER"
    UNDER_CONSTRUCTION = "UNDER CONSTRUCTION"
    ERROR_RT_TIMEOUT = {"ERROR": "REFRESH TOKEN TIMEOUT"}
    ERROR_AT_TIMEOUT = {"ERROR": "ACCESS TOKEN TIMEOUT"}
    ERROR_PD_REQUIRED = {"ERROR": "PASSWORD REQUIRED"}
    # --------------------------------------------------------------------------
    INVALID_API = "INVALID API"
    INVALID_IDENTITY = "INVALID IDENTITY"
    # --------------------------------------------------------------------------
    REFRESH_TIMEOUT = "REFRESH TOKEN TIMEOUT"
    REFRESH_TOKEN = "url goes here"
    # --------------------------------------------------------------------------
    INVALID_SKEY = "INVALID SEARCH KEY"
    INVALID_PASSWORD = {"ERROR": "INVALID PASSWORD"}
    INVALID_DEVICE = {"ERROR": "USER DEVICE MISMATCH"}
    INVALID_USER_ID = {"ERROR": "INVALID USER ID"}
    INVALID_TOKEN_ENC = {"ERROR": "INVALID TOKEN ENCODING"}
    INVALID_AT = {"ERROR": "INVALID ACCESS TOKEN"}
    ERROR_ACC_INACTIVE = {"ERROR": "ACCOUNT INACTIVE"}
    ERROR_BACKEND = {"ERROR": "BACKEND ERROR"}
    CONFLICT_USERNAME = {"ERROR": "USERNAME EXISTS"}
    ERROR_AT_GEN = {"ERROR": "ACCESS TOKEN NOT GENERATED"}
    # --------------------------------------------------------------------------
    KEYS = ["id", "jwt"]
    TOKEN_HEADER = ["BEARER", "JWT"]
    AUTHORIZATION = "Authorization"
    INVALID_API_KEY = {"ERROR": "API Key is invalid"}
    # --------------------------------------------------------------------------
    INVALID_ID = {"ERROR": "INVALID ID"}
    INVALID_FORMATTING = "INVALID FORMATTING"
    # --------------------------------------------------------------------------
    COUNTRY = "COUNTRY"
    STATE = "STATE"
    CITY = "CITY"
    # --------------------------------------------------------------------------
    ERROR_CRUD_C = "CREATE ERROR"
    ERROR_CRUD_R = "READ ERROR"
    ERROR_CRUD_U = "UPDATE ERROR"
    ERROR_CRUD_D = "DELETE ERROR"
    # --------------------------------------------------------------------------
    U_CITY_NAME_CONF = "u_ city with this name already exists."
    U_COUNTRY_NAME_CONF = "u_ country with this name code already exists."
    U_COUNTRY_ISD_CONF = "u_ country with this isd already exists."
    U_COUNTRY_ISO_CONF = "u_ country with this iso already exists."
    U_STATE_NAME_CONF = "u_ state with this name already exists."
    # --------------------------------------------------------------------------
    SUCCESS_CRUD_C = {"SUCCESS": "[CRUD] CREATE SUCCESSFUL"}
    SUCCESS_CRUD_R = {"SUCCESS": "[CRUD] READ SUCCESSFUL"}
    SUCCESS_CRUD_U = {"SUCCESS": "[CRUD] UPDATE SUCCESSFUL"}
    SUCCESS_CRUD_D = {"SUCCESS": "[CRUD] DELETE SUCCESSFUL"}
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------

    # ==============================================================================
    #                                       CODE
    # ==============================================================================
    @staticmethod
    def unpackPhoneNumber(phone_no: str):
        if phone_no not in Utility.NULL:
            phone = re.findall(pattern=Utility.PHONE_REGEX_SIMPLE, string=phone_no)
            try:
                country_ref = Country.objects.get(isd=phone[0])
                _return = (country_ref.id, phone[-1])
            except Country.DoesNotExist:
                _return = (None, phone[-1])
        else:
            _return = (None, None)
        return _return

    @staticmethod
    def packToken(token_ser, usage: str):
        token = dict()
        if usage == Utility.SIGNIN:
            token[Utility.SIGNIN] = token_ser.copy()
        del token_ser["createdOn"]
        del token_ser["access_end"]
        del token_ser["refresh_token"]
        del token_ser["refresh_end"]
        token[Utility.CHECK] = Utility.dictToB64(token_ser)
        return token

    @staticmethod
    def unpackToken(data: str):
        return Utility.b64ToDict(data)

    @staticmethod
    def log(exp: int, base: int):
        if exp == 0:
            return False

        return math.log10(exp) / math.log10(base)

    @staticmethod
    def isPowerOfTwo(n: int):
        if n == 1:
            _return = False
        else:
            _return = math.ceil(Utility.log(n, 2)) == math.floor(Utility.log(n, 2))
        return _return

    @staticmethod
    def addToHexadecimal(operand1="0", operand2=1):
        return hex(int(("0x" + operand1.lower()), 16) + operand2)[2:]

    @staticmethod
    def stringToHashHex(*args: tuple):
        if len(args) == 0:
            raise KeyError("No arguments passed")
        else:
            data = settings.SECRET_KEY.join(args)
            return "md5_" + hashlib.md5(data.encode()).hexdigest()

    @staticmethod
    def randomGenerator(length=225, only_num=False, no_symbol=False):
        choices = list()
        choices.extend(list(string.ascii_lowercase + string.ascii_uppercase))
        if not only_num:
            choices.extend(list(string.digits))
        if not no_symbol:
            choices.extend(list(string.punctuation))
        _return = "".join([random.choice(choices) for _ in range(length)])

        return _return

    @staticmethod
    def datetimeToEpochMs(
        dt: datetime.now, add_hours=0, add_minutes=0, add_seconds=0, add_days=0, add_months=0, add_years=0
    ):
        delta = list()
        if add_hours > 0:
            delta.append(timedelta(hours=add_hours))
        if add_minutes > 0:
            delta.append(timedelta(minutes=add_minutes))
        if add_seconds > 0:
            delta.append(timedelta(seconds=add_seconds))
        if add_days > 0:
            delta.append(timedelta(days=add_days))
        if add_months > 0:
            delta.append(timedelta(days=add_months * 30))
        if add_years > 0:
            delta.append(timedelta(days=add_years * 365))

        ms_from_epoch = dt
        for item in delta:
            ms_from_epoch += item
        ms_from_epoch = int(ms_from_epoch.timestamp() * 1000)

        return ms_from_epoch

    @staticmethod
    def epochMsToDatetime(epoch: int):
        return datetime.fromtimestamp(epoch // 1000)

    @staticmethod
    def datetimeToStr(data: datetime.now):
        return data.strftime("%m/%d/%Y, %H:%M:%S")

    @staticmethod
    def msToStr(data: int):
        _return = Utility.epochMsToDatetime(data)
        return _return.strftime("%m/%d/%Y, %H:%M:%S")

    @staticmethod
    def dictToB64(data: dict):
        return base64.b64encode(json.dumps(data).encode(Utility.UTF8)).decode(Utility.UTF8)

    @staticmethod
    def b64ToDict(data: str):
        try:
            _return = json.loads(base64.b64decode(data.encode(Utility.UTF8)))
        except Exception as e:
            _return = None
        return _return
