import pandas as pd
from datetime import datetime

def compute_novelty_score(df, alpha=0.4, beta=0.4, gamma=0.2):
    current_year = datetime.now().year

    # Normalize citation count to novelty component
    df['novelty_citations'] = 1 / (1 + df['citation_count'])

    # Normalize recency: recent papers get higher score
    df['recency'] = (df['year'] - df['year'].min()) / (current_year - df['year'].min())

    # Compute novelty score
    df['novelty_score'] = alpha * df['novelty_citations'] + beta * df['max_similarity'] + gamma * df['recency']

    # Compute combined score: Novelty × Citation Count
    df['combined_score'] = df['novelty_score'] * df['citation_count']

    return df

if __name__ == '__main__':
    from similarity_computer import compute_similarities
    from data_loader import load_data

    papers, _, metrics = load_data('papers.csv', 'citations.csv', 'metrics.csv')
    df = compute_similarities(papers, metrics)
    df = compute_novelty_score(df)
    print(df[['id', 'novelty_score']].sort_values(by='novelty_score', ascending=False).head())
