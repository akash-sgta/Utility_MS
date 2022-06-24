# =========================================================================================
#                                       DOCUMENTATION
# =========================================================================================

# =========================================================================================
#                                       LIBRARY
# =========================================================================================
from telegram.ext import *
from telegram import *

# ==============================================================================
#                                       CONSTANT
# ==============================================================================
REDACTED = "REDACTED"

# ==============================================================================
#                                       CODE
# ==============================================================================
class Telegram_Util(Bot):
    def __init__(self) -> None:
        self.API_KEY = REDACTED
        self.updater = Updater(token=self.API_KEY, use_context=True)
        self.dispatcher = self.updater.dispatcher
        super(Telegram_Util, self).__init__(token=self.API_KEY)

    def __start(self, update, CallbackContext) -> None:
        try:
            payload = {
                "user": update.effective_chat.id,
                "hash": update.message.text.strip().split()[1],
            }
        except Exception as e:
            print(f"ERROR : {str(e)}")
        else:
            print(payload)
        return

    def __exit(self, update, CallbackContext) -> None:
        text = """
            STEPS TO UNSUBSCRIBE
            1. GO TO PROFILE
            2. DEACTIVATE TELEGRAM NOTIFICATION
        """
        self.send(update.effective_chat.id, text)
        return

    def __parse_message(self, update, CallbackContext):
        text = """
            Thank you for the message.
            But this is an unmonitored service.
        """
        self.send(update.effective_chat.id, text)
        return

    def __add_handlers(self) -> None:
        self.dispatcher.add_handler(CommandHandler("start", self.__start))
        self.dispatcher.add_handler(CommandHandler("exit", self.__exit))
        self.dispatcher.add_handler(
            MessageHandler(Filters.text & ~Filters.command, self.__parse_message)
        )
        return

    def send(self, chat_id: str, message: str) -> bool:
        try:
            self.send_message(
                chat_id=chat_id,
                text=message,
            )
        except Exception as e:
            print(f"ERROR : {str(e)}")
            return False
        else:
            return True

    def run(self):
        try:
            self.__add_handlers()
            self.updater.start_polling()
        except Exception as e:
            print(f"ERROR : {str(e)}")
        else:
            print("POLLING STARTED...")


Telegram_Util().run()
