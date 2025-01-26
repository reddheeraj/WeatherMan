from weather_data import fetch_weather
import streamlit as st

def main():
    st.set_page_config(page_title="WeatherMan", page_icon="🌦️", layout="wide")

    st.title("WeatherMan 🌦️")

    # Reordered tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Upload Image", "Analysis", "Weather Forecast", "About"])

    with tab1:
        st.header("Upload Weather Images")
        st.write("Supported formats: `.jpeg`, `.jpg`, `.png`")
        image_file = st.file_uploader("Upload an Image", type=["jpeg", "jpg", "png"])

        if image_file:
            st.image(image_file, caption="Uploaded Image", use_container_width=True)
            st.success("Image uploaded successfully! Head over to the 'Analysis' tab to process it.")
            st.session_state["uploaded_image"] = image_file

    with tab2:
        st.header("Analysis")
        image_file = st.session_state.get("uploaded_image", None)

        if image_file:
            st.subheader("Quick Summary")
            st.text_area("", value="Placeholder for analysis output", height=200)

            st.divider()

            st.subheader("Detailed Analysis")
            st.text_area("", value="Placeholder for detailed analysis", height=200)

            with st.spinner("Generating Video Summary..."):
                st.video("./video/summary.mp4", format="video/mp4")
        else:
            st.warning("Please upload an image first from the 'Upload Image' tab.")

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
        st.header("About WeatherMan")
        st.write(
            """
            **WeatherMan** is a powerful AI-driven application designed to make weather data analysis easy and accessible.
            It is built using cutting-edge technology to deliver insights from visual weather data in a user-friendly way.
            """
        )
        st.write("Contact: support@weatherman.ai | Version: 1.0.0")

if __name__ == "__main__":
    main()
