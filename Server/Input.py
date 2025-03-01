from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


class Input:
    def __init__(self):
        self.__text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=100,
            chunk_overlap=20,
            separators=["\n\n", "\n", " ", ""], )

    def read(self, file_path):
        pdf_loader = PyPDFLoader(file_path)
        documents = pdf_loader.load()
        chunks = self.__text_splitter.split_documents(documents)
        return documents, chunks
