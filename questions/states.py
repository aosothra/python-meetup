from django.template.loader import render_to_string

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import PARSEMODE_HTML
from telegram.ext import CallbackContext

from convention.models import Attendee, Flow, Block, Presentation
from python_meetup.state_machine import State, StateMachine
from questions.models import Question


class AnswerMenuState(State):
    def __init__(self, question: Question):
        self.current_question = question

    def display_data(self, chat_id: int, update: Update, context: CallbackContext):
        event = context.user_data["present_event"]

        if not self.current_question:
            menu_keyboard = [
                [InlineKeyboardButton("Вернуться в меню", callback_data="menu")]
            ]
            self.message = context.bot.send_message(
                chat_id=chat_id,
                text="Похоже у Вас больше нет открытых вопросов.",
                reply_markup=InlineKeyboardMarkup(menu_keyboard),
            )
            return

        self.next_question = (
            Question.objects.new(chat_id, event)
            .filter(id__gt=self.current_question.id)
            .order_by("id")
            .first()
        )

        if not self.next_question:
            self.next_question = (
                Question.objects.new(chat_id, event).order_by("id").first()
            )

        self.next_question = (
            self.next_question if self.next_question != self.current_question else None
        )

        menu_keyboard = [InlineKeyboardButton("Скрыть вопрос", callback_data="hide")]
        if self.next_question:
            menu_keyboard.append(
                InlineKeyboardButton("Следующий вопрос", callback_data="next")
            )
        menu_keyboard = [
            menu_keyboard,
            [InlineKeyboardButton("Вернуться в меню", callback_data="menu")],
        ]

        self.message = context.bot.send_message(
            chat_id=chat_id,
            text=render_to_string(
                "show_question.html",
                context={"question": self.current_question},
            ),
            parse_mode=PARSEMODE_HTML,
            reply_markup=InlineKeyboardMarkup(menu_keyboard),
        )

    def handle_input(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id

        if update.callback_query:
            self.save_message = False
            if update.callback_query.data == "menu":
                return StateMachine.INITIAL_STATE
            elif update.callback_query.data == "next":
                return AnswerMenuState(self.next_question)
            elif update.callback_query.data == "hide":
                self.current_question.is_ignored = True
                self.current_question.save()
                return AnswerMenuState(self.next_question)
        elif update.message:
            self.save_message = True
            answer_text = update.message.text

            self.current_question.answer_text = answer_text
            self.current_question.save()

            context.bot.send_message(
                chat_id=chat_id,
                text="Спасибо больше за Ваш ответ!",
            )
            return AnswerMenuState(self.next_question)

        return None

    def clean_up(self, update: Update, context: CallbackContext):
        if self.save_message:
            self.message.edit_reply_markup()
        else:
            self.message.delete()


class QuestionsPickFlowState(State):
    def display_data(self, chat_id: int, update: Update, context: CallbackContext):
        event = context.user_data["present_event"]
        menu_keyboard = [
            [InlineKeyboardButton(flow.title, callback_data=f"{flow.id}")]
            for flow in event.flows.all()
        ]
        menu_keyboard.append(
            [InlineKeyboardButton("Вернуться в меню", callback_data="back")]
        )
        self.message = context.bot.send_message(
            chat_id=chat_id,
            text=render_to_string(
                "pick_flow.html",
                context={"section": "Задать вопрос Спикеру"},
            ),
            parse_mode=PARSEMODE_HTML,
            reply_markup=InlineKeyboardMarkup(menu_keyboard),
        )

    def handle_input(self, update: Update, context: CallbackContext):
        if not update.callback_query:
            return None

        answer = update.callback_query.data
        update.callback_query.answer()

        if answer == "back":
            return StateMachine.INITIAL_STATE
        else:
            flow = Flow.objects.get(id=answer)
            return QuestionsPickBlockState(flow)

    def clean_up(self, update: Update, context: CallbackContext):
        self.message.delete()


class QuestionsPickBlockState(State):
    def __init__(self, flow: Flow):
        self.flow = flow

    def display_data(self, chat_id: int, update: Update, context: CallbackContext):
        menu_keyboard = []
        for block in (
            Block.objects.filter(presentations__isnull=False, flow=self.flow)
            .distinct()
            .order_by("starts_at")
        ):
            time_start = block.starts_at.strftime("%H:%M")
            time_end = block.ends_at.strftime("%H:%M")
            menu_keyboard.append(
                [
                    InlineKeyboardButton(
                        f"{time_start} - {time_end} {block.title}",
                        callback_data=f"{block.id}",
                    )
                ]
            )

        menu_keyboard.append(
            [
                InlineKeyboardButton("Назад", callback_data="back"),
                InlineKeyboardButton("Вернуться в меню", callback_data="menu"),
            ]
        )
        self.message = context.bot.send_message(
            chat_id=chat_id,
            text=render_to_string(
                "pick_block.html",
                context={"section": "Задать вопрос Спикеру", "flow": self.flow},
            ),
            parse_mode=PARSEMODE_HTML,
            reply_markup=InlineKeyboardMarkup(menu_keyboard),
        )

    def handle_input(self, update: Update, context: CallbackContext):
        if not update.callback_query:
            return None

        answer = update.callback_query.data
        update.callback_query.answer()

        if answer == "menu":
            return StateMachine.INITIAL_STATE
        elif answer == "back":
            return QuestionsPickFlowState()
        else:
            block = Block.objects.get(id=answer)
            return QuestionsPickSpeakerState(self.flow, block)

    def clean_up(self, update: Update, context: CallbackContext):
        self.message.delete()


class QuestionsPickSpeakerState(State):
    def __init__(self, flow: Flow, block: Block):
        self.flow = flow
        self.block = block

    def display_data(self, chat_id: int, update: Update, context: CallbackContext):
        presentations = self.block.serialize_presentations()
        speakers = []
        for presentation in presentations:
            for speaker in presentation["speakers"]:
                speakers.append(speaker)

        menu_keyboard = [
            [
                InlineKeyboardButton(
                    f"{speaker['name']}",
                    callback_data=f"{speaker['id']}",
                )
            ]
            for speaker in speakers
        ]

        menu_keyboard.append(
            [
                InlineKeyboardButton("Назад", callback_data="back"),
                InlineKeyboardButton("Вернуться в меню", callback_data="menu"),
            ]
        )
        self.message = context.bot.send_message(
            chat_id=chat_id,
            text=render_to_string(
                "show_speakers.html",
                context={
                    "section": "Задать вопрос Спикеру",
                    "flow": self.flow,
                    "block": self.block,
                    "presentations": presentations,
                },
            ),
            parse_mode=PARSEMODE_HTML,
            reply_markup=InlineKeyboardMarkup(menu_keyboard),
        )

    def handle_input(self, update: Update, context: CallbackContext):
        if not update.callback_query:
            return None

        answer = update.callback_query.data
        update.callback_query.answer()

        if answer == "menu":
            return StateMachine.INITIAL_STATE
        elif answer == "back":
            return QuestionsPickBlockState(self.flow)
        else:
            speaker = Attendee.objects.get(id=answer)
            return QuestionsAskFormState(speaker)

    def clean_up(self, update: Update, context: CallbackContext):
        self.message.delete()


class QuestionsAskFormState(State):
    def __init__(self, speaker: Attendee):
        self.speaker = speaker

    def display_data(self, chat_id: int, update: Update, context: CallbackContext):
        menu_keyboard = [
            [InlineKeyboardButton("Вернуться в меню", callback_data="menu")]
        ]
        self.message = context.bot.send_message(
            chat_id=chat_id,
            text=render_to_string(
                "show_question_form.html",
                context={
                    "speaker": self.speaker,
                },
            ),
            parse_mode=PARSEMODE_HTML,
            reply_markup=InlineKeyboardMarkup(menu_keyboard),
        )

    def handle_input(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id

        if update.callback_query:
            self.save_message = False
            if update.callback_query.data == "menu":
                return StateMachine.INITIAL_STATE
            return None
        elif update.message:
            self.save_message = True
            question_text = update.message.text

            author = Attendee.objects.get(
                telegram_id=chat_id, event=context.user_data["present_event"]
            )

            Question.objects.create(
                author=author, recipient=self.speaker, question_text=question_text
            )

            context.bot.send_message(
                chat_id=chat_id,
                text="Спасибо за Ваш вопрос!",
            )
            return StateMachine.INITIAL_STATE

        return None

    def clean_up(self, update: Update, context: CallbackContext):
        if self.save_message:
            self.message.edit_reply_markup()
        else:
            self.message.delete()
