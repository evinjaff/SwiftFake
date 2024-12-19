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


def test_whether_function_call_is_used(opening, response, model_id):



    response = ollama.chat(
        model=model_id,
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
                {}
            """.format(opening)
            },
        ]
    )


    if "<function=secure_conversation" in response["message"]["content"]:

        function_body = response["message"]["content"].split("<function=")[1]
        # print("function_body: ", function_body)

        return True, function_body
    
    else:
        return False, ""




# names

male_names = ["Michael", "Robert", "John", "David", "William", "Richard", "Joseph", "Thomas", "Christopher",
    "Charles", "Daniel", "Matthew", "Anthony", "Mark", "Donald", "Steven", "Andrew", "Paul", "Joshua",
    "Kenneth", "Kevin", "Brian", "Timothy", "Ronald", "George", "Jason", "Edward", "Jeffrey", "Ryan",
    "Jacob", "Nicholas", "Gary", "Eric", "Jonathan", "Stephen", "Larry", "Justin", "Scott", "Brandon",
    "Benjamin", "Samuel", "Gregory", "Alexander", "Patrick", "Frank", "Raymond", "Jack", "Dennis", "Jerry",
    "Tyler", "Aaron", "Jose", "Adam", "Nathan", "Henry", "Zachary", "Douglas", "Peter", "Kyle",
    "Noah", "Ethan", "Jeremy", "Christian", "Walter", "Keith", "Austin", "Roger", "Terry", "Sean",
    "Gerald", "Carl", "Dylan", "Harold", "Jordan", "Jesse", "Bryan", "Lawrence", "Arthur", "Gabriel",
    "Bruce", "Logan", "Billy", "Joe", "Alan", "Juan", "Elijah", "Willie", "Albert", "Wayne",
    "Randy", "Mason", "Vincent", "Liam", "Roy", "Bobby", "Caleb", "Bradley", "Russell", "Lucas"
]

female_names = [
    "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Karen", "Sarah",
    "Lisa", "Nancy", "Sandra", "Betty", "Ashley", "Emily", "Kimberly", "Margaret", "Donna", "Michelle",
    "Carol", "Amanda", "Melissa", "Deborah", "Stephanie", "Rebecca", "Sharon", "Laura", "Cynthia", "Dorothy",
    "Amy", "Kathleen", "Angela", "Shirley", "Emma", "Brenda", "Pamela", "Nicole", "Anna", "Samantha",
    "Katherine", "Christine", "Debra", "Rachel", "Carolyn", "Janet", "Maria", "Olivia", "Heather", "Helen",
    "Catherine", "Diane", "Julie", "Victoria", "Joyce", "Lauren", "Kelly", "Christina", "Ruth", "Joan",
    "Virginia", "Judith", "Evelyn", "Hannah", "Andrea", "Megan", "Cheryl", "Jacqueline", "Madison", "Teresa",
    "Abigail", "Sophia", "Martha", "Sara", "Gloria", "Janice", "Kathryn", "Ann", "Isabella", "Judy",
    "Charlotte", "Julia", "Grace", "Amber", "Alice", "Jean", "Denise", "Frances", "Danielle", "Marilyn",
    "Natalie", "Beverly", "Diana", "Brittany", "Theresa", "Kayla", "Alexis", "Doris", "Lori", "Tiffany"
]

company_names = ["Apple", "Amazon", "ADP", "Aramark", "ADT", "Aflac", "AIG", "Allstate", "American Express", 
                 "American Airlines", "American Family Insurance", "American International Group", "American Red Cross",
                 "Baker Hughes", "Bank of America", "Barnes & Noble", "Baxter International", "Becton Dickinson",
                 "C.H. Robinson", "Cablevision", "Calpine", "Campbell Soup", "Capital One", "Cardinal Health",
                 "Darden Restaurants", "DaVita", "Dean Foods", "Deere & Company", "Dell", "Delphi Automotive",
                 "Eli Lilly", "EMC Corporation"]

names = male_names + female_names


# randomly sample 200 unique combinations of names and companies
# ONLY NEEDS TO BE RUN ONCE
# import random

# name_company_combinations = []
# for i in range(200):
#     name = random.choice(names)
#     company = random.choice(company_names)
#     name_company_combinations.append((name, company))


# print(name_company_combinations)

# import opening statements from opening_statements.json

opening_statements = json.load(open("opening_statements.json"))

print(len(opening_statements))


# AI-generate an opening statement for a legitimate call using these names and companies
results_dict = {}

import tqdm

progressbar = tqdm.tqdm(range(200))

model = "gemma:2b"

for i in range(200):

    # increment progress bar by 1
    progressbar.update(1)
    
    # name, company = name_company_combinations[i]
    
    # opening = ollama.chat("llama3.1", messages=[
    #     {"role": "user", "content": 
    #         "You are a helpful assistant who helps generate customer service greetings for a call center for someone who is returning a call. \
    #         Using the provided name and company, generate a short opening statement for a legitimate support request.\
    #         The opening statement should be professional and courteous. Do not add anything extra, just the \
    #          statement. The agent's name is {} for {} \
    #             ".format(name, company)
    #      },
    # ])

    # statement = opening["message"]["content"]
    # print(i)
    # print(opening_statements[i])

    statement = opening_statements[i]

    r, fb = test_whether_function_call_is_used(statement, statement, model)

    results_dict[statement] = (r, fb)

json.dump(results_dict, open("results_dict_{}.json".format(model), "w"))

print(opening_statements)
