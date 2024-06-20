from pydantic import BaseModel


class Message(BaseModel):
    """
    Message class to store message and metadata
    """
    role: str
    content: str


class StreamEvent(BaseModel):
    message: str
    delta: str
