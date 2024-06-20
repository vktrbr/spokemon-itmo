import asyncio
import base64
import json
import subprocess

import websockets
from elevenlabs import stream
from elevenlabs.client import ElevenLabs
from loguru import logger

from src.config import ELEVENLABS_API_KEY

VOICE_ID = "Dvfxihpdb69LFIkmih0k"
MODEL = "eleven_multilingual_v2"


def get_elevenlabs_client() -> ElevenLabs:
    """
    Get ElevenLabs client
    :return:
    """
    return ElevenLabs(api_key=ELEVENLABS_API_KEY)


class ElevenClient:

    def __init__(self, api_key=ELEVENLABS_API_KEY):
        self.client = ElevenLabs(api_key=api_key)

    def stream(self, message) -> bool:
        """
        Invoke ElevenLabs API asynchronously

        :param message:
        :return:
        """
        audio = self.client.generate(
            text=message,
            voice=VOICE_ID,
            model=MODEL
        )

        stream(audio)

        # TODO: Сделать прирывание потока
        # while stream_with_yeild(audio):
        #     yield True

        return False


async def astream(audio_stream):
    """Stream audio data using mpv player."""

    mpv_process = subprocess.Popen(
        ["mpv", "--no-cache", "--no-terminal", "--", "fd://0"],
        stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    print("Started streaming audio")
    async for chunk in audio_stream:
        if chunk:
            mpv_process.stdin.write(chunk)
            mpv_process.stdin.flush()

    if mpv_process.stdin:
        mpv_process.stdin.close()
    mpv_process.wait()


async def text_to_speech_input_streaming(text_iterator):
    """
    Stream text to speech input

    :param text_iterator:
    :return:
    """
    uri = (f"wss://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/"
           f"stream-input?model_id={MODEL}")

    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({
            "text": " ",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.8},
            "xi_api_key": ELEVENLABS_API_KEY,
        }))

        async def listen():
            """Listen to the websocket for audio data and stream it."""
            while True:
                try:
                    message = await websocket.recv()
                    data = json.loads(message)
                    if data.get("audio"):
                        yield base64.b64decode(data["audio"])
                    elif data.get('isFinal'):
                        break
                except websockets.exceptions.ConnectionClosed:
                    # TODO: Отваливается коннект – надо чинить
                    #  websockets.exceptions.ConnectionClosedError:
                    #  received 1008 (policy violation) Unusual activity
                    #  detected. Free Tier usage disabled. If you are
                    #  using a proxy/VPN you might need to purchase a Paid
                    #  Plan; then sent 1008 (policy violation)
                    #  Unusual activity detected. Free Tier usage disabled.
                    #  If you are using a proxy/VPN you might need to
                    #  purchase a Paid Plan
                    print("Connection closed")
                    break

        listen_task = asyncio.create_task(astream(listen()))

        for text in text_iterator:
            text = text.delta
            res = await websocket.send(
                json.dumps({"text": text, "try_trigger_generation": True})
            )

            logger.info(f"Sent text: {text}")
            logger.info(f"Received response: {res}")

        await websocket.send(json.dumps({"text": ""}))

        await listen_task
