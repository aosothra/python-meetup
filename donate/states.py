from django.conf import settings
from telegram import LabeledPrice, Update
from telegram.ext import CallbackContext

from donate.models import Donate
from python_meetup.state_machine import State, StateMachine


class DonateState(State):
    def display_data(self, chat_id: int, update: Update, context: CallbackContext):
        context.bot.send_message(
            chat_id=chat_id,
            text="Подскажите, на какую сумму в рублях вы хотите выполнить донат?",
        )

    def handle_input(self, update: Update, context: CallbackContext):
        if not update.message:
            return None

        answer = update.message.text

        if answer.isdigit() == True:
            context.user_data["donate"] = int(answer)
            return PaymentState()
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Вы ввели не число! Пожалуйста, введите целое число.",
            )

    def clean_up(self, update: Update, context: CallbackContext):
        pass


class PaymentState(State):
    def display_data(self, chat_id: int, update: Update, context: CallbackContext):
        self.message = context.bot.send_message(
            chat_id=chat_id,
            text="Введите данные.",
        )

        context.user_data["chat_id"] = update.effective_chat.id
        context.user_data["username"] = update.message.chat.username
        chat_id = update.message.chat_id
        title = "Донат на мероприятие"
        description = "Донат от участника"
        payload = "Custom-Payload"
        provider_token = settings.PAYMENT_BOT_TOKEN
        currency = "rub"
        price = context.user_data["donate"]
        prices = [LabeledPrice("Донатик", price * 100)]

        self.invoice = context.bot.send_invoice(
            chat_id, title, description, payload, provider_token, currency, prices
        )

    def handle_input(self, update: Update, context: CallbackContext):
        query = update.pre_checkout_query
        if query.invoice_payload != "Custom-Payload":
            query.answer(ok=False, error_message="Что-то пошло не так...")
            context.bot.send_message(
                chat_id=update.pre_checkout_query.from_user.id,
                text="Похоже возникла проблема при оплате. Вы можете попробовать еще раз.",
            )
        else:
            query.answer(ok=True)
            Donate.objects.create(
                telegram_username=context.user_data["username"],
                amount=context.user_data["donate"],
            )
            context.bot.send_message(
                chat_id=update.pre_checkout_query.from_user.id,
                text="Спасибо за Ваш вклад в наше развитие! Мы всегда рады Вам!",
            )

        return StateMachine.INITIAL_STATE

    def clean_up(self, update: Update, context: CallbackContext):
        self.message.delete()
        self.invoice.delete()
