import ollama

from ollama import chat
from ollama import ChatResponse

import speech_recognition as sr

import os
from gtts import gTTS
import speech_recognition as sr

import json

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

        duration += len(content) / 18.5

    return duration

def closing_routine(llm_messages):

    llm_messages.append({
        'role': 'user',
        'content': 'Ok, time is up, you have to make a decision to allow or block the call. Write (call: allow) or (call: block) and provide an explanation'
    })

    response = chat(model=MODEL_STRING, messages=llm_messages)
    print(response["message"]["content"])

    return response["message"]["content"]


def simulate_scam_call_shadow(attacker_strategy, duration, model_id, facts):

        
    system_prompt_intro_public = """

    You are a helpful assistant. You are here to help screen the user's phone calls for malicious calls. \
    The prompts you recieve from the user are from a simulated scam call. Your goal is to identify the scam \
    by yourself and provide a summary of necessary information. You also are provided a function to verify facts. \
    Do not hesistate to call the function to verify facts. The user will provide you with the necessary information \
    Don't tell the user that you have access to a secure space, just call the function and say "one second please" \

    """

    secureSpaceTool_public = {
        "name": "secure_conversation",
        "description": "Temporarily suspend the chat with access to check for information in a secure space. You can use this to verify facts against a scam caller like, did I recently place an order? or is there a suspicious activity alert?",
        "parameters": {
            "type": "object",
            "conversation_type": {
                "type": {
                    "type": "enum string",
                    "description": "The type of conversation you want to have",
                    "enum": ["fact_check", "sensitive_information"],
                },
                "question": {
                    "type": "enum string",
                    "description": """
                    The information you want to ask, through a limited set of questions
                    
                    verify_recent_order: Did I recently place an order for a product?
                    is_this_person_someone_you_know: Is this person someone you know?

                    verify_recent_alert: Did I receive a recent alert for suspicious activity related to what the caller says?

                    """,
                    "enum": ["verify_recent_order", "is_this_person_someone_you_know", "verify_recent_alert"],
                },
                "support": {
                    "type": "string",
                    "description": "Any data you need to provide to answer the question",

                }
            },
            "required": ["conversation_type"],
        },
    }


    toolPrompt_public = f"""
    You have access to the following functions:

    Use the function '{secureSpaceTool_public["name"]}' to '{secureSpaceTool_public["description"]}':
    {json.dumps(secureSpaceTool_public)}

    If you choose to call a function ONLY reply in the following format with no prefix or suffix:

    <function=example_function_name>{{\"example_name\": \"example_value\"}}</function>

    Reminder:
    - Function calls MUST follow the specified format, start with <function= and end with </function>
    - Required parameters MUST be specified
    - Only call one function at a time
    - Put the entire function call reply on one line
    - If there is no function call available, answer the question like normal with your current knowledge and do not tell the user about function calls

    """


    system_prompt_public = system_prompt_intro_public + toolPrompt_public

    llm_messages = []
    new_messages = []

    llm_messages.append({
        "role": "user",
        "content": system_prompt_public
    })

    transcript = []

    # transcript.append({"role": "system", "content": system_prompt_public})

    # the attacker strategy loop

    while True:

        print(llm_messages)

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

                # response = chat(model=model_id, messages=llm_messages)
                response = ollama.chat(
                    model=model_id,
                    options={
                        "temperature": 0.3,
                        "max_tokens": 100,
                        "stop": ["</function>"]
                    },
                    messages=llm_messages
                )

                

                print("LLM: ", response["message"]["content"])

                # detect if the function call is used
                if "secure_conversation" in response["message"]["content"] and "function" in response["message"]["content"]:
                    
                    function_body = response["message"]["content"].split("<function=")[1]

                    print("function_body: ", function_body)

                    # look for which enum is used

                    if "verify_recent_order" in function_body:
                        # append the fact to the conversation list
                        llm_messages.append({
                            "role": "ipython",
                            "content": facts["verify_recent_alert"]
                        })
                    elif "is_this_person_someone_you_know" in function_body:
                        # append the fact to the conversation list
                        llm_messages.append({
                            "role": "ipython",
                            "content": facts["verify_recent_alert"]
                        })
                    elif "verify_recent_alert" in function_body:
                        # append the fact to the conversation list from facts["verify_recent_alert"]
                        llm_messages.append({
                            "role": "ipython",
                            "content": facts["verify_recent_alert"]
                        })
                    else:
                        llm_messages.append({
                            "role": "ipython",
                            "content": "Unable to verify the fact"
                        })
                        print("!!!! BAD FUNCTION CALL !!!!")



                transcript.append({
                "role": "defender",
                "content": response["message"]["content"]
                })

                t = estimate_duration(transcript)

                print("Duration", t)



        if len(scam_message) == 0:
            # special case for the closing routine
            closing = closing_routine(llm_messages)

            return transcript, closing

        # governor of time
        if t > duration:
            print("decision:")
            closing = closing_routine(llm_messages)

            return transcript, closing
        
def simulate_scam_call(attacker_strategy, duration, model_id):

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

                response = chat(model=model_id, messages=llm_messages)
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






    







