import subprocess
from random import randint

from src.config import EMOTIONS_DIR

EMOTION_LIST = [
    "mintimer_couple_of_seconds.mp3",
    "mintimer_hmm.mp3",
    "mintimer_intersting.mp3",
    "mintimer_ok.mp3"
]


def speak_random_emotion():
    mpv_command = ["mpv", "--no-cache", "--no-terminal", "--", "fd://0"]
    mpv_process = subprocess.Popen(
        mpv_command,
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    emotion = EMOTION_LIST[randint(0, len(EMOTION_LIST) - 1)]

    with open(f"{EMOTIONS_DIR}/{emotion}", "rb") as f:
        for chunk in iter(lambda: f.read(1024), b""):
            mpv_process.stdin.write(chunk)  # type: ignore
            mpv_process.stdin.flush()  # type: ignore

    if mpv_process.stdin:
        mpv_process.stdin.close()
    mpv_process.wait()
