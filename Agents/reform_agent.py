from logger import get_logger
from CloudflareWorkersAI.cloudflare_workers_ai import CloudflareWorkersAI

logger = get_logger(__name__)

class ReformAgent:
    def __init__(self, model_url: str):
        """
        Initialize the ReformAgent with a model URL.

        :param model_url: URL of the Cloudflare Workers AI model.
        """
        logger.info("Initializing ReformAgent...")
        self.llm = CloudflareWorkersAI(model_url=model_url)

    def _read_prompt_file(self, file_path: str) -> str:
        """
        Read and return the prompt text from a file.

        :param file_path: Path to the cleaning prompt file.
        :return: Cleaning prompt text.
        """
        logger.debug(f"Reading prompt file: {file_path}")
        if not file_path or not isinstance(file_path, str):
            logger.error("Invalid file path provided.")
            raise ValueError("Invalid file path provided.")
        try:
            with open(file_path, "r") as file:
                return file.read().strip()
        except FileNotFoundError as e:
            logger.error(f"Prompt file not found: {file_path}", exc_info=True)
            raise e

    def clean_response(self, raw_response: str, cleaning_prompt_file: str) -> str:
        """
        Clean the raw response using the cleaning prompt via the LLM.

        :param raw_response: The raw response text to clean.
        :param cleaning_prompt_file: Path to the cleaning prompt file.
        :return: Cleaned response text.
        """
        logger.debug("Cleaning response...")

        if not raw_response or not isinstance(raw_response, str):
            logger.error("Invalid raw response provided.")
            raise ValueError("Invalid raw response provided.")

        try:
            # Read the cleaning prompt
            cleaning_prompt = self._read_prompt_file(cleaning_prompt_file)

            # Combine cleaning prompt and raw response
            combined_prompt = f"{cleaning_prompt}\n\n{raw_response}"

            # Get response from LLM
            response = self.llm._call(prompt=combined_prompt, image_prompt=False)
            logger.info("Cleaned response obtained successfully.")

            return response
        except Exception as e:
            logger.error("Error during response cleaning.", exc_info=True)
            raise

