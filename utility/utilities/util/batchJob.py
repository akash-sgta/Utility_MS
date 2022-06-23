# =========================================================================================
#                                       DOCUMENTATION
# =========================================================================================

# =========================================================================================
#                                       LIBRARY
# =========================================================================================
from email import message
import re
from threading import Thread, enumerate

# --------------------------------------------------
from utilities.models import Mailer, Telegram, Notification
from utilities.util.mailerUtil import Mailer_Util
from utilities.util.telegramUtil import Telegram_Util
from utilities.util.constant import Constant
from utilities.util.utility import Utility


# ==============================================================================
#                                       CONSTANT
# ==============================================================================
NO_FKEY = "\n---Notification Foreign Key not present---\n"
BOT = r"(Bot:)(\d+)(:updater)"
# ==============================================================================
#                                       CODE
# ==============================================================================


class BatchJob(Thread):
    def __init__(
        self,
        tname: str,
        mailer: bool,
        api: int,
        status: int,
        obj_id: tuple = None,
    ) -> None:
        super(BatchJob, self).__init__(name=tname)
        self.mailer = mailer
        self.api = api
        self.status = status
        self.obj_id = obj_id

    def __get_emails(self, emails: str) -> list:
        mail_list = Utility.emailListGen(emails=emails)
        return mail_list

    def __get_uids(self, uid: str) -> list:
        uid_list = uid.split(Constant.COMA)
        for i in range(len(uid_list)):
            if not Constant.RE_TELEGRAM.fullmatch(uid_list[i]):
                uid_list[i] = None
        try:
            uid_list.remove(None)
        except:
            pass

        return uid_list

    def _mailer(self) -> bool:
        try:
            if self.obj_id is None:  # Extra filter for solo post
                mailer_ref = Mailer.objects.filter(
                    sys=Constant.SETTINGS_SYSTEM,
                    status=self.status,
                )
            else:
                mailer_ref = Mailer.objects.filter(
                    sys=Constant.SETTINGS_SYSTEM,
                    status=self.status,
                    notification_id=self.obj_id[0],
                    id=self.obj_id[1],
                )
            if len(mailer_ref) == 0:
                return True
            else:
                for i in range(len(mailer_ref)):
                    try:
                        notification_ref = mailer_ref[i].notification
                        if notification_ref is None:
                            raise Exception("Invalid Foreign key")
                        else:
                            if (
                                notification_ref.sys
                                != Constant.SETTINGS_SYSTEM
                                or notification_ref.api.id != self.api
                            ):
                                raise Exception("Invalid Foreign key")
                    except Exception as e:
                        mailer_ref[i].status = Constant.REJECTED
                        if mailer_ref[i].reason is None:
                            mailer_ref[i].reason = f"{NO_FKEY}{str(e)}"
                        else:
                            mailer_ref[i].reason += f"\n\n{NO_FKEY}{str(e)}"
                        mailer_ref[i].save()
                        continue
                    else:
                        # filter email list
                        receivers = self.__get_emails(
                            emails=mailer_ref[i].receiver
                        )
                        cc = self.__get_emails(emails=mailer_ref[i].cc)
                        bcc = self.__get_emails(emails=mailer_ref[i].bcc)
                        # Send email
                        util = Mailer_Util().send(
                            receiver=receivers,
                            subject=notification_ref.subject,
                            message=notification_ref.body,
                            cc=cc,
                            bcc=bcc,
                        )
                        # Check Errors
                        if util is not None:
                            mailer_ref[i].status = Constant.PARTIAL
                            if mailer_ref[i].reason is None:
                                mailer_ref[i].reason = util
                            else:
                                mailer_ref[i].reason += f"\n\n{util}"
                        else:
                            mailer_ref[i].status = Constant.DONE
                        mailer_ref[i].save()
        except Exception as e:
            print(f"ERROR : {str(e)}")
            return False
        else:
            return True

    def _tg(self) -> bool:
        try:
            if self.obj_id is None:  # Extra filter for solo post
                tg_ref = Telegram.objects.filter(
                    sys=Constant.SETTINGS_SYSTEM,
                    status=self.status,
                )
            else:
                tg_ref = Telegram.objects.filter(
                    sys=Constant.SETTINGS_SYSTEM,
                    status=self.status,
                    notification_id=self.obj_id[0],
                    id=self.obj_id[1],
                )
            if len(tg_ref) == 0:
                return True
            else:
                for i in range(len(tg_ref)):
                    try:
                        notification_ref = tg_ref[i].notification
                        if notification_ref is None:
                            raise Exception("Invalid Foreign key")
                        else:
                            if (
                                notification_ref.sys
                                != Constant.SETTINGS_SYSTEM
                                or notification_ref.api.id != self.api
                            ):
                                raise Exception("Invalid Foreign key")
                    except Exception as e:
                        tg_ref[i].status = Constant.REJECTED
                        if tg_ref[i].reason is None:
                            tg_ref[i].reason = f"{NO_FKEY}{str(e)}"
                        else:
                            tg_ref[i].reason += f"{NO_FKEY}{str(e)}"
                        tg_ref[i].save()
                        continue
                    else:
                        # filter user id list
                        receivers = self.__get_uids(uid=tg_ref[i].receiver)
                        util = []
                        for j in range(len(receivers)):
                            # Send tg
                            message = f"{notification_ref.subject}\n"
                            message += f"{notification_ref.body}\n"
                            ret = Telegram_Util().send(
                                chat_id=receivers[j], message=message
                            )
                            if ret not in Constant.NULL:
                                util.append((receivers[j], ret))
                        # Check errors
                        if len(util) > 0:
                            if tg_ref[i].reason is None:
                                tg_ref[i].reason = util
                            else:
                                tg_ref[i].reason += f"\n\n{util}"
                            if len(receivers) == len(util):
                                tg_ref[i].status = Constant.REJECTED
                            else:
                                tg_ref[i].status = Constant.PARTIAL
                        else:
                            tg_ref[i].status = Constant.DONE
                        tg_ref[i].save()
        except Exception as e:
            print(f"ERROR : {str(e)}")
            return False
        else:
            return True

    def run(self) -> bool:
        if self.mailer:
            _return = self._mailer()
        else:
            _return = self._tg()
        return _return


class TGBot(Thread):
    def __init__(self, tname: str) -> None:
        super(TGBot, self).__init__(name=tname)
        self.tg_ref = Telegram_Util()

    def run(self) -> None:
        return self.tg_ref.run()

    def check(self) -> bool:
        thread_list = enumerate()
        try:
            for tr in thread_list:
                if re.search(BOT, tr.name) is not None:
                    return True
        except Exception as e:
            pass
        return False

    def stop(self) -> None:
        self.tg_ref.stop()
        return
