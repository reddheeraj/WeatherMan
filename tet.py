import boto3
from config import AWS_ACCESS_KEY, AWS_SECRET_KEY, IMAGE_PROMPT
from PIL import Image
from io import BytesIO
with open(IMAGE_PROMPT, "r") as file:
    prompt_text = file.read().strip()
image_path = 'images/2025-01-25_2313.png'
model_id = 'us.meta.llama3-2-90b-instruct-v1:0'
bedrock_runtime = boto3.client('bedrock-runtime', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY, region_name='us-west-2')


def resize_image(image_path, size=(1120, 1120)):
    with Image.open(image_path) as img:
        img = img.resize(size)
    return img
image = resize_image(image_path)

img_byte_array = BytesIO()
image.save(img_byte_array, format="PNG")
image = img_byte_array.getvalue()
print(type(image))

# image.save(image_path, format="PNG")  # Save the image to the buffer in PNG format
# with open(image_path, "rb") as f:
#     image = f.read()

print(type(image))
messages = [
    {
        'role':'user',
        'content':[
            {'image':{'format':'png','source':{'bytes':image}}},
            {'text': prompt_text}
        ],
    }
]
response = bedrock_runtime.converse(modelId = model_id, messages = messages)
print(response)