import os
import logging

from dotenv import load_dotenv
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from dialogflow_answer import detect_intent_texts


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)



def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Приветствую {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext):
    """Echo the user message."""
    project_id = os.environ['DIALOG_FLOW_PROJECT_ID']
    language_code = 'ru-RU'
    user_id = update.effective_user.id
    user_answer = update.message.text
    dialogflow_answer = detect_intent_texts(project_id, user_id, user_answer, language_code)
    update.message.reply_text(dialogflow_answer)


def main():
    """Start the bot."""
    load_dotenv()
    credentials_path = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
    bot_token = os.environ['TG_BOT_TOKEN']
    updater = Updater(bot_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

