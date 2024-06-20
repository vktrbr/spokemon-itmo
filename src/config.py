import os

import dotenv

dotenv.load_dotenv()

FILE_TRANSCRIPTIONS = os.getenv("FILE_TRANSCRIPTIONS")
EMOTIONS_DIR = os.getenv("EMOTIONS_DIR")

N_THREADS = int(os.getenv("N_THREADS"))
LANGUAGE = os.getenv("LANGUAGE")
MODEL = os.getenv("MODEL")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
LLM_SYSTEM_CONFIG = os.getenv("LLM_SYSTEM_CONFIG")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")


with open(LLM_SYSTEM_CONFIG) as con:
    SYSTEM_CONFIG = con.read()
