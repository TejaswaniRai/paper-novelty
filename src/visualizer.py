import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from collections import defaultdict

def visualize(df):
    # Scatter plot: Citation count vs Novelty score
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='citation_count', y='novelty_score', hue='year', palette='viridis')
    plt.title('Citation Count vs Novelty Score')
    plt.xlabel('Citation Count')
    plt.ylabel('Novelty Score')
    plt.savefig('outputs/plots/citation_vs_novelty.png')
    plt.show()

    # Top novel papers by year
    top_per_year = df.sort_values('novelty_score', ascending=False).groupby('year').head(1)
    plt.figure(figsize=(10, 6))
    sns.barplot(data=top_per_year, x='year', y='novelty_score')
    plt.title('Top Novelty Score per Year')
    plt.xticks(rotation=45)
    plt.savefig('outputs/plots/top_novelty_by_year.png')
    plt.show()

    # Distribution of novelty scores
    plt.figure(figsize=(10, 6))
    sns.histplot(df['novelty_score'], bins=20, kde=True)
    plt.title('Distribution of Novelty Scores')
    plt.xlabel('Novelty Score')
    plt.savefig('outputs/plots/novelty_distribution.png')
    plt.show()

def visualize_authors(df):
    # Explode authors
    df_authors = df.assign(authors=df['authors'].str.split(', ')).explode('authors')

    # Top authors by average novelty
    top_authors = df_authors.groupby('authors')['novelty_score'].mean().sort_values(ascending=False).head(10)
    plt.figure(figsize=(10, 6))
    top_authors.plot(kind='bar')
    plt.title('Top Authors by Average Novelty Score')
    plt.ylabel('Average Novelty Score')
    plt.xticks(rotation=45)
    plt.savefig('outputs/plots/top_authors_novelty.png')
    plt.show()

    # Average novelty vs average citations per author
    author_stats = df_authors.groupby('authors').agg({'novelty_score': 'mean', 'citation_count': 'mean'})
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=author_stats, x='citation_count', y='novelty_score')
    plt.title('Average Novelty vs Average Citations per Author')
    plt.xlabel('Average Citation Count')
    plt.ylabel('Average Novelty Score')
    plt.savefig('outputs/plots/novelty_vs_citations_authors.png')
    plt.show()

def visualize_trends(df):
    # Average novelty per year
    yearly_avg = df.groupby('year')['novelty_score'].mean()
    plt.figure(figsize=(10, 6))
    yearly_avg.plot(kind='line', marker='o')
    plt.title('Average Novelty Score per Year')
    plt.ylabel('Average Novelty Score')
    plt.savefig('novelty_trends.png')
    plt.show()

    # Old vs new: year vs novelty, color by citations
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='year', y='novelty_score', size='citation_count', hue='citation_count', palette='coolwarm')
    plt.title('Novelty Score Over Time (Old vs New)')
    plt.xlabel('Year')
    plt.ylabel('Novelty Score')
    plt.savefig('old_vs_new.png')
    plt.show()

def visualize_coauthor_network(df):
    # Build co-author graph
    G = nx.Graph()
    for _, row in df.iterrows():
        authors = row['authors'].split(', ')
        for i in range(len(authors)):
            for j in range(i+1, len(authors)):
                G.add_edge(authors[i], authors[j])

    # Draw network
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=50, font_size=8)
    plt.title('Co-Author Network')
    plt.savefig('coauthor_network.png')
    plt.show()

if __name__ == '__main__':
    from src.ranker import rank_papers
    from src.scorer import compute_novelty_score
    from src.similarity_computer import compute_similarities
    from src.data_loader import load_data

    papers, _, metrics = load_data('data/papers.csv', 'data/citations.csv', 'data/metrics.csv')
    df = compute_similarities(papers, metrics)
    df = compute_novelty_score(df)
    ranked = rank_papers(df)
    visualize(ranked)
