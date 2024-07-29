import matplotlib.pyplot as plt
import pandas as pd




if __name__ == "__main__":
    df = pd.read_csv("./Data/comparison_similarity.csv")
    
    # plt.figure(figsize=(10, 6))

    # # Offset x values to distinguish between the two types of similarity
    # x_values = range(len(df))
    # x_values_gemini = [x - 0.2 for x in x_values]
    # x_values_cosine = [x + 0.2 for x in x_values]

    # plt.scatter(x_values_gemini, df['geminiSimilarity'], color='blue', alpha=0.5, label='Gemini Similarity')
    # plt.scatter(x_values_cosine, df['cosineSimilarity'], color='green', alpha=0.5, label='Llama Similarity')

    # plt.title('Comparison of Gemini and Llama Similarities')
    # plt.xlabel('Row Index')
    # plt.ylabel('Similarity')
    # plt.legend()
    # plt.grid(True)

    # # Display plot
    # plt.show()

    # Histrogram

    # plt.figure(figsize=(10, 6))
    # plt.hist(df['cosineSimilarity'], bins=20, color='blue', alpha=0.7)
    # plt.title('Distribution of Llama Similarity')
    # plt.xlabel('Cosine Similarity')
    # plt.ylabel('Frequency')
    # plt.grid(True)

    
    # plt.show()


    # plt.figure(figsize=(10, 6))

    # # Plotting both histograms on the same plot
    # plt.hist(df['cosineSimilarity'], bins=20, color='blue', alpha=0.5, label='Llama Similarity')
    # plt.hist(df['geminiSimilarity'], bins=20, color='green', alpha=0.5, label='Gemini Similarity')

    # plt.title('Distribution of Llama Similarity vs Gemini Similarity')
    # plt.xlabel('Similarity')
    # plt.ylabel('Frequency')
    # plt.legend()
    # plt.grid(True)

    # # Display plot
    # plt.show()
    
    print(df.columns)