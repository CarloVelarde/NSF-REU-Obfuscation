from generate_embeddings import calculate_cosine_similarity, get_embedding

from time import sleep
import pandas as pd
import google.generativeai as genai
import torch.nn.functional as F
import torch
import ast

if __name__ == "__main__":
    df = pd.read_csv('./Data/functionality_equality2.csv')

    true_count = 0
    false_count = 0

    for index, row in df.iterrows():
        if row["equivalent"]:
            true_count +=1
        else:
            false_count +=1
        

    
    print(f"False count: {false_count}, True count: {true_count}.")
