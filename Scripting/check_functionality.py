import os
from time import sleep
from dotenv import load_dotenv
import pandas as pd
import google.generativeai as genai
import torch.nn.functional as F

def get_prompt(normal, obfuscated):
    prompt = f'''I am going to give you two JavaScript code snippets. One code snippet is a normal JavaScript code snippet and the other code snippet is an obfuscated JavaScript code snippet. Determine the functionality of both code snippets. Determine if the code snippets funciton the same and produce the same output. Determine if the code snippets do not function the same and do not produce the same output. If the two code snippets have the same functionality and produce the same output, please return 'True'. If the code snippets do not have the same functionality and/or do not produce the same output, please return 'False'. The only output you should return is 'True' or 'False'. Remember, only return 'True' or 'False' depending on the functionality of the code. True if they match, false if they do not. 
    Code snippet one: '{normal}'.
    Code snippet two: '{obfuscated}'.
    '''
    return prompt

# Return a list of code snippets given a csv with the first column having code snippets
def get_code_snippets(csv_path, indx):

    df = pd.read_csv(csv_path)
    size_of_df = df.shape[0]
    code_snippets = []
    for i in range(size_of_df):
        code_snippets.append(df.iloc[i,indx])
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

    


    data_path = "./Data/string_similarity.csv"
    df = pd.read_csv(data_path)
    
    # Get an array holding normal and obfuscated codes from the csv file
    normal = get_code_snippets(data_path, 0)
    obfuscated = get_code_snippets(data_path, 1)
    obfuscated.append(obfuscated[0])
    results = []

    counter = 0 # used to index normal and obfuscated arrays
    counter2 = 1
    while counter < len(normal):
        try:
            print(counter)
            print("Start of try...")
            prompt = get_prompt(normal[counter], obfuscated[counter2])
            response = model.generate_content(prompt, safety_settings=safety_settings)

            print("Got response...")

            # Clean data
            result = response.text
            result = result.strip()
            if result.startswith('"') and result.endswith('"'):
                result = result.strip("")
            print("Result: ", result)
            results.append(result)
            counter += 1
            counter2 += 1

            print("At the end of try...")
            sleep(5)
        except:
            print("In except...")
            sleep(20)
    df["equivalent"] = pd.Series(results)
    df.to_csv("./Data/functionality_equiality2.csv", index = False)