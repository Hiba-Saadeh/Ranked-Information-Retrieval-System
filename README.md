# Wikipedia Article Search Engine

This repository contains a search engine for Wikipedia articles using the BM25 algorithm. The search engine is built with Streamlit and demonstrates text processing, web scraping, and information retrieval.

## Features
- Web Scraping: Scrapes Wikipedia articles related to specific topics.
- Text Processing: Processes and tokenizes the text content of articles.
- Information Retrieval: Uses the BM25 algorithm to rank articles based on relevance to the user's query.
- User Interface: Provides an interactive interface to enter search queries and display the top relevant articles.

## File Structure
- Information_Retrieval_Project.ipynb: Main Jupyter notebook containing the project code and explanations.
- app.py: Main application script containing the Streamlit app and the search engine logic.
- stored_articles.json: JSON file to store the scraped articles for future use (created during the first run).
