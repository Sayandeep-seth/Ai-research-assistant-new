from utils.paper_fetcher import get_papers
from utils.s3_fetcher import fetch_papers_from_s3


def run_literature_agent(topic):

    print("\n==============================")
    print("Running Literature Agent")
    print("Topic:", topic)
    print("==============================")

    # ----------------------------
    # Fetch live papers
    # ----------------------------

    live_papers = []

    try:

        print("Fetching papers from ArXiv / Semantic Scholar...")

        live_papers = get_papers(topic)

        print("Live papers fetched:", len(live_papers))

    except Exception as e:

        print("ERROR fetching live papers:", str(e))


    # ----------------------------
    # Fetch S3 papers
    # ----------------------------

    s3_papers = []

    try:

        print("Fetching papers from AWS S3...")

        s3_papers = fetch_papers_from_s3()

        print("S3 papers fetched:", len(s3_papers))

    except Exception as e:

        print("ERROR fetching S3 papers:", str(e))


    # ----------------------------
    # Merge papers
    # ----------------------------

    all_papers = live_papers + s3_papers

    print("Total papers returned:", len(all_papers))
    print("==============================\n")

    return all_papers