# =========================================================================================
#                                       DOCUMENTATION
# =========================================================================================

# =========================================================================================
#                                       LIBRARY
# =========================================================================================
from yagmail import SMTP

# --------------------------------------------------
from utilUtilities.views.utility.constant import Constant


# ==============================================================================
#                                       CONSTANT
# ==============================================================================


# ==============================================================================
#                                       CODE
# ==============================================================================


class Mailer_Util(object):
    def __init__(self) -> None:
        super(Mailer_Util, self).__init__()
        self.password = Constant.SETTINGS_EMAIL_PASSWORD
        self.sender = Constant.SETTINGS_EMAIL_EMAIL
        self.footer = Constant.FOOTER

    def send(
        self, receiver: list, cc: list, bcc: list, subject: str, message: str
    ) -> None:
        try:
            subject = subject.upper()
            message += f"\n\n\n\n{self.footer}"
            with SMTP(user=self.sender, password=self.password) as smtp:
                smtp.send(
                    to=receiver,
                    subject=subject,
                    contents=message,
                    cc=cc,
                    bcc=bcc,
                )
        except Exception as e:
            return str(e)
        else:
            return None
