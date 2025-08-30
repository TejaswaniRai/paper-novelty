from src.data_loader import load_data
from src.similarity_computer import compute_similarities
from src.scorer import compute_novelty_score
from src.ranker import rank_papers, rank_papers_combined
from src.visualizer import visualize, visualize_authors, visualize_trends, visualize_coauthor_network

def main():
    # Load data
    papers, citations, metrics = load_data('data/papers.csv', 'data/citations.csv', 'data/metrics.csv')

    # Compute similarities
    df = compute_similarities(papers, metrics)

    # Compute novelty scores
    df = compute_novelty_score(df)

    # Rank papers
    ranked_df = rank_papers(df)

    # Visualize
    visualize(ranked_df)
    visualize_authors(ranked_df)
    visualize_trends(ranked_df)
    visualize_coauthor_network(ranked_df)

    # Rank by combined score
    combined_ranked = rank_papers_combined(df)
    print("Top 5 by Combined Score:")
    print(combined_ranked[['id', 'title', 'combined_score']].head(5))

    # Print top 5
    print("Top 5 Novel Papers:")
    print(ranked_df[['id', 'title', 'novelty_score']].head(5))

if __name__ == '__main__':
    main()
