import speech_recognition as sr


def recognize_speech_from_microphone(duration):
    # Initialize recognizer class in SpeechRecognition
    recognizer = sr.Recognizer()

    # List all microphone names and indices
    mic_list = sr.Microphone.list_microphone_names()

    # Find the index of the microphone named "VB-Cable"
    vb_cable_index = None
    for index, mic_name in enumerate(mic_list):
        if "VB-Cable" in mic_name:
            vb_cable_index = index
            break

    # Check if the VB-Cable mic was found
    if vb_cable_index is not None:
        print(f"VB-Cable found at index {vb_cable_index}.")
        # Create a microphone object with the VB-Cable index
        vb_cable_mic = sr.Microphone(device_index=vb_cable_index)

         # Use the microphone as the source
        with vb_cable_mic as source:
            print("Adjusting for ambient noise. Please wait...")
            recognizer.adjust_for_ambient_noise(source, duration=duration)  # Calibrate to background noise
            print("Listening for speech. Speak into the microphone...")

            try:
                # Capture audio from the microphone
                audio_data = recognizer.listen(source, timeout=10, phrase_time_limit=15)
                print("Processing audio...")

                # Perform speech recognition using Google Web Speech API
                text = recognizer.recognize_google(audio_data)
                print("You said:", text)

                return text

            except sr.WaitTimeoutError:
                return ""
            except sr.UnknownValueError:
                print("Google Web Speech API could not understand the audio.")
            except sr.RequestError as e:
                print(f"Could not request results from Google Web Speech API: {e}")


    else:
        print("VB-Cable microphone not found.")


   


if __name__ == "__main__":
    recognize_speech_from_microphone(3)