import telegram
from telegram.ext import *


print("Starting a bot....")


class UpbitAlertTelegramBot:
    with open("./token.txt") as f:
        lines = f.readlines()
        token = lines[0].strip()
        chat = lines[1].strip()

    TELEGRAM_TOKEN = token
    CHAT_ID = chat
    bot = telegram.Bot(TELEGRAM_TOKEN)

    async def start_commmand(update, context):
        await update.message.reply_text("Hello! Welcome To Crypto Alert!")

    async def send(chat, msg):
        await bot.sendMessage(chat_id=chat, text=msg)

    if __name__ == "__main__":
        application = Application.builder().token(TELEGRAM_TOKEN).build()

        # Commands
        application.add_handler(CommandHandler("start", start_commmand))

        # Run bot
        application.run_polling(1.0)
