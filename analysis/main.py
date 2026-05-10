from google import genai

from app.config import settings


def main() -> None:
    client = genai.Client(api_key=settings.gemini_api_key)
    print("Analysis project ready. Gemini client initialized.")
    print(f"Available models: {[m.name for m in client.models.list()][:3]}")


if __name__ == "__main__":
    main()
