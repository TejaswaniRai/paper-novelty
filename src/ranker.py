import pandas as pd

def rank_papers(df):
    # Sort by novelty_score descending
    ranked_df = df.sort_values(by='novelty_score', ascending=False).reset_index(drop=True)
    return ranked_df

def rank_papers_combined(df):
    # Sort by combined_score descending
    ranked_df = df.sort_values(by='combined_score', ascending=False).reset_index(drop=True)
    return ranked_df

if __name__ == '__main__':
    from scorer import compute_novelty_score
    from similarity_computer import compute_similarities
    from data_loader import load_data

    papers, _, metrics = load_data('papers.csv', 'citations.csv', 'metrics.csv')
    df = compute_similarities(papers, metrics)
    df = compute_novelty_score(df)
    ranked = rank_papers(df)
    print(ranked[['id', 'title', 'novelty_score']].head(10))
