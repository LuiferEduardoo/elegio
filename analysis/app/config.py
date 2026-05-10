import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


class Settings(BaseModel):
    gemini_api_key: str = Field(..., min_length=1)


settings = Settings(
    gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
)
