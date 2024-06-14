import pathlib
import textwrap

import os
import time
from dotenv import load_dotenv
import google.generativeai as genai
import pandas as pd


def get_obfuscation_prompts(prompt, code):
    template = f'''You will be acting as a code obfuscation tool. When I write BEGIN, you will enter this role. All further input from the "User:" will be a request to obfuscate a JavaScript code snippet using a specified method.
    Here are the steps to follow for each request:
    1. The user will provide the original JavaScript code snippet inside {{CODE}} tags like this:
    <code>
    {{CODE}}
    </code>

    2. The user will then specify the obfuscation method to use inside {{OBFUSCATION_METHOD}} tags like this:
    <obfuscation_method>
    {{OBFUSCATION_METHOD}}
    </obfuscation_method>

    3. Obfuscate the provided JavaScript code using the specified method. Some common obfuscation methods include:
    - Renaming variables and functions
    - Inserting dead code or dummy statements
    - Splitting strings
    - Encoding strings or numbers
    - Flattening the control flow
    - Using complex expressions or formulas
    Only use the obfuscation method that the user specifies.

    4. Ignore spacing and line breaks. Only include code. To separate lines use the ";" syntax. 

    5. After obfuscating the code, provide the obfuscated version as a STRING. Ensure that the only output you return is the code represented as a string.

    6. Ensure that the obfuscated code, when executed, produces the same output as the original code. The goal is to make the code harder to understand while preserving its functionality.

    Remember:
    - Only obfuscate the code using the method specified by the user.
    - The obfuscated code should be functionally equivalent to the original code.
    - Do not explain your obfuscation process or include any additional commentary.
    - Provide only the code as a string.

    BEGIN

    <code>
    {code}
    </code>

    <obfuscation_method>
    {prompt}
    </obfuscation_method>
    '''

    return template 


# Return a list of code snippets given a csv with the first column having code snippets
def get_code_snippets(csv_path):

    df = pd.read_csv(csv_path)
    code_snippets = []
    for i in range(size_of_df):
        code_snippets.append(df.iloc[i,0])
    return code_snippets


if __name__ == "__main__":

    
    load_dotenv()
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-pro')
    safety_settings = [
        {
            "category": "HARM_CATEGORY_DANGEROUS",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE",
        },
    ]

    # response = model.generate_content("What is the meaning of life?")
    data_path = "./data/code_snippets_update.csv"

    df = pd.read_csv(data_path)

    size_of_df = df.shape[0]
    
    prompt_types= ["Dead Code Obfuscation", "Naming Obfuscation"]

    code_snippets = get_code_snippets(data_path)
    obfuscated_snippets = []
    prompt_column_tracker = []


    error_counter = 0 # if it reaches five, then it is stuck in a loop
    counter = 0  # used to track where progress is at
    while True:
        try :
            if (counter % 10 == 0):
                print(f"Currently at: {counter}")
            print("in try")    # debugging purposes
            
            # Sets the prompt
            # First half is dead code, the second off is naming
            prompt_type = ""
            if counter <= (size_of_df // 2):
                prompt_type = prompt_types[0]
            else: 
                prompt_type = prompt_types[1]
            
            print(prompt_type)    # debugging purposes
            

            # Generate snippets
            prompt = get_obfuscation_prompts(prompt_type, code_snippets[counter])
            response = model.generate_content(prompt,safety_settings=safety_settings)


            # Clean data
            obfuscated_code = response.text
            obfuscated_code = obfuscated_code.strip()
            if obfuscated_code.startswith('"') and obfuscated_code.endswith('"'):
                obfuscated_code = obfuscated_code.strip("")
            
            obfuscated_snippets.append(obfuscated_code)

            prompt_column_tracker.append(prompt_type)

            print("got prompt")    # debugging purposes

            # Reset error counter since it worked this iteration
            error_counter = 0
            # Track how many snippets we have made
            counter += 1

            # If we have made all the snippets, then end
            if counter >= size_of_df:
                print("ended")    # debugging purposes
                break

            print("at end of try") # debugging purposes
            time.sleep(6)
        # Catches errors such as resources limited and safety errors.
        except:

            print("In except")      # debugging purposes
            if error_counter >= 5:
                raise Exception("Failed 5 or more times")
            error_counter += 1
            time.sleep(30)
        
    
    df['obfuscate code'] = pd.Series(obfuscated_snippets)
    df["obfuscation type"] = pd.Series(prompt_column_tracker)
    df.to_csv("./data/obfuscated_output.csv", index=False)

        

    

    