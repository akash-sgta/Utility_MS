# =========================================================================================
#                                       DOCUMENTATION
# =========================================================================================
# =========================================================================================
#                                       LIBRARY
# =========================================================================================
from schemadict import schemadict

# =========================================================================================
#                                       CONSTANT
# =========================================================================================
K_SYSTEM = "SYSTEM"
K_SECRET_KEY = "SECRET_KEY"
K_DEBUG = "DEBUG"
K_ALLOWED_HOSTS = "ALLOWED_HOSTS"
K_ID = "ID"
K_NAME = "NAME"
K_ADMIN = "ADMIN"
K_EMAIL = "EMAIL"
K_HOST_USER = "HOST_USER"
K_HOST_PASSWORD = "HOST_PASSWORD"
K_HOST_PORT = "HOST_PORT"
K_TELEGRAM = "TELEGRAM"
K_KEY = "KEY"

SCHEMA_SYSTEM = schemadict(
    {
        K_ID: {
            "type": int,
            "<=": 10,
        },
        K_NAME: {
            "type": str,
            "max_len": 63,
        },
        K_SECRET_KEY: {
            "type": str,
            "max_len": 127,
        },
        K_DEBUG: {
            "type": bool,
        },
        K_ALLOWED_HOSTS: {
            "type": list,
            "item_schema": {
                "type": str,
            },
        },
    }
)
SCHEMA_ADMIN_EMAIL = schemadict(
    {
        K_HOST_USER: {
            "type": str,
            "max_len": 127,
        },
        K_HOST_PASSWORD: {
            "type": str,
            "max_len": 255,
        },
        K_HOST_PORT: {
            "type": int,
        },
    }
)
SCHEMA_ADMIN_TG = schemadict(
    {
        K_NAME: {
            "type": str,
            "max_len": 63,
        },
        K_KEY: {
            "type": str,
            "max_len": 255,
        },
    }
)
SCHEMA_ADMIN = schemadict(
    {
        K_EMAIL: {
            "type": dict,
        },
        K_TELEGRAM: {
            "type": dict,
        },
    }
)
SCHEMA_SECRET_FILE = schemadict(
    {
        K_SYSTEM: {
            "type": dict,
        },
        K_ADMIN: {
            "type": dict,
        },
    }
)

# =========================================================================================
#                                       CODE
# =========================================================================================


def validateKey(json_secret: dict) -> bool:
    try:
        SCHEMA_SECRET_FILE.validate(json_secret)
        SCHEMA_SYSTEM.validate(json_secret[K_SYSTEM])
        SCHEMA_ADMIN.validate(json_secret[K_ADMIN])
        SCHEMA_ADMIN_EMAIL.validate(json_secret[K_ADMIN][K_EMAIL])
        SCHEMA_ADMIN_TG.validate(json_secret[K_ADMIN][K_TELEGRAM])
    except Exception as e:
        print(f"ERROR : {str(e)}")
        return False
    else:
        return True
