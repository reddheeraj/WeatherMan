import os
from deepgram import DeepgramClient, SpeakOptions

SPEAK_OPTIONS = {"text": "Hello, how can I help you today?"}
filename = "output.mp3"

def weather_audio(weather_report):
    try:
        SPEAK_OPTIONS = {"text": weather_report}
        filename = "output.mp3"
        with open("API_KEY.txt", "r") as f:
            API_KEY = f.read().strip()
        # STEP 1: Create a Deepgram client.
        # By default, the DEEPGRAM_API_KEY environment variable will be used for the API Key
        deepgram = DeepgramClient(API_KEY)

        # STEP 2: Configure the options (such as model choice, audio configuration, etc.)
        options = SpeakOptions(
            model="aura-asteria-en",
        )

        # STEP 3: Call the save method on the speak property
        response = deepgram.speak.rest.v("1").save(filename, SPEAK_OPTIONS, options)
        print(response.to_json(indent=4))

    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    SPEAK_OPTIONS = "Hello, how can I help you today?"
    weather_audio(SPEAK_OPTIONS)