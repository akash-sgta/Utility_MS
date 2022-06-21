# =========================================================================================
#                                       DOCUMENTATION
# =========================================================================================

# =========================================================================================
#                                       LIBRARY
# =========================================================================================
from re import compile
from schemadict import schemadict
from django.conf import settings
from django.core.validators import RegexValidator

# ==============================================================================
#                                       CONSTANT
# ==============================================================================


# ==============================================================================
#                                       CODE
# ==============================================================================
class Constant(object):
    # --------------------------------------------------
    #               PAYLOAD
    # --------------------------------------------------
    STATUS = "STATUS"
    DATA = "DATA"
    MESSAGE = "MESSAGE"
    SETTINGS_TIMEZONE = "TIMEZONE"
    BLANK_LIST = []
    BLANK_STR = ""
    RETURN_JSON = {
        STATUS: False,
        DATA: BLANK_LIST,
        MESSAGE: BLANK_STR,
        SETTINGS_TIMEZONE: settings.TIME_ZONE,
    }
    # --------------------------------------------------
    #               SYSTEM PARAMS
    # --------------------------------------------------
    SETTINGS_SYSTEM = settings.SYSTEM
    SETTINGS_SYSTEM_NAME = settings.SERVER_NAME
    SETTINGS_EMAIL_EMAIL = settings.EMAIL_HOST_USER
    SETTINGS_EMAIL_PASSWORD = settings.EMAIL_HOST_PASSWORD
    SETTINGS_EMAIL_PORT = settings.EMAIL_HOST_PORT
    SETTINGS_SECRET = settings.SECRET_KEY
    SETTINGS_TG_KEY = settings.TELEGRAM_KEY
    # --------------------------------------------------
    #               INVALID
    # --------------------------------------------------
    INVALID_SPARAMS = "INVALID SEARCH PARAMETERS"
    INVALID_API = "INVALID API"
    INVALID_URL = "INVALID URL"
    INVALID_PAYLOAD = "INVALID DATA POSTED"
    INVALID_TOKEN = "INVALID API TOKEN"
    INVALID_CRED = "INVALID API CREDENTIALS"
    # --------------------------------------------------
    #               OTHERS
    # --------------------------------------------------
    FOOTER = "THIS IS AN UNMONITORED MAILBOX, DO NOT REPLY\n"
    METHOD_NOT_ALLOWED = "METHOD NOT ALLOWED"
    NO_CONTENT = "NO CONTENT FOUND"
    SYS = "sys"
    NULL = (None, "", 0)
    COMA = ","
    SPACE = " "
    EQUAL = "eq"
    EQUAL2 = "="
    MD5 = "md5_"
    UTF8 = "utf-8"
    ATTACHMENT = "ATTACHMENT"
    AUTHORIZATION = "Authorization"
    BEARER = "Bearer"
    JWT = "Jwt"
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
    RE_EMAIL = compile(
        pattern=r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
    )
    RE_TG = compile(pattern=r"^[0-9]+$")
    REGEX_INTEGER = RegexValidator(regex=r"\d+", message="Should be numbers")
    # --------------------------------------------------
    #               CHOICES + SCHEMAS
    # --------------------------------------------------
    DEV = 0
    QAS = 1
    PRD = 2
    SYSTEM_CHOICE = [
        (DEV, "Development"),
        (QAS, "Quality"),
        (PRD, "Production"),
    ]
    # ---------------------
    PENDING = 0
    DONE = 1
    REJECTED = 2
    PARTIAL = 3
    STATUS_CHOICE = [
        (PENDING, "Pending"),
        (DONE, "Done"),
        (REJECTED, "Rejected"),
        (PARTIAL, "Partial"),
    ]
    # ---------------------
    RAW = 0
    HTML = 1
    EMAIL_TYPE_CHOICE = [
        (RAW, "Raw"),
        (HTML, "HTML"),
    ]
    # ---------------------
    SELF = 0
    IN = 1
    OUT = 2
    DIRECTION_CHOICE = [
        (SELF, "Self"),
        (IN, "Inbound"),
        (OUT, "Outbound"),
    ]
    # ---------------------
    REQUEST = 0
    API = 1
    MODEL_MODEL_CHOICE = [
        (REQUEST, "Request"),
        (API, "Api"),
    ]
    # ---------------------
    SEARCH = 0
    ID = 1
    MODEL_TYPE_CHOICE = [
        (SEARCH, "Search"),
        (ID, "Id"),
    ]
    # ---------------------
    NOTIFICATION = "notification"
    NOTIFICATION_SUBJECT = "subject"
    NOTIFICATION_BODY = "body"
    NOTIFICATION_MAILER = "mailer"
    NOTIFICATION_TELEGRAM = "telegram"
    NOTIFICATION_RECEIVER = "receiver"
    NOTIFICATION_CC = "cc"
    NOTIFICATION_BCC = "bcc"
    NOTIFICATION_DICT = {
        NOTIFICATION_SUBJECT: BLANK_STR,
        NOTIFICATION_BODY: BLANK_STR,
        NOTIFICATION_MAILER: {
            NOTIFICATION_RECEIVER: BLANK_STR,
            NOTIFICATION_CC: BLANK_STR,
            NOTIFICATION_BCC: BLANK_STR,
        },
        NOTIFICATION_TELEGRAM: {
            NOTIFICATION_RECEIVER: BLANK_STR,
        },
    }
    # ---------------------
    API = "API"
    USER = "USER"
    ID = "ID"
    JWT = "JWT"
    TOKEN = "TOKEN"
    BLANK_TOKEN_LEAF = {
        ID: 0,
        JWT: None,
    }
    TOKEN_ROOT = schemadict(
        {
            API: {
                "type": str,
                "max_len": 511,
            },
            USER: {
                "type": str,
                "max_len": 511,
            },
        }
    )
    TOKEN_LEAF = schemadict(
        {
            ID: {
                "type": int,
                ">=": 0,
            },
            JWT: {
                "type": str,
                "max_len": 255,
            },
        }
    )
    DICT_TOKEN_ROOT = schemadict(
        {
            API: {
                "type": dict,
            },
            USER: {
                "type": dict,
            },
        }
    )
    # ---------------------
    NAME = "NAME"
    CONTENT = "CONTENT"
    MIMETYPE = "MIMETYPE"
    ATTACHMENT = schemadict(
        {
            NAME: {"type": str, "max_len": 63},
            CONTENT: {"type": bytes},
            MIMETYPE: {"type": str, "max_len": 63},
        }
    )
