import requests
import base64
import ast

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def send_request(url, payload, headers):
    response = requests.post(url, json=payload, headers=headers)
    return response
def dict_res(res):
    dict_res = ast.literal_eval(res)["response"]
    return dict_res
def send_image_with_prompt(image_path):
    with open('prompt.txt', 'r') as file:
        prompt = file.read().strip()
    image_base64 = encode_image_to_base64(image_path)
    url = "https://yellow-block-4f5a.psurabhi.workers.dev"  # Replace with your API endpoint
    payload = {
        "image": image_base64,
        "prompt": prompt
    }
    # print(image_base64)
    headers = {"Content-Type": "application/json"}
    response = send_request(url, payload, headers)
    return response

def clean_response(response):
    url = 'https://llama.psurabhi.workers.dev/'
    with open('cleaning_prompt.txt', 'r') as file:
        prompt = file.read().strip()
    prompt += response
    payload = {
        "prompt": prompt
    }
    headers = {"Content-Type": "application/json"}
    response = send_request(url, payload, headers)
    return response.text

image_path = 'Image1.jpeg'
response = send_image_with_prompt(image_path)
weather_report = dict_res(response.text)
print(weather_report)
clean_response = clean_response(weather_report)
print(clean_response)