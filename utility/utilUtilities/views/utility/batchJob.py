# =========================================================================================
#                                       DOCUMENTATION
# =========================================================================================

# =========================================================================================
#                                       LIBRARY
# =========================================================================================
from re import compile
from threading import Thread

# --------------------------------------------------
from utilUtilities.models import Mailer, Notification
from utilUtilities.serializers import (
    Mailer_Serializer,
    Notification_Serializer,
)
from utilUtilities.views.utility.mailerUtil import Mailer_Util
from utilUtilities.views.utility.telegramUtil import Telegram_Util
from utilUtilities.views.utility.constant import Constant


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

    def _notif(self, api: int, status: int) -> bool:
        try:
            notif_ref = Notification.objects.filter(
                sys=Constant.SETTINGS_SYSTEM,
                api=api,
                status=status,
            )
            if len(notif_ref) == 0:
                return True
            else:
                notif_ser = Notification_Serializer(notif_ref, many=True).data
                for i in range(len(notif_ref)):
                    # filter user id list
                    receivers = notif_ser[i]["receiver"].split(Constant.COMA)
                    util = []
                    for j in range(len(receivers)):
                        if not EMAIL_REGEX.fullmatch(receivers[j]):
                            receivers[j] = None
                            continue
                        # Send notificaiton
                        ret = Telegram_Util.send(
                            receiver=receivers,
                            subject=notif_ser[i]["subject"],
                            message=notif_ser[i]["body"],
                        )
                        if ret not in Constant.NULL:
                            util.append((receivers[j], ret))
                        if len(util) == 0:
                            util = None
                    receivers.remove(None)
                    # Check errors
                    if util not in Constant.NULL:
                        notif_ser[i]["reason"] = util
                        if len(receivers) == len(util):
                            notif_ser[i]["status"] = Constant.REJECTED
                        else:
                            notif_ser[i]["status"] = Constant.PARTIAL
                    else:
                        notif_ser[i]["status"] = Constant.DONE
                    notif_ser_new = Notification_Serializer(
                        notif_ref[i], notif_ser[i]
                    )
                    try:
                        if notif_ser_new.is_valid():
                            notif_ser_new.save()
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
            _return = self._notif(api=self.api, status=self.status)
        return _return


class TGBot(Thread):
    def __init__(self) -> None:
        self.tg_ref = None

    def run(self) -> bool:
        self.tg_ref = Telegram_Util()
        return self.tg_ref.run()

    def stop(self) -> int:
        return self.tg_ref.changeStatus(status=False)
