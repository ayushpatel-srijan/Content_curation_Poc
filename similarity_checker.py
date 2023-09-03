import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SentenceSimilarityChecker:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.cosine_similarities_df = None

    def calculate_similarity(self, sentences):
        # Preprocess the sentences and create TF-IDF vectors
        tfidf_matrix = self.vectorizer.fit_transform(sentences)

        # Calculate the cosine similarity matrix
        cosine_similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)

        # Convert the cosine similarity matrix to a DataFrame
        self.cosine_similarities_df = pd.DataFrame(cosine_similarities, columns=sentences, index=sentences)

    def group_similar_sentences(self, sentences, threshold=0.2):
        self.calculate_similarity(sentences)
        groups = []
        visited = set()
        for i, sentence in enumerate(self.cosine_similarities_df.columns):
            if sentence not in visited:
                group = {self.cosine_similarities_df.columns[j] for j, score in enumerate(self.cosine_similarities_df.iloc[i]) if score > threshold}
                visited.update(group)
                groups.append(group)

        return groups


# if __name__ == "__main__":
#     sentences = [
#         "This is sentence 1.",
#         "Another sentence.",
#         "A similar sentence.",
#         "Different sentence here.",
#         "Sentence 5."
#     ]
#
#     checker = SentenceSimilarityChecker()
#     checker.calculate_similarity(sentences)
#     similarity_groups = checker.group_similar_sentences()
#     print("Similarity groups:")
#     for group in similarity_groups:
#         print(group)
