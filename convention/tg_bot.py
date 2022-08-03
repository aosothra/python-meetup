from django.conf import settings
from telegram import Update
from telegram.ext import (
    Updater,
    CallbackQueryHandler,
    MessageHandler,
    CommandHandler,
    Filters,
    CallbackContext,
)


def handle(update: Update, context: CallbackContext):
    pass


def start_bot():
    token = settings.BOT_TOKEN
    updater = Updater(token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CallbackQueryHandler(handle))
    dispatcher.add_handler(MessageHandler(Filters.text, handle))
    dispatcher.add_handler(CommandHandler("start", handle))
    updater.start_polling()
    updater.idle()
