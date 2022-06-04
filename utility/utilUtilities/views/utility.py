# =========================================================================================
#                                       DOCUMENTATION
# =========================================================================================

# =========================================================================================
#                                       LIBRARY
# =========================================================================================
from django.conf import settings
from django.core.validators import RegexValidator
from hashlib import md5
import string
import json
import base64
import random
import math
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from schemadict import schemadict

# ==============================================================================
#                                       CONSTANT
# ==============================================================================
class Constant(object):
    # --------------------------------------------------
    #               PAYLOAD
    # --------------------------------------------------
    STATUS = "STATUS"
    DATA = "DATA"
    MESSAGE = "MESSAGE"
    TIMEZONE = "TIMEZONE"
    BLANK_LIST = []
    BLANK_STR = ""
    RETURN_JSON = {
        STATUS: False,
        DATA: BLANK_LIST,
        MESSAGE: BLANK_STR,
        TIMEZONE: settings.TIME_ZONE,
    }
    # --------------------------------------------------
    #               SYSTEM PARAMS
    # --------------------------------------------------
    SETTINGS_SYSTEM = settings.SYSTEM
    SETTINGS_EMAIL = settings.EMAIL
    SETTINGS_SECRET = settings.SECRET_KEY
    # --------------------------------------------------
    #               INVALID
    # --------------------------------------------------
    INVALID_SPARAMS = "INVALID SEARCH PARAMETERS"
    INVALID_URL = "INVALID URL"
    INVALID_PAYLOAD = "INVALID DATA POSTED"
    # --------------------------------------------------
    #               OTHERS
    # --------------------------------------------------
    METHOD_NOT_ALLOWED = "METHOD NOT ALLOWED"
    NO_CONTENT = "NO CONTENT FOUND"
    SYS = "sys"
    NULL = (None, "", 0)
    COMA = ","
    EQUAL = "EQ"
    EQUAL2 = "="
    MD5 = "md5_"
    UTF8 = "utf-8"
    # --------------------------------------------------
    #               VALIDATOR
    # --------------------------------------------------
    REGEX_PHONE_SIMPLE = r"\d{8,13}"
    REGEX_PHONE = RegexValidator(
        regex=REGEX_PHONE_SIMPLE,
        message="Phone number invalid. Expected : 10 to 15 digits.",
    )
    REGEX_EMAIL = RegexValidator(
        regex=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        message="Email Id is invalid.",
    )
    # --------------------------------------------------
    #               CHOICES + SCHEMAS
    # --------------------------------------------------
    DEV = 0
    QAS = 1
    PRD = 2
    SYSTEM = [
        (DEV, "Development"),
        (QAS, "Quality"),
        (PRD, "Production"),
    ]
    PENDING = 0
    DONE = 1
    REJECTED = 2
    STATUS = [
        (PENDING, "Pending"),
        (DONE, "Done"),
        (REJECTED, "Rejected"),
    ]
    RAW = 0
    HTML = 1
    EMAIL_TYPE = [
        (RAW, "Raw"),
        (HTML, "HTML"),
    ]
    IN = 0
    OUT = 1
    DIRECTION = [
        (IN, "Inbound"),
        (OUT, "Outbound"),
    ]
    API = "API"
    USER = "USER"
    ID = "ID"
    JWT = "JWT"
    TOKEN_ROOT = schemadict(
        {
            API: {
                "type": str,
                "max_len": 255,
            },
            USER: {
                "type": str,
                "max_len": 255,
            },
        }
    )
    TOKEN_LEAF = schemadict(
        {
            ID: {
                "type": int,
                ">": 0,
            },
            JWT: {
                "type": str,
                "max_len": 255,
            },
        }
    )


# ==============================================================================
#                                       CODE
# ==============================================================================
class Utility(object):
    # --------------------------------------------------
    #               TOKEN
    # --------------------------------------------------
    @staticmethod
    def packTokenRoot(token_ser: dict, token=None, flag=True) -> str:
        if token in Constant.NULL:
            _return = {
                Constant.API: None,
                Constant.USER: None,
            }
        else:
            _return = token

        if flag:
            _return[Constant.API] = Utility.dictToB64(token_ser)
        else:
            _return[Constant.USER] = Utility.dictToB64(token_ser)
        return _return

    @staticmethod
    def packTokenLeaf(id: int, token: str) -> str:
        _return = {
            Constant.ID: id,
            Constant.JWT: token,
        }
        _return = Utility.dictToB64(_return)
        return _return

    @staticmethod
    def unpackTokenRoot(data: str) -> dict:
        _return = Utility.b64ToDict(data)
        if _return not in Constant.NULL:
            try:
                Constant.TOKEN_ROOT.validate(_return)
            except Exception as e:
                print(f"ERROR : {str(e)}")
                _return = None
        return _return

    # --------------------------------------------------
    #               OTHERS
    # --------------------------------------------------
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
            _return = math.ceil(Utility.log(n, 2)) == math.floor(
                Utility.log(n, 2)
            )
        return _return

    @staticmethod
    def addToHexadecimal(operand1="0", operand2=1):
        return hex(int(("0x" + operand1.lower()), 16) + operand2)[2:]

    # --------------------------------------------------
    #               CRYPT
    # --------------------------------------------------
    @staticmethod
    def packTokenEnc(token: str) -> str:
        crypt = Fernet(Utility.stringToHashHex(Constant.SETTINGS_SECRET))
        _return = crypt.encrypt(token.encode(Constant.UTF8)).decode(
            Constant.UTF8
        )
        return _return

    def packTokenDec(token: str) -> str:
        crypt = Fernet(Utility.stringToHashHex(Constant.SETTINGS_SECRET))
        _return = crypt.decrypt(token.encode(Constant.UTF8)).decode(
            Constant.UTF8
        )
        return _return

    @staticmethod
    def stringToHashHex(*args: tuple) -> str:
        if len(args) == 0:
            raise KeyError("No arguments passed")
        else:
            data = Constant.BLANK_STR.join(args)
            return Constant.MD5 + md5(data.encode()).hexdigest()

    @staticmethod
    def randomGenerator(length=225, only_num=False, no_symbol=False) -> str:
        choices = list()
        choices.extend(list(string.ascii_lowercase + string.ascii_uppercase))
        if not only_num:
            choices.extend(list(string.digits))
        if not no_symbol:
            choices.extend(list(string.punctuation))
        _return = "".join([random.choice(choices) for _ in range(length)])

        return _return

    # --------------------------------------------------
    #               TIME
    # --------------------------------------------------
    @staticmethod
    def datetimeToEpochMs(
        dt: datetime,
        add_hours=0,
        add_minutes=0,
        add_seconds=0,
        add_days=0,
        add_months=0,
        add_years=0,
    ) -> int:
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
    def epochMsToDatetime(epoch: int) -> datetime:
        return datetime.fromtimestamp(epoch // 1000)

    @staticmethod
    def datetimeToStr(data: datetime) -> str:
        return data.strftime("%m/%d/%Y, %H:%M:%S")

    @staticmethod
    def msToStr(data: int) -> str:
        _return = Utility.epochMsToDatetime(data)
        return _return.strftime("%m/%d/%Y, %H:%M:%S")

    # --------------------------------------------------
    #               DICT
    # --------------------------------------------------
    @staticmethod
    def dictToB64(data: dict) -> str:
        try:
            _return = json.dumps(data)
            _return = _return.encode(Constant.UTF8)
            _return = base64.b64encode(_return)
            _return = _return.decode(Constant.UTF8)
        except Exception as e:
            print(f"ERROR : {str(e)}")
            _return = None
        return _return

    @staticmethod
    def b64ToDict(data: str) -> dict:
        try:
            _return = data.encode(Constant.UTF8)
            _return = base64.b64decode(_return)
            _return = _return.decode(Constant.UTF8)
            _return = json.loads(_return)
        except Exception as e:
            print(f"ERROR : {str(e)}")
            _return = None
        return _return


class Mailer(object):
    def __init__(self) -> None:
        super(Mailer, self).__init__()

    def prepare(self) -> None:
        pass
