import streamlit as st
import pandas as pd
import plotly.express as px
import networkx as nx
import matplotlib.pyplot as plt
from src.data_loader import load_data
from src.similarity_computer import compute_similarities
from src.scorer import compute_novelty_score
from src.ranker import rank_papers, rank_papers_combined

# Load and process data
@st.cache_data
def load_processed_data():
    papers, _, metrics = load_data('data/papers.csv', 'data/citations.csv', 'data/metrics.csv')
    df = compute_similarities(papers, metrics)
    df = compute_novelty_score(df)
    return df

df = load_processed_data()
ranked_novelty = rank_papers(df)
ranked_combined = rank_papers_combined(df)

st.title('Paper Novelty Ranking Dashboard')

# Sidebar
st.sidebar.header('Filters')
year_range = st.sidebar.slider('Year Range', int(df['year'].min()), int(df['year'].max()), (int(df['year'].min()), int(df['year'].max())))
citation_min = st.sidebar.slider('Min Citations', 0, int(df['citation_count'].max()), 0)

filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1]) & (df['citation_count'] >= citation_min)]

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(['Overview', 'Author Insights', 'Trends', 'Co-Author Network', 'Rankings'])

with tab1:
    st.header('Overview')
    fig = px.scatter(filtered_df, x='citation_count', y='novelty_score', color='year', hover_data=['title', 'authors'])
    st.plotly_chart(fig)

    fig2 = px.histogram(filtered_df, x='novelty_score', nbins=20)
    st.plotly_chart(fig2)

with tab2:
    st.header('Author Insights')
    # Explode authors
    df_authors = filtered_df.assign(authors=filtered_df['authors'].str.split(', ')).explode('authors')
    top_authors = df_authors.groupby('authors')['novelty_score'].mean().sort_values(ascending=False).head(10)
    fig = px.bar(top_authors, x=top_authors.index, y=top_authors.values)
    st.plotly_chart(fig)

    author_stats = df_authors.groupby('authors').agg({'novelty_score': 'mean', 'citation_count': 'mean'})
    fig2 = px.scatter(author_stats, x='citation_count', y='novelty_score', hover_name=author_stats.index)
    st.plotly_chart(fig2)

with tab3:
    st.header('Trends Over Time')
    yearly_avg = filtered_df.groupby('year')['novelty_score'].mean()
    fig = px.line(yearly_avg, x=yearly_avg.index, y=yearly_avg.values, markers=True)
    st.plotly_chart(fig)

    fig2 = px.scatter(filtered_df, x='year', y='novelty_score', size='citation_count', color='citation_count', hover_data=['title'])
    st.plotly_chart(fig2)

with tab4:
    st.header('Co-Author Network')
    # Build graph
    G = nx.Graph()
    for _, row in filtered_df.iterrows():
        authors = row['authors'].split(', ')
        for i in range(len(authors)):
            for j in range(i+1, len(authors)):
                G.add_edge(authors[i], authors[j])

    # Plot with matplotlib since plotly network is complex
    fig, ax = plt.subplots(figsize=(10, 8))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=50, font_size=8, ax=ax)
    st.pyplot(fig)

with tab5:
    st.header('Rankings')
    ranking_type = st.selectbox('Ranking Type', ['Novelty Score', 'Combined Score'])
    if ranking_type == 'Novelty Score':
        ranked = ranked_novelty
    else:
        ranked = ranked_combined

    st.dataframe(ranked[['id', 'title', 'authors', 'novelty_score', 'combined_score', 'citation_count']].head(20))
