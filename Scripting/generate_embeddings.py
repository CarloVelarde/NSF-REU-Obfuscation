from time import sleep
import pandas as pd
import google.generativeai as genai
import torch.nn.functional as F
import torch



def get_embedding(text):
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=text,
        task_type="retrieval_document",
        title="Embedding of single string")
    
    return result['embedding']

# Give it two lists representing the embeddings
def calculate_cosine_similarity(embedding1, embedding2):
    vec1 = torch.tensor(embedding1, dtype=torch.float32)
    vec2 = torch.tensor(embedding2, dtype=torch.float32)

    vec1 = vec1.unsqueeze(0)
    vec2 = vec2.unsqueeze(0)

    cosine_sim = F.cosine_similarity(vec1, vec2)
    return cosine_sim.item()

if __name__ == "__main__":
    df = pd.read_csv("./Data/new_code_outputs_processed.csv")
    for index, row in df.iterrows():
        if pd.isna(row['code']) or pd.isna(row['obfuscatedCode']):
            print("NaN value")
            break
        fail = True 
        while fail:
            try:
                original_embedding = get_embedding(row['code'])
                obfuscated_embedding = get_embedding(row["obfuscatedCode"])
                fail = False
                print(f"Success for index {index}")
            except Exception as e:
                print(f"Failed for index {index} with error: {e}")
                sleep(5)
        
        similarity = calculate_cosine_similarity(original_embedding, obfuscated_embedding)
        df.at[index, "similarity"] = round(similarity, 4)
    
    
    df.to_csv("./Data/embedding_similarity_output.csv", index=False)
