# =========================================================================================
#                                       DOCUMENTATION
# =========================================================================================

# =========================================================================================
#                                       LIBRARY
# =========================================================================================
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
    SETTINGS_EMAIL = settings.EMAIL_HOST_USER
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
    EQUAL = "eq"
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
    SYSTEM_CHOICE = [
        (DEV, "Development"),
        (QAS, "Quality"),
        (PRD, "Production"),
    ]
    PENDING = 0
    DONE = 1
    REJECTED = 2
    STATUS_CHOICE = [
        (PENDING, "Pending"),
        (DONE, "Done"),
        (REJECTED, "Rejected"),
    ]
    RAW = 0
    HTML = 1
    EMAIL_TYPE_CHOICE = [
        (RAW, "Raw"),
        (HTML, "HTML"),
    ]
    IN = 0
    OUT = 1
    DIRECTION_CHOICE = [
        (IN, "Inbound"),
        (OUT, "Outbound"),
    ]
    API = "API"
    USER = "USER"
    ID = "ID"
    JWT = "JWT"
    TOKEN_ROOT = schemadict(
        {
            API: {"type": str, "max_len": 255},
            USER: {"type": str, "max_len": 255},
        }
    )
    TOKEN_LEAF = schemadict(
        {
            ID: {"type": int, ">": 0},
            JWT: {"type": str, "max_len": 255},
        }
    )
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
