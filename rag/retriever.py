from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

CHROMA_PATH = "data/vector_db"


def get_retriever():

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )

    retriever = vectordb.as_retriever(
        search_kwargs={"k": 5}
    )

    return retriever


def retrieve_papers(query):

    retriever = get_retriever()

    docs = retriever.get_relevant_documents(query)

    if not docs:
        return ""

    context = "\n\n".join([doc.page_content for doc in docs])

    return context