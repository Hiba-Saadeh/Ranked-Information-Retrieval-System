import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import streamlit as st
import json
from rank_bm25 import BM25Okapi

nltk.download('punkt')
nltk.download('stopwords')

def process_text(text):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    return filtered_tokens

def extract_text_content(url):
    response = requests.get("https://en.wikipedia.org" + url)
    soup = BeautifulSoup(response.text, 'html.parser')
    content = ""
    for p_tag in soup.find_all('p'):
        content += p_tag.text.strip() + " "
    return content

def scrape_main_articles(topic):
    url = f"https://en.wikipedia.org/wiki/{topic}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    article_links = []
    for link in soup.find_all('div', {'class': 'mw-parser-output'}):
        for a in link.find_all('a', href=True):
            if "/wiki/" in a['href'] and ":" not in a['href']:
                article_links.append(a['href'])
    return article_links

def retrieve_articles(query, all_articles):
    tokenized_corpus = [process_text(article) for article in all_articles.values()]
    bm25 = BM25Okapi(tokenized_corpus)
    tokenized_query = process_text(query)
    doc_scores = bm25.get_scores(tokenized_query)
    sorted_indices = sorted(range(len(doc_scores)), key=lambda i: doc_scores[i], reverse=True)[:10]
    top_10_articles = [(list(all_articles.keys())[i], f"https://en.wikipedia.org/wiki/{list(all_articles.keys())[i].replace(' ', '_')}", doc_scores[i]) for i in sorted_indices]
    return top_10_articles

def main():
    st.title("Search Engine Using BM25")
    st.write("Welcome to the Wikipedia Article Search app!")
    st.write("Enter a topic of interest in the search box below to find relevant Wikipedia articles.")

    try:
        with open("stored_articles.json", "r") as f:
            all_articles = json.load(f)
    except FileNotFoundError:
        all_articles = {}
    
    query = st.text_input("Enter your search topic (e.g., 'Artificial Intelligence:")
    if st.button("Search"):
        with st.spinner("Searching for articles..."):
            if query.strip() == "":
                st.error("Please enter a query.")
            else:
                if not all_articles:
                    topics = ['Artificial_intelligence', 'Machine_learning', 'Data_science']
                    num_articles_per_topic = 17
                    
                    for topic in topics:
                        article_links = scrape_main_articles(topic)[:num_articles_per_topic]
                        for link in article_links:
                            response = requests.get("https://en.wikipedia.org" + link)
                            soup = BeautifulSoup(response.text, 'html.parser')
                            title = soup.find('h1', {'class': 'firstHeading'}).text
                            content = extract_text_content(link)
                            all_articles[title] = content
                    
                    # Store the scraped articles for future use
                    with open("stored_articles.json", "w") as f:
                        json.dump(all_articles, f)
                
                top_10_articles = retrieve_articles(query, all_articles)
                if not top_10_articles:
                    st.error("No relevant articles found.")
                else:
                    st.write("Top 10 Relevant Articles:")
                    for title, link, score in top_10_articles:
                        st.markdown(f"- [{title}]({link}) (BM25 Score: {score:.4f})")

if __name__ == "__main__":
    main()
