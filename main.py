from dotenv import load_dotenv
from google import genai
from google.genai import types
import json
import os


def main():
    load_dotenv()
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    model = "gemini-2.5-flash"

    prompt = "What are the best Italian restaurants within a 15-minute walk from here?"

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_maps=types.GoogleMaps(enable_widget=True))],
            tool_config=types.ToolConfig(
                retrieval_config=types.RetrievalConfig(
                    lat_lng=types.LatLng(
                        latitude=28.5494,  # Baldwin Park, Orlando, FL
                        longitude=-81.3295,
                    )
                )
            ),
        ),
    )

    # Write full response to JSON file
    with open("response.json", "w") as f:
        f.write(response.model_dump_json(indent=2))
    print("Response written to response.json")

    print("=" * 60)
    print("PROMPT:", prompt)
    print("=" * 60)
    print("\nGENERATED RESPONSE:")
    print(response.text)

    if grounding := response.candidates[0].grounding_metadata:
        if grounding.grounding_chunks:
            print("\n" + "-" * 40)
            print("SOURCES:")
            for chunk in grounding.grounding_chunks:
                print(f"  - [{chunk.maps.title}]({chunk.maps.uri})")


if __name__ == "__main__":
    main()
