import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


class Settings(BaseModel):
    gemini_api_key: str = Field(..., min_length=1)
    database_url: str = Field(..., min_length=1)
    qdrant_url: str = Field(..., min_length=1)
    qdrant_api_key: str = ""
    openai_api_key: str = ""
    hf_token: str = ""


settings = Settings(
    gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
    database_url=os.getenv("DATABASE_URL", ""),
    qdrant_url=os.getenv("QDRANT_URL", ""),
    qdrant_api_key=os.getenv("QDRANT_API_KEY", ""),
    openai_api_key=os.getenv("OPENAI_API_KEY", ""),
    hf_token=os.getenv("HF_TOKEN", ""),
)
