import re
from typing import Iterable

import anthropic

from src.agent.schemas import StreamEvent
from src.config import SYSTEM_CONFIG

USER_ROLE = "user"
ASSISTANT_ROLE = "assistant"
CONTENT_TAG = "content"


def ends_with_punctuation(sentence):
    pattern = r'[.!?]$'
    return bool(re.search(pattern, sentence))


def get_anthropic_client() -> anthropic.Client:
    """
    Get Anthropi client

    :return:
    """
    return anthropic.Client()


def invoke_anthropic(messages: list[dict]) -> anthropic.types.Message:
    """
    Invoke Anthropi API synchronously

    :param messages:
    :return:
    """

    client = get_anthropic_client()

    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        temperature=0.1,
        system=SYSTEM_CONFIG,
        messages=messages
    )
    return message


def stream_anthropic(
        messages: list[dict]
) -> Iterable[StreamEvent]:
    """
    Invoke Anthropi API asynchronously

    :param messages:
    :return:
    """

    client = get_anthropic_client()

    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        temperature=0.0,
        system=SYSTEM_CONFIG,
        messages=messages,
        stream=True
    )

    block = ""
    running_block = ""

    for response in message:

        if not isinstance(response, anthropic.types.RawContentBlockDeltaEvent):
            continue

        delta = response.delta.text

        block += response.delta.text
        running_block += response.delta.text

        if ends_with_punctuation(delta.strip()):
            yield StreamEvent(
                message=block.strip(),
                delta=running_block.strip()
            )
            running_block = ""


async def astream_anthropic(
        messages: list[dict]
):
    """
    Invoke Anthropi API asynchronously

    :param messages:
    :return:
    """

    client = anthropic.AsyncClient()

    block = ""
    running_block = ""

    async with client.messages.stream(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            temperature=0.0,
            system=SYSTEM_CONFIG,
            messages=messages,
    ) as stream:
        async for response in stream:
            if not isinstance(response,
                              anthropic.types.RawContentBlockDeltaEvent):
                continue

            delta = response.delta.text

            block += response.delta.text
            running_block += response.delta.text

            if ends_with_punctuation(delta.strip()):
                yield StreamEvent(
                    message=block.strip(),
                    delta=running_block.strip()
                )
                running_block = ""
