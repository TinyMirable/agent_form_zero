import os
from pathlib import Path
from dotenv import load_dotenv

_ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=_ENV_PATH, override=False)


class Config:
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", None)
