from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")


class VectorStore:
    def create_vector_store(self, chunks):
        vector_store = FAISS.from_documents(
            documents=chunks,
            embedding=embeddings
        )
        return vector_store
