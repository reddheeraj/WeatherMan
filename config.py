import os

# Directories
IMAGE_DIR = 'images'
PROMPT_DIR = 'prompts'
AUDIO_DIR = 'audio'

# Prompt files
IMAGE_PROMPT = os.path.join(PROMPT_DIR, 'prompt.txt')
CLEANING_PROMPT = os.path.join(PROMPT_DIR, 'cleaning_prompt.txt')

# API Keys
with open('KEYS.txt', 'r') as f:
    keys = f.readlines()
    keys = [key.strip() for key in keys]
    DEEPGRAM_API = keys[0]
    AWS_ACCESS_KEY = keys[1]
    AWS_SECRET_KEY = keys[2]

# MODEL URLS
VISION_MODEL_URL = "https://llama-vision.akash-pillai-0810.workers.dev/"
REFORM_MODEL_URL = "https://llama.akash-pillai-0810.workers.dev/"