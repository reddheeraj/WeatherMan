from logger import get_logger
from Agents.vision_agent import VisionAgent
from Agents.reform_agent import ReformAgent
from config import IMAGE_DIR, IMAGE_PROMPT, CLEANING_PROMPT, VISION_MODEL_URL, REFORM_MODEL_URL, AWS_ACCESS_KEY, AWS_SECRET_KEY
from deepgram_audio import weather_audio
import os
from weather_data import fetch_weather
import streamlit as st
import requests
import boto3
import time

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
    st.set_page_config(page_title="NimbusNews", page_icon="🌦️")
    st.markdown("""
        <style>
            /* Hide the Deploy button */
            .stDeployButton {
                display: none;
            }
            /* Optional: Hide the hamburger menu */
            #MainMenu {visibility: hidden;}
            
            .stAppHeader {
                display: none;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("NimbusNews 🌦️")

    # Reordered tabs
    tab1, tab3, tab4 = st.tabs(["Generate Report", "Weather Forecast", "About"])

    with tab1:
        st.header("Upload or Select a Weather Chart")
        
        # images from s3
        s3 = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key= AWS_SECRET_KEY
        )
        # Access the weather-man bucket
        bucket_name = "weather-man"
        obj_list = s3.list_objects_v2(Bucket=bucket_name).get("Contents", [])
        # st.write("obj from s3", obj_list)
        object_list = [obj["Key"] for obj in obj_list]
        # for obj in object_list:
        #     response = s3.get_object(Bucket=bucket_name, Key=obj)
        #     image = response["Body"].read()
            # st.image(image, caption=obj, use_container_width=True)
        drop_down = st.selectbox("Select an image", ["Select an image"] + object_list)
        if drop_down == "Select an image":
            image_file = st.file_uploader("Upload an Image", type=["jpeg", "jpg", "png"])
            image_name = image_file.name if image_file else None
        else:
            response = s3.get_object(Bucket=bucket_name, Key=drop_down)
            image_file = response["Body"].read()
            image_name = drop_down
        if image_file:
            with open(os.path.join(IMAGE_DIR,image_name),"wb") as f: 
                if drop_down == "Select an image" and image_file:
                    f.write(image_file.getbuffer())
                else:
                    f.write(image_file)         
            # st.success("Saved File")
        if image_file:
            st.image(image_file, caption=image_name, use_container_width=False)
            # st.success("Image uploaded successfully! Head over to the 'Analysis' tab to process it.")
            st.session_state["uploaded_image"] = image_file
            col0, col1, col2 = st.columns([0.05, 0.06, 0.09])
            if image_name in object_list:
                col2 = st.columns([0.09])[0]
            with col2:
                if st.button("Analyze image"):
                    image_file = st.session_state.get("uploaded_image", None)
                    
                    if image_file == None:
                        st.error("Please upload an image!")
                        st.stop()
                    # image_name = image_file.name
                    # st.image(image_file, caption="Uploaded Image", use_container_width=True)
                    logger.info("Initializing VisionAgent and ReformAgent...")
                    # Initialize agents
                    vision_agent = VisionAgent(model_url=VISION_MODEL_URL, image_dir=IMAGE_DIR, image_name=image_name)
                    reform_agent = ReformAgent(model_url=REFORM_MODEL_URL)
                        
                    logger.info("Starting image processing pipeline...")

                    if image_file:
                        try:
                            with st.spinner("Processing and performing analysis..."):
                                # st.subheader("Analysis")

                                # Process image
                                response = process_image(vision_agent, IMAGE_PROMPT)

                                # Clean response
                                cleaned_response = clean_response(reform_agent, response, CLEANING_PROMPT)
                                print(cleaned_response)

                            # Show cleaned response
                            st.subheader("Summary")
                            st.text_area("", value=cleaned_response, height=200)
                            
                            st.divider()

                            # Show VisionAgent response
                            st.subheader("Detailed Analysis")
                            st.text_area("", value=response, height=200)

                            # Generate Deepgram audio
                            with st.spinner("Generating Deepgram audio..."):
                                audio_file_path = handle_deepgram_audio(cleaned_response)
                                st.audio(audio_file_path, format="audio/wav")
                            url = "http://127.0.0.1:5000/process"
                            headers = {
                                "Content-Type": "application/json"
                            }
                            video_dir = os.path.abspath("video")
                            video_file = "MyVideo.mp4"
                            # Construct the full paths
                            video_path = os.path.join(video_dir, video_file)
                            audio_path = os.path.join(os.path.abspath('audio') , "output.mp3")
                            # Define the output file path (you can customize this as needed)
                            output_path = os.path.join("video", "MyVideo_output.mp4")
                            payload = {
                                "video_file": video_path,
                                "vocal_file": audio_path,
                                "output_file": output_path
                            }
                            st.divider()
                            st.subheader("Video Report")
                            with st.spinner("Creating a video report..."):
                                response = requests.post(url, json=payload, headers=headers)

                            # Check the response status code and print the response
                            if response.status_code == 200:
                                st.video(os.path.join(video_dir, 'MyVideo_output_Easy-Wav2Lip.mp4'))
                        except Exception as e:
                            st.error(f"An error occurred in the pipeline!")
            if image_name not in object_list:
                with col1:
                    if st.button("Upload image"):
                        
                        @st.dialog("Upload image to S3")
                        def dialog(file_path, bucket_name, image_name):
                            st.write("Uploading image to DB...")
                            s3.upload_file(file_path, bucket_name, image_name)
                            st.write("Image uploaded successfully!")
                            time.sleep(2)
                            st.rerun()
                        dialog(os.path.join(IMAGE_DIR,image_name), bucket_name, image_name)

    with tab3:  # Renamed "Home" to "Weather Forecast"
        st.header("Search Weather Forecast by Location")
        location = st.text_input("Enter a city or country name", value="College Station")

        if st.button("Get Weather"):
            try:
                weather_data = fetch_weather(location)
                if weather_data:
                    st.subheader(f"Current Weather in {location}")
                    st.table([weather_data["current"]])  # Display general weather attributes

                    st.subheader("Daily Weather Forecast")
                    st.table(weather_data["daily"])  # Display daily forecast data
                else:
                    st.error(f"No weather data found for {location}. Please try again.")
            except Exception as e:
                st.error(f"An error occurred: {e}")

    with tab4:
        st.header("About NimbusNews")
        st.write(
            """
            **NimbusNews** is a powerful Agentic AI application designed to make weather data analysis easy and accessible from 4 panel weather charts.
            It is built using cutting-edge technology to deliver insights from visual weather data in a user-friendly way.
            """
        )
        st.write("Contact: praneetasritha@gmail.com | Version: 1.0.0")

if __name__ == "__main__":
    main()
