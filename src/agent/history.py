from src.agent.schemas import Message


class VanillaHistory:
    def __init__(self, max_len: int = 128):
        self.max_len = max_len
        self.data: list[Message] = []

    def add(self, item: Message) -> bool:
        """
        Append item to history
        :param item:
        :return:
        """
        self.data.append(item)
        if len(self.data) > self.max_len:
            self.data.pop(0)

        return True

    def get(self) -> list[Message]:
        """
        Get history prompt
        :return:
        """
        return self.data

    def clear(self):
        self.data = []
