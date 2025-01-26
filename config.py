import os

# Directories
IMAGE_DIR = 'images'
PROMPT_DIR = 'prompts'
AUDIO_DIR = 'audio'

# Prompt files
IMAGE_PROMPT = os.path.join(PROMPT_DIR, 'prompt.txt')
CLEANING_PROMPT = os.path.join(PROMPT_DIR, 'cleaning_prompt.txt')

# API Keys
DEEPGRAM_API = "fb283957453aa87358b42a3e1260f5c3f5f88823"
AWS_ACCESS_KEY = 'AKIAXTH4J5OP25KUCR7Z'
AWS_SECRET_KEY = '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'

# MODEL URLS
VISION_MODEL_URL = "https://yellow-block-4f5a.psurabhi.workers.dev"
REFORM_MODEL_URL = "https://llama.psurabhi.workers.dev/"