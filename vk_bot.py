import os
import random

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv

from dialogflow_answer import detect_intent_texts


def answer_questions(event, vk_api):
    project_id = os.environ['DIALOG_FLOW_PROJECT_ID']
    language_code = 'ru-RU'
    user_id = event.user_id
    user_question = event.text
    response = detect_intent_texts(
        project_id, user_id,
        user_question, language_code
    )
    if not response.query_result.intent.is_fallback:
        vk_api.messages.send(
            user_id=user_id,
            message=response.query_result.fulfillment_text,
            random_id=random.randint(1, 1000)
        )


if __name__ == '__main__':
    load_dotenv()
    vk_token = os.environ['VK_GROUP_TOKEN']
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            answer_questions(event, vk_api)
