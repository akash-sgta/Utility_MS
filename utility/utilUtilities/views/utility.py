# =========================================================================================
#                                       DOCUMENTATION
# =========================================================================================

# =========================================================================================
#                                       LIBRARY
# =========================================================================================
from django.conf import settings
import hashlib
import string
import json
import base64
import random
import math
from datetime import datetime, timedelta

# ==============================================================================
#                                       CONSTANT
# ==============================================================================
class Constant(object):
    # --------------------------------------------------
    STATUS = "STATUS"
    DATA = "DATA"
    MESSAGE = "MESSAGE"
    TIMEZONE = "TIMEZONE"
    BLANK_LIST = []
    BLANK_STR = ""
    RETURN_JSON = {STATUS: False, DATA: BLANK_LIST, MESSAGE: BLANK_STR, TIMEZONE: settings.TIME_ZONE}
    # --------------------------------------------------
    SYS = "sys"
    NULL = (None, "", 0)
    SETTINGS_SYSTEM = settings.SYSTEM
    COMA = ","
    EQUAL = "EQ"
    EQUAL2 = "="
    # --------------------------------------------------
    INVALID_SPARAMS = "INVALID SEARCH PARAMETERS"
    INVALID_URL = "INVALID URL"
    INVALID_PAYLOAD = "INVALID DATA POSTED"
    # --------------------------------------------------
    METHOD_NOT_ALLOWED = "METHOD NOT ALLOWED"
    NO_CONTENT = "NO CONTENT FOUND"
    # --------------------------------------------------


# ==============================================================================
#                                       CODE
# ==============================================================================
class Utility(object):
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
