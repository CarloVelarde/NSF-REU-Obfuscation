import pathlib
import textwrap
import time
import os
from dotenv import load_dotenv

import google.generativeai as genai

import pandas as pd

from IPython.display import display
from IPython.display import Markdown


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))



if __name__ == "__main__":
  
  
  # Api config
  load_dotenv()
  GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

  genai.configure(api_key = GOOGLE_API_KEY)


  # Select model
  model = genai.GenerativeModel("gemini-1.0-pro")


  # Generate code snippets
  code_snippets = []
  for _ in range(5):
      try:
          response = model.generate_content("Write me a javascript program that is no more than 10 lines. It should be simple but it should not have control flows or loops. It needs to have easy logic. Do not use randomness, dates, or variables that can change depending when called. The program should console.log all results. Ignore formatting, simply use ';' when the line ends. Do not use line breaks in the string response, use semi colons. In the string response do not use '/' or '\'. I want a pure string without extra operators. Just use the necessary syntax. Please refrain from using nested quotes and /. I just want a string. Here is an example of an acceptable program: 'let name = 'Carlo';console.log(name);")
          code_snippets.append(response.text)
          time.sleep(2)
      except:
          print("Exhausted")
          break

  

  # Construct path
  script_dir = os.path.dirname(__file__)
  csv_path = os.path.join(script_dir, '..', 'Data', 'code_snippets.csv')
  
  # Add code snippets to existing csv
  if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    new_data = pd.DataFrame({'Code': code_snippets})
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv('Data/code_snippets.csv', index = False)
  else:
     print(f"File not found: {csv_path}")
