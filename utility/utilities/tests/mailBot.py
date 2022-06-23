# =========================================================================================
#                                       DOCUMENTATION
# =========================================================================================

# =========================================================================================
#                                       LIBRARY
# =========================================================================================
from yagmail import SMTP

# ==============================================================================
#                                       CONSTANT
# ==============================================================================
REDACTED = "REDACTED"
# ==============================================================================
#                                       CODE
# ==============================================================================


class Mailer_Util(object):
    def __init__(self) -> None:
        super(Mailer_Util, self).__init__()
        self.port = 465
        self.sender = REDACTED
        self.receiver = REDACTED
        self.key = REDACTED

    def send(self) -> bool:
        try:
            with SMTP(user=self.sender, password=self.key) as smtp:
                smtp.send(
                    to=self.receiver,
                    subject="TEST MAIL",
                    contents="TEST MAIL",
                )
        except Exception as e:
            print(f"ERROR : {str(e)}")
            return False
        else:
            return True


print(Mailer_Util().send())
