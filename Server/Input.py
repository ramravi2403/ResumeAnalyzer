from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import tempfile

class Input:
    def __init__(self):
        self.__text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=100,
            chunk_overlap=20,
            separators=["\n\n", "\n", " ", ""], )

    def read(self, file):
        with tempfile.NamedTemporaryFile(suffix='.pdf') as tmp_file:
                tmp_file.write(file.getvalue())
                pdf_path = tmp_file.name
                pdf_loader = PyPDFLoader(pdf_path)
        
                documents = pdf_loader.load()
        chunks = self.__text_splitter.split_documents(documents)
        return documents, chunks