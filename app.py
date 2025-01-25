from logger import get_logger
from Agents.vision_agent import VisionAgent
from Agents.reform_agent import ReformAgent
from config import IMAGE_DIR, IMAGE_PROMPT, CLEANING_PROMPT, VISION_MODEL_URL, REFORM_MODEL_URL
from deepgram_audio import weather_audio
import streamlit as st
import tempfile

# Initialize logger
logger = get_logger(__name__)

def process_image(vision_agent: VisionAgent, prompt_file: str) -> str:
    """
    Process an image using the VisionAgent and return the response.
    
    :param vision_agent: Instance of VisionAgent.
    :param prompt_file: Path to the prompt file.
    :return: Response from the VisionAgent.
    """
    try:
        response = vision_agent.process_image_with_prompt(prompt_file)
        return response
    except Exception as e:
        logger.error(f"Error during VisionAgent processing: {e}", exc_info=True)
        raise

def clean_response(reform_agent: ReformAgent, response: str, cleaning_prompt_file: str) -> str:
    """
    Clean a response using the ReformAgent and return the cleaned text.
    
    :param reform_agent: Instance of ReformAgent.
    :param response: Raw response to be cleaned.
    :param cleaning_prompt_file: Path to the cleaning prompt file.
    :return: Cleaned response.
    """
    try:
        cleaned_response = reform_agent.clean_response(response, cleaning_prompt_file)
        return cleaned_response
    except Exception as e:
        logger.error(f"Error during ReformAgent cleaning: {e}", exc_info=True)
        raise

def handle_deepgram_audio(cleaned_response: str):
    """
    Handle Deepgram audio generation based on the cleaned response.
    
    :param cleaned_response: The cleaned response text.
    """
    try:
        logger.info("Generating audio with Deepgram...")
        output_file = weather_audio(cleaned_response)
        logger.info("Audio generated successfully.")

        return output_file
    except Exception as e:
        logger.error(f"Error during Deepgram audio generation: {e}", exc_info=True)
        raise

def main():
    """
    Main function to orchestrate the image processing, cleaning, and audio generation pipeline.
    """
    st.title("WeatherMan")
    logger.info("Initializing VisionAgent and ReformAgent...")
    
    # navbar = st.sidebar.radio("Navigation", ["Upload Image", "Analysis", "About"])

    st.subheader("Upload Weather Images")
    image_file = st.file_uploader("Upload an Image", type=["jpeg", "jpg", "png"])
    # if navbar == "Upload Image":
    #     st.subheader("Upload Weather Images")
    #     image_file = st.file_uploader("Upload an Image", type=["jpeg", "jpg", "png"])

    # if navbar == "Analysis" and image_file:
    #     st.subheader("Analysis")
    #     st.write("Please click the button below to start the analysis.")
    #     st.write("The analysis will process the image, clean the response, and generate an audio report.")
    if image_file:
        
        if st.button("Run Analysis"):
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpeg') as tmp_file:
                tmp_file.write(image_file.read())
                image_name = tmp_file.name
                st.image(image_file, caption="Uploaded Image", use_container_width=True)

            # Initialize agents
            # image_name = "Image1.jpeg"
            vision_agent = VisionAgent(model_url=VISION_MODEL_URL, image_dir=IMAGE_DIR, image_name=image_name)
            reform_agent = ReformAgent(model_url=REFORM_MODEL_URL)
            
            logger.info("Starting image processing pipeline...")
            
            try:
                with st.spinner("Processing and performing analysis..."):

                    # Process image
                    response = process_image(vision_agent, IMAGE_PROMPT)

                    # Clean response
                    cleaned_response = clean_response(reform_agent, response, CLEANING_PROMPT)
                    print(cleaned_response)

                # Show cleaned response
                st.subheader("Quick Summary")
                st.text_area("", value=cleaned_response, height=200)
                
                st.divider()

                # Show VisionAgent response
                st.subheader("Detailed Analysis")
                st.text_area("", value=response, height=200)

                # Generate Deepgram audio
                with st.spinner("Generating Deepgram audio..."):
                    audio_file_path = handle_deepgram_audio(cleaned_response)
                    st.audio(audio_file_path, format="audio/wav")

            except Exception as e:
                st.error(f"An error occurred in the pipeline: {e}")
    

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(f"Unhandled exception in application: {e}", exc_info=True)
        raise
