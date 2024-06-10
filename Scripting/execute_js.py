import re
import pandas as pd
import subprocess
import os


def execute_code(js_code):
    try:
        result = subprocess.run(
            ['node', '-e', js_code],
            capture_output=True, text=True, check=True
        )
        try:
            return result.stdout.strip()
        except Exception:
            return "Not a valid command."
        
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"
    
def has_bad_characters(s):
    return bool(re.search(r'[^\x00-\x7F]', s))


if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    project_dir = os.path.join(script_dir, '..')
    data_dir = os.path.join(project_dir, 'Data')
    csv_path = os.path.join(data_dir, 'code_snippets.csv')

    df = pd.read_csv(csv_path)

    df['output'] = df['code'].apply(execute_code)

    # Filter bad data
    df = df[~df["output"].str.contains("Error: Command")]

    df = df[~df["output"].apply(has_bad_characters)]
    
    df.to_csv(f"{data_dir}/code_snippets_with_output.csv", index = False)







        



