from dotenv import load_dotenv
from google import genai
from google.genai import types
import os


def main():
    load_dotenv()
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    model = "gemini-2.5-flash"
    response = client.models.generate_content(
        model=model,
        contents="Hello, world!",
    )
    print(response.text)


if __name__ == "__main__":
    main()
