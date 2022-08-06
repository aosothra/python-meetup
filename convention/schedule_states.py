from django.template.loader import render_to_string

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import PARSEMODE_HTML
from telegram.ext import CallbackContext

from convention.models import Block, Flow
from python_meetup.state_machine import State, StateMachine


class SchedulePickFlowState(State):
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
                context={"section": "Расписание"},
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
            return SchedulePickBlockState(flow)

    def clean_up(self, update: Update, context: CallbackContext):
        self.message.delete()


class SchedulePickBlockState(State):
    def __init__(self, flow: Flow):
        self.flow = flow

    def display_data(self, chat_id: int, update: Update, context: CallbackContext):
        menu_keyboard = []
        for block in self.flow.blocks.all().order_by("starts_at"):
            time = block.starts_at.strftime("%H:%M")
            menu_keyboard.append(
                [
                    InlineKeyboardButton(
                        f"{time} {block.title}", callback_data=f"{block.id}"
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
                context={"section": "Расписание", "flow": self.flow},
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
            return SchedulePickFlowState()
        else:
            block = Block.objects.get(id=answer)
            return ScheduleShowPresentationsState(self.flow, block)

    def clean_up(self, update: Update, context: CallbackContext):
        self.message.delete()


class ScheduleShowPresentationsState(State):
    def __init__(self, flow: Flow, block: Block):
        self.flow = flow
        self.block = block

    def display_data(self, chat_id: int, update: Update, context: CallbackContext):
        menu_keyboard = [
            [
                InlineKeyboardButton("Назад", callback_data="back"),
                InlineKeyboardButton("Вернуться в меню", callback_data="menu"),
            ]
        ]
        self.message = context.bot.send_message(
            chat_id=chat_id,
            text=render_to_string(
                "show_schedule.html",
                context={
                    "section": "Расписание",
                    "flow": self.flow,
                    "block": self.block,
                    "presentations": self.block.serialize_presentations(),
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
            return SchedulePickBlockState(self.flow)

    def clean_up(self, update: Update, context: CallbackContext):
        self.message.edit_reply_markup()
