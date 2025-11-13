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
        f"My name is Gemini, and the user's name is {user_name}. Respond naturally."
    )


def set_location(location: str) -> str:
    global user_location
    user_location = location
    return gemini_respond(
        f"The user's location is {user_location}. Acknowledge this nicely."
    )


def get_time() -> str:
    now = datetime.datetime.now().strftime("%I:%M %p")
    return gemini_respond(
        f"The current time is {now}. Respond like a friendly assistant."
    )


def get_weather() -> str:
    global user_location
    if not user_location:
        user_location = input("Tell me where you are from first! ")
        if not user_location:
            return "Please tell me your location first."
    return gemini_respond(f"The user is in {user_location}. Respond with the weather.")


def get_greeting() -> str:
    hour = datetime.datetime.now().hour
    tod = "morning" if hour < 12 else "afternoon" if hour < 18 else "evening"
    who = user_name or "the user"
    return gemini_respond(f"Say a nice {tod} greeting to {who}.")


def analyze_image(image_path: str) -> None:
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


def generate_image(prompt: str) -> str:
    pass




def main() -> None:
    name = input("Hi! My name is Gemini, what is yours? ")
    print(set_name(name))
    print("Ask me about the time, weather, or say hi! I can also generate or analyze images.")

    while True:
        raw_input = input("\nWhat would you like me to do? ")
        command = str(raw_input).strip().lower()

        # Quit command
        if command in ("bye", "exit", "quit"):
            print("Goodbye! Have a great day!")
            break
        
        # Location setter
        if "from" in command:
            parts = command.split("from", 1)
            if len(parts) > 1:
                location = parts[1].strip()
                print(set_location(location))
            else:
                print("Please specify a location (e.g., 'weather from Athens').")
            continue

        # Time query
        if "time" in command:
            print(get_time())
            continue

        # Weather query
        if "weather" in command:
            print(get_weather())
            continue

        # Greeting
        if command in ["hi", "hello", "hey", "yo", "sup"]:
            print(get_greeting())
            continue

        if "image" in command:
            if "analyze" in command:
                image = input("What is the name of the image? ")
                if not image:
                    print("Please provide the image file name.")
                    continue
                analyze_image(image)
                continue
            elif "generate" in command:
                prompt = input("What image would you like me to generate? ")
                if not prompt:
                    print("Please describe the image you want to generate.")
                    continue
                print(generate_image(prompt.strip()))
                continue
            else:
                print("Try 'analyze image' or 'generate image'.")
                continue

        # Default: forward the user's text to the model
        print(gemini_respond(f"The user said: '{command}'. Respond naturally."))


if __name__ == "__main__":
    main()