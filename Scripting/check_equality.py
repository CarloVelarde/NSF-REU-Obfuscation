import pandas as pd

import os



if __name__ == "__main__":

    # Checks if the obfuscated and normal output matches
    # Puts result in 'equal' column
    df = pd.read_csv("Data/code_obfuscate_both_outputs.csv")

    df['equal'] = df['obfuscate output'] == df['output']

    df.to_csv("Data/obfuscation_sheet.csv", index = False)

