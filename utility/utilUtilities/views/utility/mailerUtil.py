# =========================================================================================
#                                       DOCUMENTATION
# =========================================================================================

# =========================================================================================
#                                       LIBRARY
# =========================================================================================
from yagmail import SMTP

# --------------------------------------------------
from utilUtilities.views.utility.constant import Constant
from utilUtilities.serializers import Mailer_Serializer
from utilUtilities.models import Mailer

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
        self.footer = "THIS IS AN UNMONITORED MAILBOX, DO NOT REPLY\n"

    def send(self, receiver: str, subject: str, message: str) -> bool:
        try:
            subject = subject.upper()
            message += f"\n\n\n\n{self.footer}"
            with SMTP(user=self.sender, password=self.password) as smtp:
                smtp.send(
                    to=receiver,
                    subject=subject,
                    contents=message,
                )
        except Exception as e:
            print(f"ERROR : {str(e)}")
            return False
        else:
            return True
