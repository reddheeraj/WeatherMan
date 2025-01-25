import os
from deepgram import DeepgramClient, SpeakOptions
from config import DEEPGRAM_API, AUDIO_DIR
SPEAK_OPTIONS = {"text": "Hello, how can I help you today?"}



def weather_audio(weather_report):
    try:
        if not os.path.exists(AUDIO_DIR):
            os.makedirs(AUDIO_DIR)
        SPEAK_OPTIONS = {"text": weather_report}
        filename = "output.mp3"

        filename = os.path.join(AUDIO_DIR, filename)
       
        # STEP 1: Create a Deepgram client.
        # By default, the DEEPGRAM_API_KEY environment variable will be used for the API Key
        deepgram = DeepgramClient(DEEPGRAM_API)

        # STEP 2: Configure the options (such as model choice, audio configuration, etc.)
        options = SpeakOptions(
            model="aura-asteria-en",
        )

        # STEP 3: Call the save method on the speak property
        response = deepgram.speak.rest.v("1").save(filename, SPEAK_OPTIONS, options)
        print(response.to_json(indent=4))

        return filename

    except Exception as e:
        print(f"Exception: {e}")