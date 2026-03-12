from langchain.embeddings import HuggingFaceEmbeddings
from config import EMBED_MODEL

def get_embeddings():
    return HuggingFaceEmbeddings(model_name=EMBED_MODEL)