# --------------------------------------------------------------------------
# CONSTANTS
# --------------------------------------------------------------------------
DOC_TYPE = (
    (1, "IMAGE"),
    (2, "EXCEL"),
    (3, "PDF"),
    (4, "WORD"),
    (5, "OTHERS"),
)
IMG_SIZE = {"L": "1280x1024", "M": "1024x786", "S": "320x240"}
# --------------------------------------------------------------------------
ERROR_RT_TIMEOUT = {"ERROR": "REFRESH TOKEN TIMEOUT"}
ERROR_AT_TIMEOUT = {"ERROR": "ACCESS TOKEN TIMEOUT"}
ERROR_PD_REQUIRED = {"ERROR": "Password required"}
# --------------------------------------------------------------------------
INVALID_USERNAME = {"ERROR": "INVALID USERNAME"}
INVALID_PASSWORD = {"ERROR": "INVALID PASSWORD"}
INVALID_DEVICE = {"ERROR": "USER DEVICE MISMATCH"}
INVALID_USER_ID = {"ERROR": "INVALID USER ID"}
INVALID_TOKEN_ENC = {"ERROR": "INVALID TOKEN ENCODING"}
INVALID_AT = {"ERROR": "INVALID ACCESS TOKEN"}
ERROR_ACC_INACTIVE = {"ERROR": "ACCOUNT INACTIVE"}
ERROR_BACKEND = {"ERROR": "BACKEND ERROR"}
CONFLICT_USERNAME = {"ERROR": "USERNAME EXISTS"}
ERROR_AT_GEN = {"ERROR": "ACCESS TOKEN NOT GENERATED"}
KEYS = ["id", "jwt"]
TOKEN_HEADER = ["BEARER", "JWT"]
SPACE_1 = " "
AUTHORIZATION = "Authorization"
UTF8 = "utf-8"
INVALID_API_KEY = {"ERROR": "API Key is invalid"}
# --------------------------------------------------------------------------
INVALID_ID = {"ERROR": "INVALID ID"}
INVALID_FORMATTING = "INVALID FORMATTING"
# --------------------------------------------------------------------------
COUNTRY = "COUNTRY"
STATE = "STATE"
CITY = "CITY"
# --------------------------------------------------------------------------
ERROR_CRUD_GEN = {"ERROR": None}
ERROR_CRUD_C = {"ERROR": "CREATE ERROR"}
ERROR_CRUD_R = {"ERROR": "READ ERROR"}
ERROR_CRUD_U = {"ERROR": "UPDATE ERROR"}
ERROR_CRUD_D = {"ERROR": "DELETE ERROR"}
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
# --------------------------------------------------------------------------
