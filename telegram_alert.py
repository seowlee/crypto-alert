import logging
import asyncio
from telegram import ForceReply, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

with open("./token.txt") as f:
    lines = f.readlines()
    token = lines[0].strip()
    chat = lines[1].strip()

TELEGRAM_TOKEN = token
CHAT_ID = chat


class UpbitAlertTelegramBot:
    def __init__(self):
        self.token = TELEGRAM_TOKEN
        self.chat_id = CHAT_ID
        self.app, self.bot, self.updater, self.loop = self._build_application()
        self.telegram_thread = None

        print("Bot initialized...")

    def _build_application(self):
        loop = asyncio.new_event_loop()
        builder = Application.builder().token(self.token)
        app = builder.build()
        return app, app.bot, app.updater, loop

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /start is issued."""
        user = update.effective_user
        await update.message.reply_html(
            rf"Hi {user.mention_html()}!",
            reply_markup=ForceReply(selective=True),
        )

    async def help_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Send a message when the command /help is issued."""
        await update.message.reply_text("Help!")

    async def echo(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Echo the user message."""
        await update.message.reply_text(update.message.text)

    async def send_msg(self, message: str) -> None:
        """Echo the user message."""
        await update.message.reply_text({message})

    # def echo(self, message: str) -> None:
    #     """Echo the message."""
    #     # You can replace the following print statement with your logic to send the message
    #     print(f"Echo: {message}")

    def main(self) -> None:
        """Start the bot."""
        self.app.add_handler(CommandHandler(command="start", callback=self.start))
        self.app.add_handler(CommandHandler(command="help", callback=self.help_command))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.echo))
        # Run the bot until the user presses Ctrl-C
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    # Create an instance of the UpbitAlertTelegramBot class
    bot_instance = UpbitAlertTelegramBot()
    # Call the main method to start the bot
    bot_instance.main()


# class UpbitAlertTelegramBot:
#     with open("./token.txt") as f:
#         lines = f.readlines()
#         token = lines[0].strip()
#         chat = lines[1].strip()

#     TELEGRAM_TOKEN = token
#     CHAT_ID = chat
#     bot = telegram.Bot(TELEGRAM_TOKEN)

#     async def start_commmand(update, context):
#         await update.message.reply_text("Hello! Welcome To Crypto Alert!")

#     async def send(chat, msg):
#         await bot.sendMessage(chat_id=chat, text=msg)

#     if __name__ == "__main__":
#         application = Application.builder().token(TELEGRAM_TOKEN).build()

#         # Commands
#         application.add_handler(CommandHandler("start", start_commmand))

#         # Run bot
#         application.run_polling(1.0)
