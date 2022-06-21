# =========================================================================================
#                                       DOCUMENTATION
# =========================================================================================

# =========================================================================================
#                                       LIBRARY
# =========================================================================================
from time import sleep
from telegram.ext import *
from telegram import *
from threading import Thread

# --------------------------------------------------
from utilities.util.constant import Constant

# ==============================================================================
#                                       CONSTANT
# ==============================================================================


# ==============================================================================
#                                       CODE
# ==============================================================================
class Telegram_Util(Bot):
    def __init__(self) -> None:
        self.API_KEY = Constant.SETTINGS_TG_KEY
        self.updater = Updater(token=self.API_KEY, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.footer = Constant.FOOTER
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
            MessageHandler(
                Filters.text & ~Filters.command, self.__parse_message
            )
        )
        return

    def send(self, chat_id: str, message: str) -> str:
        message += f"\n\n\n\n{self.footer}"
        try:
            self.send_message(
                chat_id=chat_id,
                text=message,
            )
        except Exception as e:
            return str(e)
        else:
            return None

    def run(self) -> None:
        try:
            self.__add_handlers()
            self.updater.start_polling(poll_interval=15)
        except Exception as e:
            print(f"ERROR : {str(e)}")
        else:
            print("POLLING STARTED...")
        return

    def stop(self) -> None:
        try:
            self.updater.stop()
        except Exception as e:
            print(f"ERROR : {str(e)}")
        else:
            print("POLLING STOPPED...")
        return


class Telegram_Thread(Thread):
    def run(self, chat_id: list, message: str) -> None:
        for id in chat_id:
            Telegram_Util().send(chat_id=id, message=message)
        return
