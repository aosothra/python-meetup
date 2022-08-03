from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from convention.state_machine import State


class MenuState(State):
    def display_data(self, chat_id: int, update: Update, context: CallbackContext):
        menu_keyboard = [
            [InlineKeyboardButton("Расписание", callback_data="schedule")],
            [InlineKeyboardButton("Вопросы и ответы", callback_data="qa")],
            [InlineKeyboardButton("Нетворкинг", callback_data="networking")],
            [InlineKeyboardButton("Пожертвование", callback_data="donate")],
        ]
        self.message = context.bot.send_message(
            chat_id=chat_id,
            text="Здравствуйте! Это официальный бот по поддержке участников.",
            reply_markup=InlineKeyboardMarkup(menu_keyboard),
        )

    def handle_input(self, update: Update, context: CallbackContext):
        if not update.callback_query:
            return None

        answer = update.callback_query.data
        update.callback_query.answer()
        print(answer)
        if answer == "schedule":
            return SchedulePickEventState()

    def clean_up(self, update: Update, context: CallbackContext):
        self.message.edit_reply_markup()


class SchedulePickEventState(State):
    def display_data(self, chat_id: int, update: Update, context: CallbackContext):
        menu_keyboard = [
            [InlineKeyboardButton("Назад", callback_data="back")],
        ]
        self.message = context.bot.send_message(
            chat_id=chat_id,
            text="Выберите поток мероприятия:",
            reply_markup=InlineKeyboardMarkup(menu_keyboard),
        )

    def handle_input(self, update: Update, context: CallbackContext):
        if not update.callback_query:
            return None

        answer = update.callback_query.data
        update.callback_query.answer()

        if answer == "back":
            return MenuState()

    def clean_up(self, update: Update, context: CallbackContext):
        self.message.delete()
