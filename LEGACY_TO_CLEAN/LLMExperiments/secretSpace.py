import ollama
import json


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


response = ollama.chat(
    model="llama3.2",
    options={
        "temperature": 0.3,
        "max_tokens": 100,
        "stop": ["</function>"]
    },
    messages=[
        {"role": "system", "content": system_prompt_public},
        {"role": "user", "content": 
         """
            Caller Says:
            Hello, this is Kevin from ADT, we've noticed some suspicious activity on your home security system.
            Audio Description: Male voice, american accent, 30s, professional tone
         """
        },
    ]
)

print("homegrown:")

print(response["message"]["content"])

print("\n")


if "<function=secure_conversation" in response["message"]["content"]:

    function_body = response["message"]["content"].split("<function=")[1]

    print("function_body: ", function_body)


print("tool:")

print(response["message"]["content"])

response = ollama.chat(
    model="llama3.2",
    options={
        "temperature": 0.2,
        "max_tokens": 100,
        "stop": ["</function>"]
    },
    messages=[
        {"role": "system", "content": system_prompt_public},
        {"role": "user", "content": 
         """
            Caller Says:
            Hello, this is Kevin from ADT, we've noticed some suspicious activity on your home security system.
            Audio Description: Male voice, american accent, 30s, professional tone
         """
        },
        {
            "role": "assistant",
            "content": "<function=secure_conversation>{{\"conversation_type\": \"fact_check\", \"question\": \"verify_recent_alert\", \"support\": \"\"}}</function>"
        },
        {
            "role": "ipython",
            "content": "Yes, this is correct. An alert did appear recently. Respond back to the caller as is appropriate or connect the call."
        }

    ]
)
print("True: ")

print(response["message"]["content"])