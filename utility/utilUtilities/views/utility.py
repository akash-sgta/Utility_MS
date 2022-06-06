# =========================================================================================
#                                       DOCUMENTATION
# =========================================================================================

# =========================================================================================
#                                       LIBRARY
# =========================================================================================
import os
from hashlib import md5
from re import sub
import string
import json
import base64
import random
import math
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from aspose import words as aw
from schemadict import schemadict
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.validators import RegexValidator

# --------------------------------------------------
from utilUtilities.serializers import Mailer_Serializer

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
    def log(exp: int, base: int) -> float:
        if exp == 0:
            _return = False
        else:
            _return = math.log10(exp) / math.log10(base)
        return _return

    @staticmethod
    def isPowerOfTwo(n: int) -> bool:
        if n == 1:
            _return = False
        else:
            _return = math.ceil(Utility.log(n, 2)) == math.floor(
                Utility.log(n, 2)
            )
        return _return

    @staticmethod
    def addToHexadecimal(operand1="0", operand2=1) -> str:
        return hex(int(("0x" + operand1.lower()), 16) + operand2)[2:]

    # --------------------------------------------------
    #               CRYPT
    # --------------------------------------------------
    @staticmethod
    def packTokenEnc(token: str) -> str:
        try:
            key = Utility.stringToHashHex(Constant.SETTINGS_SECRET)
            token = token.encode(Constant.UTF8)
            crypt = Fernet(key)
            _return = crypt.encrypt(token)
            _return = _return.decode(Constant.UTF8)
        except Exception as e:
            print(f"ERROR : {str(e)}")
            _return = None
        return _return

    def packTokenDec(token: str) -> str:
        try:
            key = Utility.stringToHashHex(Constant.SETTINGS_SECRET)
            token = token.encode(Constant.UTF8)
            crypt = Fernet(key)
            _return = crypt.decrypt(token)
            _return = _return.decode(Constant.UTF8)
        except Exception as e:
            print(f"ERROR : {str(e)}")
            _return = None
        return _return

    @staticmethod
    def stringToHashHex(*args: tuple) -> str:
        try:
            if len(args) == 0:
                raise KeyError("No arguments passed")
            else:
                data = Constant.BLANK_STR.join(args)
                _return = Constant.MD5 + md5(data.encode()).hexdigest()
        except Exception as e:
            print(f"ERROR : {str(e)}")
            _return = None
        return _return

    @staticmethod
    def randomGenerator(length=225, only_num=False, no_symbol=False) -> str:
        try:
            choices = list()
            choices.extend(
                list(string.ascii_lowercase + string.ascii_uppercase)
            )
            if not only_num:
                choices.extend(list(string.digits))
            if not no_symbol:
                choices.extend(list(string.punctuation))
            _return = "".join([random.choice(choices) for _ in range(length)])
        except Exception as e:
            print(f"ERROR : {str(e)}")
            _return = None
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
        try:
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

            _return = dt
            for item in delta:
                _return += item
            _return = int(_return.timestamp() * 1000)
        except Exception as e:
            print(f"ERROR : {str(e)}")
            _return = None
        return _return

    @staticmethod
    def epochMsToDatetime(epoch: int) -> datetime:
        try:
            datetime.fromtimestamp(epoch // 1000)
        except Exception as e:
            print(f"ERROR : {str(e)}")
            _return = None
        return _return

    @staticmethod
    def datetimeToStr(data: datetime) -> str:
        try:
            data.strftime("%m/%d/%Y, %H:%M:%S")
        except Exception as e:
            print(f"ERROR : {str(e)}")
            _return = None
        return _return

    @staticmethod
    def msToStr(data: int) -> str:
        try:
            _return = Utility.epochMsToDatetime(data)
            _return = _return.strftime("%m/%d/%Y, %H:%M:%S")
        except Exception as e:
            print(f"ERROR : {str(e)}")
            _return = None
        return _return

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

    def send(
        self,
        subject: str,
        message: str,
        from_email: str,
        to_email: list,
        bcc_email: list,
        cc_email: list,
        attachment: list,
    ) -> bool:
        _return = True
        if (
            subject not in Constant.NULL
            and to_email not in Constant.NULL
            and from_email not in Constant.NULL
        ):
            _return = False
        else:
            try:
                email = EmailMessage(
                    subject=subject.upper(),
                    body=message,
                    from_email=from_email,
                    to=to_email,
                    bcc=bcc_email,
                )
                if len(attachment) > 0:
                    for att in attachment:
                        try:
                            Constant.ATTACHMENT.validate(att)
                        except Exception as e:
                            raise e
                        else:
                            try:
                                email.attach(
                                    filename=att[Constant.NAME],
                                    content=att[Constant.CONTENT],
                                    mimetype=att[Constant.MIMETYPE],
                                )
                            except Exception as e:
                                print(f"ERROR : {str(e)}")
                                _return = False
            except Exception as e:
                print(f"ERROR : {str(e)}")
                _return = False
            return _return


class Converter(object):
    QUALITY = 100

    def __init__(self) -> None:
        super(Converter, self).__init__()

    @staticmethod
    def genFileName(path: str, final_ext: str) -> str:
        final_ext = final_ext.lower()
        path = path.split("/")
        file_name = path[-1].split(".")
        if len(file_name) > 1:
            file_name = (".").join(file_name[:-1])
        file_name = f"{file_name}.{final_ext}"
        path[-1] = file_name
        return ("/").join(path)

    @staticmethod
    def wordToPdf(path: str, img_compression=0) -> bool:
        try:
            # convert(input_path=path)
            doc = aw.Document(os.path.join(BASE_DIR, path))
            save_options = aw.saving.PdfSaveOptions()
            save_options.compliance = aw.saving.PdfCompliance.PDF17
            save_options.image_compression[0] = (
                aw.saving.PdfImageCompression.JPEG,
            )
            save_options.jpeg_quality = Converter.QUALITY - img_compression
            doc.save(
                os.path.join(path, Converter.genFileName(path, "PDF")),
                save_options,
            )
            _return = True
        except Exception as e:
            print(f"ERROR : {str(e)}")
            _return = False
        return _return


class BatchJobs(object):
    def __init__(self) -> None:
        super(BatchJobs, self).__init__()

    def mail(self) -> None:
        mailer_ref = Mailer.objects.filter(
            sys=Constant.SETTINGS_SYSTEM, status=Constant.PENDING
        )
        if len(mailer_ser) > 0:
            mailer_ser = Mailer_Serializer(mailer_ref, many=True).data
            for i in range(len(mailer_ref)):
                try:
                    _attachment = json.loads(mailer_ser[i]["attachment"])
                    _attachment = _attachment["ATTACHMENT"]
                except Exception as e:
                    _attachment = None
                else:
                    try:
                        if not Mailer.send(
                            subject=mailer_ser[i]["subject"],
                            message=mailer_ser[i]["body"],
                            from_email=mailer_ser[i]["sender"],
                            to_email=mailer_ser[i]["receiver"].split(
                                Constant.COMA
                            ),
                            cc_email=mailer_ser[i]["cc"].split(Constant.COMA),
                            bcc_email=mailer_ser[i]["bcc"].split(
                                Constant.COMA
                            ),
                            attachment=_attachment,
                        ):
                            mailer_ser[i]["status"] = Constant.REJECTED
                            mailer_ser[i]["reason"] = Constant.INVALID_PAYLOAD
                            mailer_change_ref = mailer_ref.get(
                                id=mailer_ser[i]["id"]
                            )
                            mailer_change_ser = Mailer_Serializer(
                                mailer_change_ref, mailer_ser[i]
                            )
                            if mailer_change_ser.is_valid():
                                try:
                                    mailer_change_ser.save()
                                except Exception as e:
                                    print(f"ERROR : {str(e)}")
                    except Exception as e:
                        print(f"ERROR : {str(e)}")
        return

    def notification(self) -> None:
        return
