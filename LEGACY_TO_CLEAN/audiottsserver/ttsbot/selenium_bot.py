from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import torch
from gtts import gTTS
import os


import ttsMic
import asr


def start_browser():
    # Set up WebDriver with fake audio
    options = Options()
    # options.add_argument("--use-fake-ui-for-media-stream")  # Auto-allow mic/cam
    # options.add_argument(f"--use-file-for-fake-audio-capture={file_path}")  # Fake audio input

    # Set default microphone to "Steam Streaming Microphone"
    prefs = {
        "profile.default_content_setting_values.media_stream_mic": 1,  # Allow mic usage
        "profile.default_content_settings.media_stream": 1,
        "profile.managed_default_content_settings.media_stream": 1,
        "media_stream": {
            "mic": "Steam Streaming Microphone"  # Replace with desired mic name
        }
    }
    options.add_experimental_option("prefs", prefs)

    # service = Service()  # Replace with the path to your ChromeDriver
    driver = webdriver.Chrome(options=options)
    return driver

driver = start_browser()

# Open WebRTC client
driver.get("http://localhost:5000")

# Automate interactions
# Example: Click a "Start" button on the page
start_button = driver.find_element(By.ID, "start-call")
start_button.click()


device = ttsMic.setup()

ttsMic.inject("Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.", device)

print("speech: {}".format(asr.recognize_speech_from_microphone(5) )) 

# Wait for the interaction




time.sleep(65)

# Close the browser
driver.quit()
