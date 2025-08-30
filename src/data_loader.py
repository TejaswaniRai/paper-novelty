import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download required NLTK data
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

def load_data(papers_file, citations_file, metrics_file):
    # Load CSVs
    papers_df = pd.read_csv(papers_file)
    citations_df = pd.read_csv(citations_file)
    metrics_df = pd.read_csv(metrics_file)

    # Clean text in papers
    papers_df['title'] = papers_df['title'].apply(clean_text)
    papers_df['abstract'] = papers_df['abstract'].apply(clean_text)

    return papers_df, citations_df, metrics_df

def clean_text(text):
    if pd.isna(text):
        return ''
    # Lowercase
    text = text.lower()
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = text.split()
    words = [word for word in words if word not in stop_words]
    # Lemmatize
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    return ' '.join(words)

if __name__ == '__main__':
    papers, citations, metrics = load_data('papers.csv', 'citations.csv', 'metrics.csv')
    print("Data loaded and cleaned.")
    print(papers.head())
