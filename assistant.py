import os
import datetime
from google import genai
from dotenv import load_dotenv
import base64

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY"),
    http_options={"api_version": "v1"},
)

user_name = None
user_location = None


def gemini_respond(prompt: str) -> str:
    try:
        resp = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[{"role": "user", "parts": [{"text": prompt}]}],
        )
        return resp.text.strip()
    except Exception as e:
        return f"Gemini Error: {e}"



def set_name(name: str) -> str:
    global user_name
    user_name = name

    return gemini_respond(
        f"My name is Gemini. The user's name is {user_name}. "
        f"From now on, respond naturally and personalize replies."
    )


def set_location(location: str) -> str:
    global user_location
    user_location = location

    return gemini_respond(
        f"The user is located in {user_location}. Acknowledge nicely."
    )


def get_time() -> str:
    now = datetime.datetime.now().strftime("%I:%M %p")

    return gemini_respond(
        f"The real time is {now}. Answer the user clearly with the current time."
    )


def get_weather() -> str:
    global user_location

    if not user_location:
        return "Please tell me where you're from first."

    return gemini_respond(
        f"Provide the current real-world weather for {user_location}. "
        f"Be factual and concise."
    )


def get_greeting() -> str:
    hour = datetime.datetime.now().hour
    tod = "morning" if hour < 12 else "afternoon" if hour < 18 else "evening"
    who = user_name or "my friend"

    return gemini_respond(
        f"Give a warm {tod} greeting to {who}."
    )

def analyze_image(image_path: str) -> None:
    """Analyze a real image file."""
    if not os.path.exists(image_path):
        print(f"Could not find image '{image_path}'.")
        return

    mime = "image/png" if image_path.lower().endswith(".png") else "image/jpeg"

    with open(image_path, "rb") as f:
        img_bytes = f.read()

    try:
        resp = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                {
                    "role": "user",
                    "parts": [
                        {"text": "Describe this image in detail."},
                        {"inline_data": {"mime_type": mime, "data": img_bytes}},
                    ],
                }
            ],
        )
        print("Gemini says:\n", resp.text)
    except Exception as e:
        print(f"Error analyzing image: {e}")


def describe_image_prompt(prompt: str) -> str:
    return gemini_respond(
        f"Describe in vivid detail what an image like this WOULD look like: {prompt}"
    )


def main() -> None:
    name = input("Hi! My name is Gemini, what is yours? ").strip()
    print(set_name(name))
    print("Ask me the time, weather, say hi, or ask me to analyze/describe an image!")

    while True:
        raw_input_text = input("\nWhat would you like me to do? ").strip()
        command = raw_input_text.lower()

        if command in ("bye", "exit", "quit"):
            print("Goodbye! Have a great day!")
            break

        # Location change
        if "from" in command:
            parts = command.split("from", 1)
            if len(parts) > 1:
                location = parts[1].strip()
                print(set_location(location))
            else:
                print("Please specify a location (e.g., 'I'm from Athens').")
            continue

        # Time
        if "time" in command:
            print(get_time())
            continue

        # Weather
        if "weather" in command:
            print(get_weather())
            continue

        # Greetings
        if command in ["hi", "hello", "hey", "yo", "sup"]:
            print(get_greeting())
            continue

        # Image commands
        if "image" in command:
            if "analyze" in command:
                image = input("Name of the image file to analyze: ")
                analyze_image(image)
                continue
            elif "describe" in command or "generate" in command:
                prompt = input("Describe the image you want me to describe: ")
                print(describe_image_prompt(prompt))
                continue
            else:
                print("Try 'analyze image' or 'describe image'.")
                continue
        print(gemini_respond(f"The user said: '{raw_input_text}'. Respond naturally."))


if __name__ == "__main__":
    main()
