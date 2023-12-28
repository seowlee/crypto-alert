import logging
import asyncio
import telegram
from telegram import ForceReply, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


with open("./token.txt") as f:
    lines = f.readlines()
    token = lines[0].strip()
    chat = lines[1].strip()

TELEGRAM_TOKEN = token
CHAT_ID = chat

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# async def send_alert(message):
#     bot = telegram.Bot(token=TELEGRAM_TOKEN)
#     await bot.sendMessage(chat_id=CHAT_ID, text=message)


# def main():
#     # self.app.add_handler(CommandHandler(command="start", callback=self.start))
#     message = " ".join(sys.argv[1:]) or "Bot에서 보낸 메세지입니다."
#     asyncio.run(send_alert(message))


# if __name__ == "__main__":
#     main()


class UpbitAlertTelegramBot:
    def __init__(self):
        self.token = TELEGRAM_TOKEN
        self.chat_id = CHAT_ID
        self.app, self.bot, self.updater, self.loop = self._build_application()
        self.telegram_thread = None
        self.app.add_handler(CommandHandler(command="start", callback=self.start))
        print("Bot initialized...")

    def _build_application(self):
        loop = asyncio.new_event_loop()
        builder = ApplicationBuilder()
        builder.token(self.token)
        app = builder.build()
        return app, app.bot, app.updater, loop

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /start is issued."""
        user = update.effective_user
        await update.message.reply_html(
            rf"Hi {user.mention_html()}!",
            reply_markup=ForceReply(selective=True),
        )

    async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """End Conversation by command."""
        await update.message.reply_text("Okay, bye.")

        return END

    async def help_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Send a message when the command /help is issued."""
        await update.message.reply_text("Help!")

    async def echo(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Echo the user message."""
        await update.message.reply_text(update.message.text)

    async def send_alert(self, message):
        bot = self.bot
        await bot.sendMessage(chat_id=CHAT_ID, text=message)

    # async def callback_msg(self, context: ContextTypes.DEFAULT_TYPE):
    #     await context.bot.send_message(
    #         chat_id=self.chat_id, text="RSI is greater than 40!"
    #     )

    # async def _send_message(self, message):
    #     print("Sending message to Telegram.. ")
    #     recipient_chat_id = self.chat_id
    #     bot = self.bot
    #     await bot.send_message(chat_id=recipient_chat_id, text=message)

    # def echo(self, message: str) -> None:
    #     """Echo the message."""
    #     # You can replace the following print statement with your logic to send the message
    #     print(f"Echo: {message}")

    def main(self) -> None:
        """Start the bot."""
        self.app.add_handler(CommandHandler(command="start", callback=self.start))
        self.app.add_handler(CommandHandler(command="stop", callback=self.stop))
        self.app.add_handler(CommandHandler(command="help", callback=self.help_command))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.echo))
        # self.job_queue.run_once(self.callback_msg, 30)
        # Run the bot until the user presses Ctrl-C
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    # Create an instance of the UpbitAlertTelegramBot class
    bot = UpbitAlertTelegramBot()
    # Call the main method to start the bot
    bot.main()
#     upbit = Upbit()

#     # 기준 차트 단위. 3 = 3분봉
#     CANDLE_MIN_UNIT = 240  # 4 hours

#     # 불러올 최대 거래량 갯수
#     MAX_COUNT = 200
#     while True:
#         candles = upbit.candles("KRW-BTC")
#         min_candles = candles.minute(unit=CANDLE_MIN_UNIT, count=MAX_COUNT)

#         df = pd.DataFrame(
#             data={
#                 "open": [x.opening_price() for x in min_candles],
#                 "close": [x.trade_price() for x in min_candles],
#                 "high": [x.high_price() for x in min_candles],
#                 "low": [x.low_price() for x in min_candles],
#             }
#         )
#         df_rsi = ta.RSI(df["close"], timeperiod=14)
#         now_rsi = df_rsi[-1:].values[0]
#         print(now_rsi)
#         time.sleep(30)
#         msg = "RSI is greater than 40!"
#         if now_rsi > 30:
#             message = " ".join(sys.argv[1:]) or "RSI is greater than 40!"
#             asyncio.run(send_alert(message))
# bot.callback_msg()
# # context.bot.sendMessage(
# #     chat_id=update.message.chat_id,
# #     reply_to_message_id=update.effective_message.id,
# #     text=msg,
# # )


# # class UpbitAlertTelegramBot:
# #     with open("./token.txt") as f:
# #         lines = f.readlines()
# #         token = lines[0].strip()
# #         chat = lines[1].strip()

# #     TELEGRAM_TOKEN = token
# #     CHAT_ID = chat
# #     bot = telegram.Bot(TELEGRAM_TOKEN)

# #     async def start_commmand(update, context):
# #         await update.message.reply_text("Hello! Welcome To Crypto Alert!")

# #     async def send(chat, msg):
# #         await bot.sendMessage(chat_id=chat, text=msg)

# #     if __name__ == "__main__":
# #         application = Application.builder().token(TELEGRAM_TOKEN).build()

# #         # Commands
# #         application.add_handler(CommandHandler("start", start_commmand))

# #         # Run bot
# #         application.run_polling(1.0)
