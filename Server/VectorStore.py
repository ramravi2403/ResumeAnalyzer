from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


class VectorStore:
    def __init__(self):
        self.vector_store = None
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

    def create_vector_store(self, chunks):
        vector_store = FAISS.from_documents(
            documents=chunks,
            embedding=self.embeddings
        )
        return vector_store

    def embed_text(self, text):
        """Generate embeddings for a given text."""
        return self.embeddings.embed_query(text)