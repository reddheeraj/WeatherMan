from itt import weather_report
from deepgram_audio import weather_audio

if __name__ == "__main__":
    image_path = "images/Image1.jpeg"
    weather_report = weather_report(image_path)
    print(weather_report)
    weather_audio(weather_report)