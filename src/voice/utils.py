import shutil
import subprocess
from typing import Iterator


def is_installed(lib_name: str) -> bool:
    lib = shutil.which(lib_name)
    if lib is None:
        return False
    return True


def stream_with_yeild(audio_stream: Iterator[bytes]) -> None:
    """
    Stream audio data using mpv player.
    :param audio_stream:
    :return:
    """
    if not is_installed("mpv"):
        message = (
            "mpv not found, necessary to stream audio. "
            "On mac you can install it with 'brew install mpv'. "
            "On linux and windows you can install it from https://mpv.io/"
        )
        raise ValueError(message)

    mpv_command = ["mpv", "--no-cache", "--no-terminal", "--", "fd://0"]
    mpv_process = subprocess.Popen(
        mpv_command,
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    for chunk in audio_stream:
        if chunk is not None:
            mpv_process.stdin.write(chunk)  # type: ignore
            mpv_process.stdin.flush()  # type: ignore
            yield True

    if mpv_process.stdin:
        mpv_process.stdin.close()
    mpv_process.wait()

    yield False
