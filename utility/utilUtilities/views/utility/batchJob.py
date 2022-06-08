# =========================================================================================
#                                       DOCUMENTATION
# =========================================================================================

# =========================================================================================
#                                       LIBRARY
# =========================================================================================
import json
from django.core.mail import EmailMessage

# --------------------------------------------------
from utilUtilities.views.utility.constant import Constant
from utilUtilities.serializers import (
    Mailer_Serializer,
    Notificaiton_Serializer,
)
from utilUtilities.models import Mailer, Notification

# ==============================================================================
#                                       CONSTANT
# ==============================================================================

# ==============================================================================
#                                       CODE
# ==============================================================================


class Mailer_Util(object):
    def __init__(self) -> None:
        super(Mailer_Util, self).__init__()

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


class Notification_Util(object):
    def __init__(self) -> None:
        super(Notification_Util, self).__init__()

    def send(
        self,
        subject: str,
        message: str,
        to_tg: list,
        attachment: list,
    ) -> bool:
        _return = True
        if subject not in Constant.NULL and to_tg not in Constant.NULL:
            _return = False
        else:
            try:
                pass
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
                        if not Mailer_Util.send(
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
                        else:
                            mailer_ser[i]["status"] = Constant.DONE

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
        notif_ref = Notification.objects.filter(
            sys=Constant.SETTINGS_SYSTEM, status=Constant.PENDING
        )
        if len(notif_ser) > 0:
            notif_ser = Notificaiton_Serializer(notif_ref, many=True).data
            for i in range(len(notif_ref)):
                try:
                    _attachment = json.loads(notif_ser[i]["attachment"])
                    _attachment = _attachment["ATTACHMENT"]
                except Exception as e:
                    _attachment = None
                else:
                    try:
                        if not Notification_Util.send(
                            subject=notif_ser[i]["subject"],
                            message=notif_ser[i]["body"],
                            to_tg=notif_ser[i]["receiver"].split(
                                Constant.COMA
                            ),
                            attachment=_attachment,
                        ):
                            notif_ser[i]["status"] = Constant.REJECTED
                            notif_ser[i]["reason"] = Constant.INVALID_PAYLOAD
                        else:
                            notif_ser[i]["status"] = Constant.DONE

                        notif_change_ref = notif_ref.get(
                            id=notif_ser[i]["id"]
                        )
                        notif_change_ser = Notificaiton_Serializer(
                            notif_change_ref, notif_ser[i]
                        )
                        if notif_change_ser.is_valid():
                            try:
                                notif_change_ser.save()
                            except Exception as e:
                                print(f"ERROR : {str(e)}")
                    except Exception as e:
                        print(f"ERROR : {str(e)}")
        return
