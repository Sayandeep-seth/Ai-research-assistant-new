from rag.retriever import retrieve_papers


def build_rag_context(query):

    papers_context = retrieve_papers(query)

    if papers_context is None:
        return ""

    rag_context = f"""
    The following literature was retrieved from research papers.

    {papers_context}

    Use this information to generate research insights.
    """

    return rag_context