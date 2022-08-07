from django.conf import settings
from django.template.loader import render_to_string
from telegram import LabeledPrice, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from telegram.constants import PARSEMODE_HTML

from donate.models import Donate
from python_meetup.state_machine import State, StateMachine


class DonateState(State):
    def display_data(self, chat_id: int, update: Update, context: CallbackContext):
        message = render_to_string("donate_message.html")

        context.bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode=PARSEMODE_HTML,
        )

    def handle_input(self, update: Update, context: CallbackContext):
        if not update.message:
            return None

        answer = update.message.text

        if answer.isdigit() is False:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Вы ввели не число! Пожалуйста, введите целое число.",
            )
            return None

        amount = int(answer)

        if amount < 65 or amount > 1000:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Введите, пожалуйста, сумму от 65 до 1000 рублей.",
            )
        else:
            return PaymentState(int(answer))

    def clean_up(self, update: Update, context: CallbackContext):
        pass


class PaymentState(State):
    def __init__(self, amount: int):
        self.amount = amount

    def display_data(self, chat_id: int, update: Update, context: CallbackContext):
        menu_keyboard = [
            [InlineKeyboardButton("Вернуться в меню", callback_data="menu")]
        ]
        self.message = context.bot.send_message(
            chat_id=chat_id,
            text=render_to_string("donate_details_message.html"),
            parse_mode=PARSEMODE_HTML,
            reply_markup=InlineKeyboardMarkup(menu_keyboard),
        )

        title = "Донат на мероприятие"
        description = "Донат от участника"
        payload = "Custom-Payload"
        provider_token = settings.PAYMENT_BOT_TOKEN
        currency = "rub"
        prices = [LabeledPrice("Донатик", self.amount * 100)]

        self.invoice = context.bot.send_invoice(
            chat_id, title, description, payload, provider_token, currency, prices
        )

    def handle_input(self, update: Update, context: CallbackContext):
        if update.message and update.message.successful_payment:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Платеж прошел, спасибо!",
            )
            Donate.objects.create(
                telegram_id=update.message.chat_id,
                telegram_username=update.message.from_user.username,
                event=context.user_data["present_event"],
                amount=self.amount,
            )
            return StateMachine.INITIAL_STATE

        if update.callback_query and update.callback_query.data == "menu":
            return StateMachine.INITIAL_STATE

        if not (query := update.pre_checkout_query):
            return None

        if query.invoice_payload != "Custom-Payload":
            query.answer(ok=False, error_message="Что-то пошло не так...")
            context.bot.send_message(
                chat_id=query.from_user.id,
                text="Похоже возникла проблема при оплате. Вы можете попробовать еще раз.",
            )
            return StateMachine.INITIAL_STATE
        else:
            query.answer(ok=True)
            context.bot.send_message(
                chat_id=query.from_user.id, text="Обрабатываем Ваш платеж..."
            )

            return None

    def clean_up(self, update: Update, context: CallbackContext):
        self.message.delete()
        self.invoice.delete()
