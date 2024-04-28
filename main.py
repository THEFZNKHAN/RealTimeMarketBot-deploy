import os
from typing import Final
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import logging

load_dotenv()

# Constants
BOT_USERNAME: Final = os.getenv("BOT_NAME")

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# START COMMAND
async def start_cmd(update: Update, context):
    await update.message.reply_text(f"Welcome to the {BOT_USERNAME}!")

# HANDLE MESSAGE OF THE USER
async def handle_message(update: Update, context):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    logger.info("User (%s) in %s: '%s'", update.message.chat.id, message_type, text)

    if message_type == "group":
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            song_id: str = search_id(new_text)
            response: str = await get_data(song_id)
            logger.info('Bot: %s', response)
            await update.message.reply_text(response)
        return

    song_id: str = search_id(text)
    response: str = await get_data(song_id)
    logger.info('Bot: %s', response)
    await update.message.reply_text(response)

# ERROR
async def error(update: Update, context):
    logger.error("Update %s caused error %s", update, context.error)

# MAIN
if __name__ == '__main__':
    TOKEN: Final = os.getenv("BOT_TOKEN")

    logger.info("Bot is starting...")

    app = Application.builder().token(TOKEN).build()

    # COMMANDS
    app.add_handler(CommandHandler("start", start_cmd))

    # MESSAGES
    # app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # ERROR
    app.add_error_handler(error)

    # POLLING
    logger.info("Polling...")
    app.run_polling(poll_interval=3)