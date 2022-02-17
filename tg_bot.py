import os
import logging

from dotenv import load_dotenv
from telegram import Update, ForceReply
from telegram.ext import (
    Updater, CommandHandler,
    MessageHandler, Filters,
    CallbackContext
)

from dialogflow_answer import detect_intent_texts


logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Приветствую {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext):
    update.message.reply_text('Help!')


def answer_questions(update: Update, context: CallbackContext):
    project_id = os.environ['DIALOG_FLOW_PROJECT_ID']
    language_code = 'ru-RU'
    user_id = update.effective_user.id
    user_question = update.message.text
    response = detect_intent_texts(
        project_id, user_id,
        user_question, language_code
    )
    update.message.reply_text(response.query_result.fulfillment_text)


if __name__ == '__main__':
    load_dotenv()
    credentials_path = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
    bot_token = os.environ['TG_BOT_TOKEN']
    logging.basicConfig(level=logging.ERROR)
    logger.setLevel(logging.DEBUG)
    try:
        updater = Updater(bot_token)
        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CommandHandler("help", help_command))
        dispatcher.add_handler(
            MessageHandler(Filters.text & ~Filters.command, answer_questions)
        )
        updater.start_polling()
        updater.idle()
    except Exception as error:
        logger.exception(error)
