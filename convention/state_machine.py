from telegram import Update
from telegram.ext import CallbackContext


class State:
    def __init__(self):
        pass

    def display_data(self, chat_id: int, update: Update, context: CallbackContext):
        # Display state message to the user
        # Provide InlineKeyboard if necessary
        pass

    def handle_input(self, update: Update, context: CallbackContext):
        # Process user input and return new states
        # If None returned - keep waiting for valid input
        return None

    def clean_up(self, update: Update, context: CallbackContext):
        # Clean up logic for when state is complete
        # Can be used to update, delete bot messages or keyboards
        pass


class StateMachine:
    def __init__(self, InitialState):
        self.users_state = dict()
        self.InitialState = InitialState

    def handle_message(self, update: Update, context: CallbackContext):
        # Reset state to initial upon /start command regardless of current state
        chat_id = update.effective_chat.id

        if update.message and update.message.text == "/start":
            self.users_state[chat_id] = self.InitialState()
            self.users_state[chat_id].display_data(chat_id, update, context)
            return

        if self.users_state.get(chat_id, None) is None:
            # User must /start to get to initial state
            return

        new_state = self.users_state[chat_id].handle_input(update, context)
        if new_state:
            # Clean up previous state
            self.users_state[chat_id].clean_up(update, context)

            # Set new state and display state message
            self.users_state[chat_id] = new_state
            self.users_state[chat_id].display_data(chat_id, update, context)
