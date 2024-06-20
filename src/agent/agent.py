from loguru import logger

from src.agent.history import VanillaHistory
from src.agent.schemas import Message
from src.agent.text_to_text import invoke_anthropic


class Agent:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.history = VanillaHistory()

    def process(self, message: str) -> Message:

        logger.info(f"{message=}")
        if self.history.data and self.history.get()[-1].role == "user":
            self.history.data[-1].content += f"\n{message}"
            logger.info(f"Update last message")
        else:
            self.history.add(Message(role="user", content=message))
            logger.info(f"Add new message")

        messages = [j.model_dump() for j in self.history.get()]
        logger.info(f"{messages=}")
        response = invoke_anthropic(messages)
        response = Message(role="assistant", content=response.content[-1].text)
        self.history.add(response)
        return response

    def process_stream(self, message: Message) -> str:
        # TODO: Implement this method
        raise NotImplementedError
