import asyncio
from time import sleep
from uuid import uuid4

from loguru import logger

from src.agent.agent import Agent
from src.db import load_transcriptions
from src.voice.emotion_filler import speak_random_emotion
from src.voice.text_to_speech import ElevenClient


async def run_listener(session_id: str):
    """
    Run listener in subprocess asynchronously

    :param session_id:
    :return:
    """

    _ = await asyncio.create_subprocess_exec(
        "python", "src/listener.py", "--session_id", session_id,
    )


def main():
    s_id = str(uuid4())
    agent = Agent(session_id=s_id)
    messages_cnt = 0
    client = ElevenClient()

    asyncio.run(run_listener(s_id))

    while True:

        user_speeches = load_transcriptions(s_id)
        user_speeches = [x for x in user_speeches if "[музыка]" not in x[2]]
        logger.info(f"{user_speeches=}")

        if len(user_speeches) > messages_cnt:
            user_speeches = sorted(user_speeches, key=lambda x: x[1])

            message = '\n'.join([x[2] for x in user_speeches[messages_cnt:]])

            if messages_cnt > 0:
                speak_random_emotion()

            response = agent.process(message)
            logger.info(f"{response=}")

            while client.stream(response.content):
                logger.info("Stream is in progress")
                sleep(1)

            messages_cnt = len(user_speeches)

        sleep(1)
