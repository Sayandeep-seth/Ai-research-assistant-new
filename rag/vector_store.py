from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

CHROMA_PATH = "data/vector_db"


def get_embeddings():

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


def get_vector_store():

    embeddings = get_embeddings()

    vectordb = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )

    return vectordb


def store_papers(papers):

    if papers is None or len(papers) == 0:
        return

    embeddings = get_embeddings()

    docs = []

    for p in papers:
        docs.append(Document(page_content=p))

    vectordb = Chroma.from_documents(
        docs,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )

    vectordb.persist()