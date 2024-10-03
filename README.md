# Metaverse Knowledge Graph Construction Using Web Scraping and Neo4j

This project focuses on constructing a domain-specific knowledge graph for the metaverse by leveraging web scraping techniques, natural language processing (NLP), and graph databases. The goal is to extract and visualize relationships between entities in the metaverse field, providing insightful analysis for researchers and industry professionals.

Memebers: Qing (Serena) Xue, Li Jiang, Xingyi Du, Minqi Zhou

## Project Overview

- **Domain**: Metaverse
- **Core Technologies**: Python, Selenium, BeautifulSoup, PyLTP, Neo4j
- **Objective**: To construct a knowledge graph representing relationships within the metaverse domain by extracting structured information from web articles.

## Key Features

1. **Web Scraping**: Collected over 170 articles from the "Metaverse Observation" section of The Paper using Selenium for JavaScript-rendered content and BeautifulSoup for HTML parsing.
2. **Triple Extraction**: Used PyLTP, a Chinese NLP toolkit, to extract subject-predicate-object triples from the articles, obtaining over 18,000 meaningful relationships.
3. **Knowledge Graph Construction**: Created nodes and relationships from extracted triples in Neo4j, facilitating visual exploration of trends and relationships in the metaverse.

## Technologies Used

- **Python**: Main programming language for the project.
- **Selenium**: Used for web scraping, simulating user interactions to extract JavaScript-rendered content.
- **BeautifulSoup**: HTML parsing to retrieve structured content from web pages.
- **PyLTP**: NLP toolkit used for dependency parsing and triple extraction.
- **Neo4j**: Graph database for storing and visualizing the knowledge graph.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/username/metaverse-knowledge-graph.git
   ```
2. Set up a virtual environment and install the required packages:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```
3. Start Neo4j:
   - Download and install Neo4j from [neo4j.com](https://neo4j.com/download/).
   - Start the Neo4j server and set up credentials as required.

## Usage

1. **Run the Web Scraper**: Use `spider.py` to scrape articles from the specified website.
   ```bash
   python spider.py
   ```
2. **Triple Extraction**: Extract triples from the scraped articles using `triple_extraction.py`.
   ```bash
   python triple_extraction.py
   ```
3. **Construct Knowledge Graph**: Use `to_neo4j.py` to create nodes and relationships in Neo4j.
   ```bash
   python to_neo4j.py
   ```

## Results

The final knowledge graph visualizes relationships among entities such as companies, technologies, and key figures in the metaverse domain. This visualization helps uncover patterns and insights into the evolving landscape of the metaverse.

## Future Work

- **Data Quality Improvement**: Enhance named entity recognition and semantic role labeling to improve the accuracy of relationships.
- **Coreference Resolution**: Implement coreference resolution to better handle pronouns and ambiguous references in text.
