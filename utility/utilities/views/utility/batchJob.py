# =========================================================================================
#                                       DOCUMENTATION
# =========================================================================================

# =========================================================================================
#                                       LIBRARY
# =========================================================================================
from re import compile
from threading import Thread

# --------------------------------------------------
from utilities.models import Mailer, Telegram
from utilities.serializers import (
    Mailer_Serializer,
    Telegram_Serializer,
)
from utilities.views.utility.mailerUtil import Mailer_Util
from utilities.views.utility.telegramUtil import Telegram_Util
from utilities.views.utility.constant import Constant


# ==============================================================================
#                                       CONSTANT
# ==============================================================================
EMAIL_REGEX = compile(r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$")
TG_REGEX = compile(r"^\d+$")
# ==============================================================================
#                                       CODE
# ==============================================================================


class BatchJob(Thread):
    def __init__(self, mailer: bool, api: int, status: int) -> None:
        super(BatchJob, self).__init__()
        self.mailer = mailer
        self.api = api
        self.status = status

    def _mailer(self, api: int, status: int) -> bool:
        try:
            mailer_ref = Mailer.objects.filter(
                sys=Constant.SETTINGS_SYSTEM,
                api=api,
                status=status,
            )
            if len(mailer_ref) == 0:
                return True
            else:
                mailer_ser = Mailer_Serializer(mailer_ref, many=True).data
                for i in range(len(mailer_ref)):
                    # filter email list
                    receivers = mailer_ser[i]["receiver"].split(Constant.COMA)
                    cc = mailer_ser[i]["cc"].split(Constant.COMA)
                    bcc = mailer_ser[i]["bcc"].split(Constant.COMA)
                    for j in range(len(receivers)):
                        if not EMAIL_REGEX.fullmatch(receivers[j]):
                            receivers[j] = None
                    receivers.remove(None)
                    for j in range(len(cc)):
                        if not EMAIL_REGEX.fullmatch(cc[j]):
                            cc[j] = None
                    cc.remove(None)
                    for j in range(len(bcc)):
                        if not EMAIL_REGEX.fullmatch(bcc[j]):
                            bcc[j] = None
                    bcc.remove(None)
                    # Send email
                    util = Mailer_Util.send(
                        receiver=receivers,
                        subject=mailer_ser[i]["subject"],
                        message=mailer_ser[i]["body"],
                        cc=cc,
                        bcc=bcc,
                    )
                    # Check Errors
                    if util not in Constant.NULL:
                        mailer_ser[i]["status"] = Constant.REJECTED
                        mailer_ser[i]["reason"] = util
                    else:
                        mailer_ser[i]["status"] = Constant.DONE
                    mailer_ser_new = Mailer_Serializer(
                        mailer_ref[i], mailer_ser[i]
                    )
                    try:
                        if mailer_ser_new.is_valid():
                            mailer_ser_new.save()
                    except Exception as e:
                        print(f"ERROR : {str(e)}")
        except Exception as e:
            print(f"ERROR : {str(e)}")
            return False
        else:
            return True

    def _tg(self, api: int, status: int) -> bool:
        try:
            tg_ref = Telegram.objects.filter(
                sys=Constant.SETTINGS_SYSTEM,
                api=api,
                status=status,
            )
            if len(tg_ref) == 0:
                return True
            else:
                tg_ser = Telegram_Serializer(tg_ref, many=True).data
                for i in range(len(tg_ref)):
                    # filter user id list
                    receivers = tg_ser[i]["receiver"].split(Constant.COMA)
                    util = []
                    for j in range(len(receivers)):
                        if not EMAIL_REGEX.fullmatch(receivers[j]):
                            receivers[j] = None
                            continue
                        # Send tg
                        ret = Telegram_Util.send(
                            receiver=receivers,
                            subject=tg_ser[i]["subject"],
                            message=tg_ser[i]["body"],
                        )
                        if ret not in Constant.NULL:
                            util.append((receivers[j], ret))
                        if len(util) == 0:
                            util = None
                    receivers.remove(None)
                    # Check errors
                    if util not in Constant.NULL:
                        tg_ser[i]["reason"] = util
                        if len(receivers) == len(util):
                            tg_ser[i]["status"] = Constant.REJECTED
                        else:
                            tg_ser[i]["status"] = Constant.PARTIAL
                    else:
                        tg_ser[i]["status"] = Constant.DONE
                    tg_ser_new = Telegram_Serializer(tg_ref[i], tg_ser[i])
                    try:
                        if tg_ser_new.is_valid():
                            tg_ser_new.save()
                    except Exception as e:
                        print(f"ERROR : {str(e)}")
        except Exception as e:
            print(f"ERROR : {str(e)}")
            return False
        else:
            return True

    def run(self) -> bool:
        if self.mailer:
            _return = self._mailer(api=self.api, status=self.status)
        else:
            _return = self._tg(api=self.api, status=self.status)
        return _return


class TGBot(Thread):
    def __init__(self) -> None:
        self.tg_ref = Telegram_Util()

    def run(self) -> None:
        return self.tg_ref.run()

    def stop(self) -> None:
        return self.tg_ref.stop()
