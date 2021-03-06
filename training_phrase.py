import argparse
import os
import json
import logging

from dotenv import load_dotenv
from google.cloud import dialogflow

logger = logging.getLogger(__name__)


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(
            text=training_phrases_part
        )
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)
    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)
    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases,
        messages=[message]
    )
    intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )




def get_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--json_path',
        help='Указать свой путь к *.json файлу с данными.',
        default='phrase.json'
    )
    return parser


if __name__ == '__main__':
    load_dotenv()
    logging.basicConfig(level=logging.ERROR)
    logger.setLevel(logging.DEBUG)
    parser = get_parser()
    args = parser.parse_args()
    training_phrase = args.json_path

    with open(training_phrase, 'r') as my_file:
        intents = json.load(my_file)
        for intent in intents:
            training_phrases = intents[intent]['questions']
            message_answer = [intents[intent]['answer']]
            project_id = os.environ['DIALOG_FLOW_PROJECT_ID']
            create_intent(project_id, intent, training_phrases, message_answer)

