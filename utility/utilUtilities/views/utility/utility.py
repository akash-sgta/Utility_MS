# =========================================================================================
#                                       DOCUMENTATION
# =========================================================================================

# =========================================================================================
#                                       LIBRARY
# =========================================================================================
from hashlib import md5
import string
import json
import base64
import random
import math
from datetime import datetime, timedelta
from cryptography.fernet import Fernet

# --------------------------------------------------
from utilUtilities.views.utility.constant import Constant

# ==============================================================================
#                                       CONSTANT
# ==============================================================================

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

    @staticmethod
    def unpackTokenLeaf(data: str) -> dict:
        _return = Utility.b64ToDict(data)
        if _return not in Constant.NULL:
            try:
                Constant.TOKEN_LEAF.validate(_return)
            except Exception as e:
                print(f"ERROR : {str(e)}")
                _return = None
        return _return

    # --------------------------------------------------
    #               OTHERS
    # --------------------------------------------------
    @staticmethod
    def emailListGen(emails: str) -> list:
        """
        Generate a list of emails after checking validity
        """
        emails = emails.split(Constant.COMA)
        for i in len(emails):
            emails[i] = emails[i].strip()
            if Constant.RE_EMAIL.fullmatch(string=emails[i]):
                emails[i] = emails[i].upper()
            else:
                emails[i] = None
        emails.remove(None)
        return emails

    @staticmethod
    def tgUserListGen(users: str) -> list:
        """
        Generate a list of tg user id(s) after checking validity
        """
        users = users.split(Constant.COMA)
        for i in len(users):
            users[i] = users[i].strip()
            if not Constant.RE_TG.fullmatch(string=users[i]):
                users[i] = None
        users.remove(None)
        return users

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
            _return = datetime.fromtimestamp(epoch // 1000)
        except Exception as e:
            print(f"ERROR : {str(e)}")
            _return = None
        return _return

    @staticmethod
    def datetimeToStr(data: datetime) -> str:
        try:
            _return = data.strftime("%m/%d/%Y, %H:%M:%S")
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
