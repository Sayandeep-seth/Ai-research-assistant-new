from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from config import CHROMA_PATH, EMBED_MODEL


def get_vector_db():

    embedding_model = HuggingFaceEmbeddings(
        model_name=EMBED_MODEL
    )

    vector_db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding_model
    )

    return vector_db


def store_papers(papers):

    vector_db = get_vector_db()

    texts = []
    metadata = []

    for p in papers:
        texts.append(p["summary"])
        metadata.append({
            "title": p["title"],
            "link": p["link"]
        })

    vector_db.add_texts(texts, metadatas=metadata)


def retrieve_papers(query, k=5):

    vector_db = get_vector_db()

    docs = vector_db.similarity_search(query, k=k)

    return docs