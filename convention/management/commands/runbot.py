from django.core.management import BaseCommand
from django.conf import settings
from telegram.ext import (
    Updater,
    CallbackQueryHandler,
    MessageHandler,
    CommandHandler,
    Filters,
)

from convention.states import MenuState
from python_meetup.state_machine import StateMachine


class Command(BaseCommand):
    def handle(self, *args, **options):
        token = settings.BOT_TOKEN

        state_machine = StateMachine(MenuState)

        updater = Updater(token)
        dispatcher = updater.dispatcher
        dispatcher.add_handler(CallbackQueryHandler(state_machine.handle_message))
        dispatcher.add_handler(
            MessageHandler(Filters.text, state_machine.handle_message)
        )
        dispatcher.add_handler(CommandHandler("start", state_machine.handle_message))
        updater.start_polling()
        updater.idle()
