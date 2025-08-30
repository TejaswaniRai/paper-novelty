# Paper Novelty Ranking Project

## Overview

This project presents a comprehensive framework for evaluating and ranking academic papers based on their novelty. Leveraging a combination of citation metrics, textual similarity, and temporal factors, the system quantifies the novelty of research contributions. Beyond paper-level analysis, the project extends to author-level insights, temporal trends, and interactive exploration, providing a multifaceted perspective on research impact and innovation.

## Features

### 1. Paper Novelty Scoring
- **Novelty Score Calculation:** Combines inverse citation count, maximum textual similarity to other papers, and recency to compute a composite novelty score.
- **Combined Ranking:** Introduces a combined score that multiplies novelty by citation count, balancing novelty with impact.

### 2. Author-Level Insights
- **Top Authors by Novelty:** Identifies leading authors based on average novelty scores of their publications.
- **Novelty vs Citations:** Visualizes the relationship between authors' average novelty and citation counts.
- **Co-Author Network:** Constructs and visualizes collaboration networks among authors, revealing research communities.

### 3. Temporal Trends
- **Novelty Over Time:** Tracks average novelty scores per year to identify evolving research trends.
- **Old vs New Comparison:** Compares novelty scores across publication years, highlighting shifts in research innovation.

### 4. Interactive Dashboard
- **Streamlit Web App:** Provides an intuitive interface for exploring papers, authors, and trends.
- **Dynamic Filtering:** Enables filtering by publication year and citation thresholds.
- **Multiple Views:** Includes tabs for overview, author insights, trends, co-author network, and rankings.
- **Visualizations:** Employs Plotly and Matplotlib for rich, interactive charts and network graphs.

## Data Inputs

- **papers.csv:** Contains paper metadata including ID, title, abstract, publication year, and authors.
- **citations.csv:** Records citation relationships between papers.
- **metrics.csv:** Includes citation counts and author metrics such as h-index.

## Architecture and Components

- **Data Loader:** Parses and cleans input CSV files.
- **Similarity Computer:** Calculates TF-IDF based textual similarity between paper abstracts.
- **Scorer:** Computes novelty and combined scores using weighted metrics.
- **Ranker:** Sorts papers by novelty and combined scores.
- **Visualizer:** Generates static plots and network graphs for insights.
- **Streamlit App:** Hosts the interactive dashboard for user-driven exploration.

## Installation and Setup

1. Clone the repository.
2. Ensure Python 3.8+ is installed.
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Prepare data files (`papers.csv`, `citations.csv`, `metrics.csv`).
5. Run the main pipeline:
   ```
   python main.py
   ```
6. Launch the interactive dashboard:
   ```
   python -m streamlit run app.py
   ```

## Usage

- Use the command-line pipeline to generate rankings and visualizations.
- Access the Streamlit dashboard at the following URLs for interactive analysis:
  - Local URL: `http://localhost:8501`
  - Network URL: `http://<your-network-ip>:8501`
- Explore different tabs to gain insights into paper novelty, author contributions, temporal trends, and collaboration networks.

## Contribution and Extension

This project serves as a foundation for advanced bibliometric analysis and can be extended with:
- Integration of additional metrics (e.g., altmetrics, social media impact).
- Enhanced natural language processing for deeper semantic analysis.
- Real-time data updates and integration with external databases.
- User authentication and personalized dashboards.

## License

This project is open-source and available under the MIT License.

## Contact

For questions or collaboration inquiries, please contact the project maintainer.

---

This README provides a detailed and polished description of the Paper Novelty Ranking Project, highlighting its technical sophistication and practical utility for research evaluation.
