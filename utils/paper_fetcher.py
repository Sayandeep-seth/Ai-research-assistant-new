import requests
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor


# ---------------------------
# ARXIV API FETCH
# ---------------------------
def fetch_arxiv(topic):

    url = "http://export.arxiv.org/api/query"

    params = {
        "search_query": f"all:{topic}",
        "start": 0,
        "max_results": 20
    }

    papers = []

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:

            root = ET.fromstring(response.text)

            for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):

                title = entry.find("{http://www.w3.org/2005/Atom}title").text.strip()

                summary = entry.find("{http://www.w3.org/2005/Atom}summary").text.strip()

                link = entry.find("{http://www.w3.org/2005/Atom}id").text

                year = entry.find("{http://www.w3.org/2005/Atom}published").text[:4]

                papers.append({
                    "title": title,
                    "summary": summary[:300],
                    "year": year,
                    "citations": 0,
                    "source": "ArXiv",
                    "link": link
                })

    except Exception as e:
        print("ArXiv API error:", e)

    return papers


# ---------------------------
# SEMANTIC SCHOLAR FETCH
# ---------------------------
def fetch_semantic(topic):

    url = "https://api.semanticscholar.org/graph/v1/paper/search"

    params = {
        "query": topic,
        "limit": 10,
        "fields": "title,year,citationCount,abstract,url"
    }

    papers = []

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:

            data = response.json()

            for p in data.get("data", []):

                papers.append({
                    "title": p.get("title"),
                    "summary": (p.get("abstract") or "")[:300],
                    "year": p.get("year"),
                    "citations": p.get("citationCount", 0),
                    "source": "Semantic Scholar",
                    "link": p.get("url")
                })

    except Exception as e:
        print("Semantic Scholar API error:", e)

    return papers


# ---------------------------
# COMBINED FETCH (PARALLEL)
# ---------------------------
def get_papers(topic):

    with ThreadPoolExecutor() as executor:

        arxiv_future = executor.submit(fetch_arxiv, topic)
        semantic_future = executor.submit(fetch_semantic, topic)

        arxiv_papers = arxiv_future.result()
        semantic_papers = semantic_future.result()

    papers = arxiv_papers + semantic_papers

    # sort by citation count
    papers = sorted(papers, key=lambda x: x["citations"], reverse=True)

    return papers