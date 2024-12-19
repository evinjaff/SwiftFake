import ollama

from ollama import chat
from ollama import ChatResponse

import speech_recognition as sr

import os
from gtts import gTTS
import speech_recognition as sr

MODEL_STRING = 'llama3.2:3b'
MAX_DURATION = 25

class RobocallStrategy:

    valid_strategies = ["repeat", "use_llm", "basic_tree"]
    step = 0
    opening = ""
    opts = {}

    def __init__(self, strategy, opening, optionals={}) -> None:
        if strategy not in self.valid_strategies:
            raise ValueError("Invalid strategy")
        
        self.response_strategy = strategy
        self.opening = opening
        self.opts = optionals

    def pretty_print(self):
        return """

        Strategy: {}
        Opening: {}
        Options: {}

        """.format(self.response_strategy, self.opening, self.opts)

    def get_response(self):
        print(self.step)
        if self.step == 0:
            self.step += 1
            return self.opening
        
        else:
            if self.response_strategy == "repeat":
                self.step += 1
                return self.opening

            elif self.response_strategy == "use_llm":
                raise ValueError("not implemented")

            elif self.response_strategy == "basic_tree":
                if self.step > 0:
                    if self.step < len(self.opts["messages"]):
                        self.step += 1
                        return self.opts["messages"][self.step - 1]
                    else:
                        self.step += 1
                        return ""
                
                else:
                    self.step += 1
                    return self.opening
            
            else:
                raise ValueError("Invalid strategy")
            
    def getTree(self):
        pass




def create_text_to_speech_file(text, output_file):
    # Create a gTTS object
    tts = gTTS(text=text, lang="en")
    # Save the audio file
    tts.save(output_file)

    return output_file


def transcode_tts_to_webrtc_compatible_wav(input_file):

    output_file = input_file.replace(".mp3", ".wav")

    ffmpeg_command = "ffmpeg -y -i {} -ar 16000 -ac 1 -c:a pcm_s16le {}".format(input_file, output_file)

    # Convert the MP3 file to WAV format, blocking until complete
    os.system(ffmpeg_command)


    return output_file

def estimate_duration(response_list):

    duration = 0
    for message in response_list:

        content = message["content"]

        duration += len(content) / 12.5

    return duration

def closing_routine(llm_messages):

    llm_messages.append({
        'role': 'user',
        'content': 'Ok, time is up, you have to make a decision to allow or block the call. Write (call: allow) or (call: block) and provide an explanation'
    })

    response = chat(model=MODEL_STRING, messages=llm_messages)
    print(response["message"]["content"])

    return response["message"]["content"]


def simulate_scam_call(attacker_strategy, duration):

    llm_messages = [
        {
            'role': 'user',
            'content': 'You are a helpful assistant. You are here to help screen the user\'s phone calls for malicious calls. \
            Some rules to follow:    \
            -Pretend like you are on the phone. For example, instead of saying "I would say Hello"  say "Hello"   \
            -Keep responses short     \
            -I will inform you that you have to make a decision to allow or block the call after a certain amount of time. When I do, write (call: allow) or (call: block).   \
            You must only do this when I ask you. \
            If you understand, repeat your opening message: "Hello, this is an automated bot using call screening, please state the purpose of the call"'
        }
    ]

    
    response = chat(model=MODEL_STRING, messages=llm_messages)
    print(response["message"]["content"])

    llm_messages.append({
        "role": "assistant",  # Ensure the role matches the model's expected behavior
        "content": response["message"]["content"]  # Access correctly
    })

    transcript = []

    transcript.append({
        "role": "defender",
        "content": response["message"]["content"]
    })

    new_messages = []
    while True:

        print("\n")

        scam_message = attacker_strategy.get_response()

        print("scam message: ", scam_message)

        if scam_message != "":

            scam_file = create_text_to_speech_file(scam_message, "scam.mp3")

            scam_wav = transcode_tts_to_webrtc_compatible_wav(scam_file)

            transcript.append({
            "role": "attacker",
            "content": scam_message
            })

            # use asr to read the scam message
            r = sr.Recognizer()
            with sr.AudioFile(scam_wav) as source:
                audio = r.record(source)
                try:
                    scam_message = r.recognize_google(audio)
                except:
                    scam_message = ""
            
            if scam_message != "":

                print("Scammer: ", scam_message)

                # Add a new user message to continue the conversation
                llm_messages.append({
                    "role": "user",
                    "content": scam_message
                })

                new_messages.append({
                    "role": "user",
                    "content": scam_message
                })

                response = chat(model=MODEL_STRING, messages=llm_messages)
                print("LLM: ", response["message"]["content"])

                transcript.append({
                "role": "defender",
                "content": response["message"]["content"]
                })

                t = estimate_duration(new_messages)

                print(t)

        if len(scam_message) == 0:
            # special case for the closing routine
            closing = closing_routine(llm_messages)

            return transcript, closing

        # governor of time
        if t > duration:
            print("decision:")
            closing = closing_routine(llm_messages)

            return transcript, closing

            break
        







    


if __name__ == "__main__":
    main()