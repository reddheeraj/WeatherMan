import base64
import requests
from typing import Optional, Dict
from logger import get_logger

logger = get_logger(__name__)

class CloudflareWorkersAI():
    def __init__(self, model_url: str):
        """
        Initialize the Cloudflare Workers AI client.

        :param model_url: The URL of the model endpoint hosted on Cloudflare Workers AI.
        """
        logger.info("Initializing CloudflareWorkersAI client...")
        self.model_url = model_url

    def set_model_url(self, model_url: str):
        """
        Set a different model URL to switch between models.

        :param model_url: The new model URL.
        """
        self.model_url = model_url

    @staticmethod
    def encode_image_to_base64(image_path: str) -> str:
        """
        Encode an image to a base64 string.

        :param image_path: Path to the image file.
        :return: Base64 encoded string of the image.
        """
        logger.debug(f"Encoding image to base64: {image_path}")

        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    @property
    def _llm_type(self) -> str:
        """
        Return the type of LLM.
        """
        return "cloudflare_workers_ai"

    def _model_info(self) -> Dict[str, str]:
        """
        Return the model information.

        :return: A dictionary containing the model information.
        """
        return {"model_type": self._llm_type, "model_url": self.model_url}

    def _call(self, prompt: Dict[str, str], image_prompt: bool, stop: Optional[str] = None) -> str:
        """
        Call the Cloudflare Workers AI endpoint.

        :param prompt: A dictionary containing the 'image' and 'prompt'.
        :param stop: Optional stop sequences (not used here).
        :return: Response from the model.
        """
        logger.info("Calling Cloudflare Workers AI endpoint...")

        headers = {"Content-Type": "application/json"}
        if not image_prompt:
            payload = {"prompt": prompt}
        else:
            payload = prompt
        try:
            response = requests.post(self.model_url, json=payload, headers=headers)
            logger.debug("Response received successfully.")
            if response.status_code != 200:
                raise Exception(f"Error from Cloudflare Workers AI: {response.text}")

            return response.json().get("response", "No response received")
        except Exception as e:
            logger.error(f"Error calling Cloudflare Workers AI endpoint: {e}", exc_info=True)
            raise