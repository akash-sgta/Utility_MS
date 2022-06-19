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
from utilities.views.utility.constant import Constant

# ==============================================================================
#                                       CONSTANT
# ==============================================================================

# ==============================================================================
#                                       CODE
# ==============================================================================
class Utility(object):
    # --------------------------------------------------
    #               DICT
    # --------------------------------------------------
    @staticmethod
    def dictToB64(data: dict) -> str:
        """
        Dict to B64 String
        ------------------
        1. Check json structure
        2. Encode String to Byte_String
        3. Encode Byte_String to B64_Byte_String
        4. Decode B64_Byte_String to String
        """
        try:
            json_str = json.dumps(data)
            json_str = json_str.encode(Constant.UTF8)
            b64_str = base64.b64encode(json_str)
            b64_str = b64_str.decode(Constant.UTF8)
        except Exception as e:
            raise e
        return b64_str

    @staticmethod
    def b64ToDict(data: str) -> dict:
        """
        B64 String to Dict
        ------------------
        1. Check json structure
        2. Encode String to Byte_String
        3. Encode Byte_String to B64_Byte_String
        4. Decode B64_Byte_String to String
        """
        try:
            b64_str = data.encode(Constant.UTF8)
            json_str = base64.b64decode(b64_str)
            json_str = json_str.decode(Constant.UTF8)
            json_dict = json.loads(json_str)
        except Exception as e:
            raise e
        return json_dict

    # --------------------------------------------------
    #               CRYPT
    # --------------------------------------------------
    @staticmethod
    def encryptString(data: str, key: str) -> str:
        """
        Enc - AES encryption
        --------------------
        1. Encode String to Byte_String
        2. Encrypt using KEY
        3. Decode Byte_String => String
        """
        try:
            key[:32].encode(Constant.UTF8)
            key = base64.urlsafe_b64encode(key)
            crypt = Fernet(key)
            # --------------------
            token_enc = data.encode(Constant.UTF8)
            token_enc = crypt.encrypt(token_enc)
            token_enc = token_enc.decode(Constant.UTF8)
        except Exception as e:
            raise e
        return token_enc

    def decryptString(data: str, key: str) -> str:
        """
        Dec - AES decryption
        --------------------
        1. Encode String to Byte_String
        2. Decrypt using KEY
        3. Decode Byte_String to String
        """
        try:
            key = key[:32].encode(Constant.UTF8)
            key = base64.urlsafe_b64encode(key)
            crypt = Fernet(key)
            # --------------------
            token_dec = data.encode(Constant.UTF8)
            token_dec = crypt.decrypt(token_dec)
            token_dec = token_dec.decode(Constant.UTF8)
        except Exception as e:
            raise e
        return token_dec

    @staticmethod
    def stringToHashHex(*args: tuple) -> str:
        """
        Generate Hex Hash
        --------------------
        1. Check tuple length
        2. Join contents
        3. Encode String to Byte_String
        4. Generate md5 hash -> digest
        """
        try:
            if len(args) == 0:
                raise KeyError("No arguments passed")
            else:
                data = Constant.BLANK_STR.join(args)
                data = data.encode()
                hash_str = md5(data).hexdigest()
                hash_str = f"{Constant.MD5}{hash_str}"
        except Exception as e:
            return e
        return hash_str

    @staticmethod
    def randomGenerator(
        length: int = 225,
        only_num: bool = False,
        no_symbol: bool = False,
    ) -> str:
        """
        Generate Random String
        ----------------------
        """
        try:
            choices = list()
            choices.extend(
                list(string.ascii_lowercase + string.ascii_uppercase)
            )
            if not only_num:
                choices.extend(list(string.digits))
            if not no_symbol:
                choices.extend(list(string.punctuation))
            ranom_str = "".join(
                [random.choice(choices) for _ in range(length)]
            )
        except Exception as e:
            raise e
        return ranom_str

    # --------------------------------------------------
    #               TOKEN
    # --------------------------------------------------
    @staticmethod
    def packToken(
        api_ser: dict = None,
        user_ser: dict = None,
        token: dict = None,
        enc: bool = False,
    ) -> dict:
        """
        Token - Dict to Encrypted B64 String
        ------------------------------------
        1. Check if partial or old token reference is passed
        2. Check leaf structures
        3. Fill token dict with appropriate data
        4. Check root structure
        5. Encrypt final B64 string
        """
        if token in Constant.NULL:
            token_dict = {
                Constant.API: Constant.BLANK_TOKEN_LEAF,
                Constant.USER: Constant.BLANK_TOKEN_LEAF,
            }
        else:
            token_dict = token

        if api_ser not in Constant.NULL:
            try:
                Constant.TOKEN_LEAF.validate(api_ser)
            except Exception as e:
                raise e
            else:
                try:
                    token_dict[Constant.API] = Utility.dictToB64(api_ser)
                except Exception as e:
                    raise e

        if user_ser not in Constant.NULL:
            try:
                Constant.TOKEN_LEAF.validate(user_ser)
            except Exception as e:
                raise e
            else:
                try:
                    token_dict[Constant.USER] = Utility.dictToB64(user_ser)
                except Exception as e:
                    raise e
        try:
            Constant.TOKEN_ROOT.validate(token_dict)
            token_dict = Utility.dictToB64(token_dict)
            if enc:
                token_dict = Utility.encryptString(
                    data=token_dict,
                    key=Constant.SETTINGS_SECRET,
                )
                token_dict = {Constant.TOKEN: token_dict}
        except Exception as e:
            raise e

        return token_dict

    @staticmethod
    def unpackToken(data: str, enc: bool = False) -> dict:
        """
        Token - Encrypted B64 String to Dict
        ------------------------------------
        """
        try:
            if enc:
                token_b64 = Utility.decryptString(
                    data=data,
                    key=Constant.SETTINGS_SECRET,
                )
            else:
                token_b64 = data
            token_dict = Utility.b64ToDict(token_b64)
            Constant.TOKEN_ROOT.validate(token_dict)
            token_dict[Constant.API] = Utility.b64ToDict(
                data=token_dict[Constant.API]
            )
            token_dict[Constant.USER] = Utility.b64ToDict(
                data=token_dict[Constant.USER]
            )
            try:
                Constant.TOKEN_LEAF.validate(token_dict[Constant.API])
            except:
                token_dict[Constant.API] = Constant.BLANK_TOKEN_LEAF
            try:
                Constant.TOKEN_LEAF.validate(token_dict[Constant.USER])
            except:
                token_dict[Constant.USER] = Constant.BLANK_TOKEN_LEAF
        except Exception as e:
            raise e
        return token_dict

    # --------------------------------------------------
    #               OTHERS
    # --------------------------------------------------
    @staticmethod
    def emailListGen(emails: str) -> list:
        """
        Generate - List of valid emails
        -------------------------------
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
        Generate - List of valid telegram ids
        -------------------------------------
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
