import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
def levenshtein_distance(s, t):
    m, n = len(s), len(t)
    if m < n:
        s, t = t, s
        m, n = n, m
    d = [list(range(n + 1))] + [[i] + [0] * n for i in range(1, m + 1)]
    for j in range(1, n + 1):
        for i in range(1, m + 1):
            if s[i - 1] == t[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                d[i][j] = min(d[i - 1][j], d[i][j - 1], d[i - 1][j - 1]) + 1
    return d[m][n]
 
def compute_similarity(input_string, reference_string):
    distance = levenshtein_distance(input_string, reference_string)
    max_length = max(len(input_string), len(reference_string))
    similarity = 1 - (distance / max_length)
    return similarity


if __name__ == "__main__":
    df = pd.read_csv("./Data/embedding_similarity_output.csv")
    for index, row in df.iterrows():
        code = row["code"]
        obfuscated = row["obfuscatedCode"]
        df.at[index, "stringSimilarity"] = round(compute_similarity(code, obfuscated), 4)

    df.to_csv("./Data/string_similarity.csv", index=False)

    
    
    
        
    
    