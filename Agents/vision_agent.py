import os
from logger import get_logger
from CloudflareWorkersAI.cloudflare_workers_ai import CloudflareWorkersAI

logger = get_logger(__name__)

class VisionAgent:
    def __init__(self, model_url: str, image_dir: str, image_name: str):
        """
        Initialize the VisionAgent with a model URL and default image directory.

        :param model_url: URL of the Cloudflare Workers AI model.
        :param image_dir: Directory containing the image files.
        :param image_name: Default image name to use.
        """
        logger.info("Initializing VisionAgent...")

        self.llm = CloudflareWorkersAI(model_url=model_url)
        self.image_dir = image_dir
        self.image_name = image_name

        # Ensure the image directory exists
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)
            logger.debug(f"Created image directory: {self.image_dir}")


    def _get_image_path(self) -> str:
        """
        Get the full path of the default image.

        :return: Full image path.
        """
        image_path = os.path.join(self.image_dir, self.image_name)
        logger.debug(f"Image path: {image_path}")
        return image_path

    def _read_prompt_file(self, file_path: str) -> str:
        """
        Read and return the prompt text from a file.

        :param file_path: Path to the prompt file.
        :return: Prompt text.
        """
        logger.debug(f"Reading prompt file: {file_path}")
        if not os.path.exists(file_path):
            logger.error(f"Prompt file not found: {file_path}")
            raise FileNotFoundError(f"Prompt file not found: {file_path}")
        with open(file_path, "r") as file:
            return file.read().strip()

    def process_image_with_prompt(self, prompt_file: str) -> str:
        """
        Process an image and prompt using the LLM and return the response.

        :param prompt_file: Path to the prompt text file.
        :return: Response from the LLM.
        """
        logger.info("Processing image with prompt...")
        try:
            # Get the image path
            image_path = self._get_image_path()

            # Read the prompt
            prompt_text = self._read_prompt_file(prompt_file)

            # Prepare payload
            image_base64 = self.llm.encode_image_to_base64(image_path)
            payload = {
                "image": image_base64,
                "prompt": prompt_text,
            }

            # Get response
            response = self.llm._call(prompt=payload, image_prompt=True)
            logger.info("Response from LLM obtained successfully.")

            return response
        except Exception as e:
            logger.error("Error during image processing.", exc_info=True)
            raise
