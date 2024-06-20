from datetime import datetime

from pywhispercpp.examples.assistant import Assistant

from src.config import N_THREADS, LANGUAGE, MODEL
from src.db import save_transcription


def handle_transcription(transcription: str, session_id: str) -> None:
    """
    Handle whisper transcription

    :param transcription:
    :return:
    """

    dtime_at = datetime.now().isoformat()

    save_transcription(
        session_id=session_id,
        dtime_at=dtime_at,
        transcription=transcription
    )

    print(f"Saved: {transcription}")


def set_assistant(session_id: str) -> Assistant:
    """
    Set whisper assistant

    :param session_id:
    :return:
    """
    assistant = Assistant(
        commands_callback=lambda t: handle_transcription(t, session_id),
        n_threads=N_THREADS,
        language=LANGUAGE,
        model=MODEL
    )
    return assistant
