from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from convention.models import Attendee, Event

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
        chat_id = update.effective_chat.id

        if not update.callback_query:
            return None

        answer = update.callback_query.data
        update.callback_query.answer()

        if answer == "schedule":
            return SchedulePickEventState()
        elif answer == "networking":
            attendee, new = Attendee.objects.get_or_create(telegram_id=chat_id)
            if new or attendee.is_anonymous():
                return SignupNameState()

    def clean_up(self, update: Update, context: CallbackContext):
        self.message.edit_reply_markup()


class SignupNameState(State):
    def display_data(self, chat_id: int, update: Update, context: CallbackContext):
        context.bot.send_message(
            chat_id=chat_id,
            text='Похоже что мы с Вами еще не знакомы. Скажите, пожалуйста, как Вас зовут ("Имя Фамилия"):',
        )

    def handle_input(self, update: Update, context: CallbackContext):
        if not update.message:
            return None

        answer = update.message.text
        firstname, lastname = answer.split(" ", 1)
        context.user_data["firstname"] = firstname
        context.user_data["lastname"] = lastname

        return SignupCompanyState()


class SignupCompanyState(State):
    def display_data(self, chat_id: int, update: Update, context: CallbackContext):
        firstname = context.user_data["firstname"]
        lastname = context.user_data["lastname"]
        context.bot.send_message(
            chat_id=chat_id,
            text=f"Приятно познакомиться, {firstname} {lastname}. Скажите, пожалуйста, где Вы работаете?",
        )

    def handle_input(self, update: Update, context: CallbackContext):
        if not update.message:
            return None

        answer = update.message.text
        context.user_data["company"] = answer
        return SignupPositionState()


class SignupPositionState(State):
    def display_data(self, chat_id: int, update: Update, context: CallbackContext):
        self.message = context.bot.send_message(
            chat_id=chat_id,
            text="Скажите, пожалуйста, какая у Вас должность в компании?",
        )

    def handle_input(self, update: Update, context: CallbackContext):
        if not update.message:
            return None

        answer = update.message.text
        context.user_data["position"] = answer
        return SignupConfirmState()


class SignupConfirmState(State):
    def display_data(self, chat_id: int, update: Update, context: CallbackContext):
        firstname = context.user_data["firstname"]
        lastname = context.user_data["lastname"]
        company = context.user_data["company"]
        position = context.user_data["position"]
        message_text = (
            "Пожалуйста проверьте анкету, убедитесь что все верно:"
            f"\n{firstname} {lastname}\n{position}\n{company}"
        )

        menu_keyboard = [
            [InlineKeyboardButton("Подтвердить", callback_data="confirm")],
            [InlineKeyboardButton("Отменить", callback_data="cancel")],
        ]

        self.message = context.bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=InlineKeyboardMarkup(menu_keyboard),
        )

    def handle_input(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id

        if not update.callback_query:
            return None

        answer = update.callback_query.data
        if answer == "confirm":
            telegram_username = update.callback_query.from_user.username
            attendee = Attendee.objects.get(telegram_id=chat_id)
            attendee.firstname = context.user_data["firstname"]
            attendee.lastname = context.user_data["lastname"]
            attendee.company = context.user_data["company"]
            attendee.position = context.user_data["position"]
            attendee.telegram_username = telegram_username
            attendee.save()

            context.bot.send_message(
                chat_id=chat_id,
                text="Отлично! Теперь мы сможем познакомиться с другими участниками.",
            )
        else:
            context.bot.send_message(
                chat_id=chat_id, text="Ничего страшного, мы можем попробовать снова."
            )
        return MenuState()

    def clean_up(self, update: Update, context: CallbackContext):
        self.message.delete()
        context.user_data.pop("firstname", None)
        context.user_data.pop("lastname", None)
        context.user_data.pop("company", None)
        context.user_data.pop("position", None)


class SchedulePickEventState(State):
    def display_data(self, chat_id: int, update: Update, context: CallbackContext):
        # FIXME: выбирать мероприятия динамически
        event = Event.objects.get(pk=1)
        menu_keyboard = [
            [InlineKeyboardButton(flow.title, callback_data=f"flow{flow.id}")]
            for flow in event.flows.all()
        ]
        menu_keyboard.append([InlineKeyboardButton("Назад", callback_data="back")])
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
