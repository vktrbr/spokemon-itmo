from loguru import logger

from src.config import FILE_TRANSCRIPTIONS


def save_transcription(
        session_id: str,
        dtime_at: str,
        transcription: str
) -> bool:
    """
    Save whisper transcription to the "database"

    :param session_id:
    :param dtime_at:
    :param transcription:
    :return:
    """
    try:
        with open(FILE_TRANSCRIPTIONS, "a") as f:
            f.write(
                f"{session_id}\t{dtime_at}\t{transcription}\n"
            )

        return True

    except Exception as e:
        logger.error(f"Error saving transcription: {e}")
        return False


def load_transcriptions(session_id: str) -> list:
    """
    Load transcriptions for the session

    :param session_id:
    :return:
    """
    try:
        with open(FILE_TRANSCRIPTIONS, "r") as f:
            lines = f.readlines()

        return [
            line.strip().split("\t") for line in lines if
            line.startswith(session_id)
        ]

    except Exception as e:
        logger.error(f"Error loading transcriptions: {e}")
        return []
