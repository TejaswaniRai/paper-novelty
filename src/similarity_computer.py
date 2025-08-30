import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def compute_similarities(papers_df, metrics_df):
    # Merge papers with metrics
    df = pd.merge(papers_df, metrics_df, left_on='id', right_on='paper_id', how='left')

    # Fill NaN citations with 0
    df['citation_count'] = df['citation_count'].fillna(0)
    df['h_index'] = df['h_index'].fillna(0)

    # Combine title and abstract for text
    df['text'] = df['title'] + ' ' + df['abstract']

    # TF-IDF vectorization
    vectorizer = TfidfVectorizer(max_features=1000)
    tfidf_matrix = vectorizer.fit_transform(df['text'])

    # Identify high-impact papers: top 50% by citation_count
    threshold = df['citation_count'].quantile(0.5)
    high_impact_indices = df[df['citation_count'] >= threshold].index

    # Compute similarities
    similarities = cosine_similarity(tfidf_matrix)

    # For each paper, max similarity to high-impact papers
    max_similarities = []
    for i in range(len(df)):
        if i in high_impact_indices:
            # For high-impact, similarity to others, but perhaps exclude self
            sims = similarities[i, high_impact_indices]
            sims = sims[sims < 1]  # exclude self if 1
            max_sim = np.max(sims) if len(sims) > 0 else 0
        else:
            sims = similarities[i, high_impact_indices]
            max_sim = np.max(sims) if len(sims) > 0 else 0
        max_similarities.append(max_sim)

    df['max_similarity'] = max_similarities
    return df

if __name__ == '__main__':
    from data_loader import load_data
    papers, _, metrics = load_data('papers.csv', 'citations.csv', 'metrics.csv')
    df = compute_similarities(papers, metrics)
    print(df[['id', 'max_similarity']].head())
