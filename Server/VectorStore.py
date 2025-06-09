import pandas as pd
import os
import re
import unicodedata
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from tqdm import tqdm
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


os.environ["TOKENIZERS_PARALLELISM"] = "false"
DB_PATH = "./courses_db"


class VectorStore:
    def __init__(self, df_path, model_name="sentence-transformers/all-mpnet-base-v2"):
        self.vector_store = None
        self.df = pd.read_csv(df_path)
        self.vector_store = Chroma(
            collection_name="courses",
            persist_directory=DB_PATH,
            embedding_function=HuggingFaceEmbeddings(model_name=model_name)
        )
        self.retriever = None
        
    def __clean_text(self, text):
        text = unicodedata.normalize('NFKD', str(text)).encode('ASCII', 'ignore').decode('ASCII')
        text = re.sub(r'[^\w\s.,!?-]', '', str(text))
        return text.strip()
    
    def __index(self):
            docs = []
            ids = []
            with tqdm(self.df.iterrows()) as t:
                t.set_description("Indexing")
                for i, row in t:
                    row = row.map(self.__clean_text)
                    document = Document(
                        page_content="||".join([row["course_title"], row["course_skills"]]),
                        metadata={"course_rating": row["course_rating"]},
                        id = str(i)
                        )
                    ids.append(str(i))
                    docs.append(document)
                    
                
                self.vector_store.add_documents(documents=docs, ids=ids)
    
    def build(self ,rebuild=False):
        if not self.vector_store._collection.count() or rebuild:
            self.__index()
        return self
            
    def load_retriever(self, k=3):
        if self.retriever is None:
            self.retriever = self.vector_store.as_retriever(search_type="similarity",search_kwargs={'k':k})
        return self.retriever



def get_similar_courses(unmatched_skills):
    Q = vector_store.load_retriever(k=10).invoke(unmatched_skills)
    course_data = [str({"Course Title": title, "Skills": skills})
                 for doc in Q
                 for title, skills in [doc.page_content.split('||')]]
    return course_data



template = """
Given a list of unmatched skills, recommend the top 3 courses from the dataset below that will help the user acquire the missing skills.

Unmatched Skills: {unmatched_skills}

Available courses:\n\t{course_data}

Recommendations (top 3 courses):
"""

prompt = PromptTemplate(input_variables=["unmatched_skills", "course_data"], template=template)
    
        
if __name__ == "__main__":
    
    from pprint import pprint
    sample = "NLP, deep learning, cloud platforms (AWS, GCP, Azure), background in mathematics or statistics"
    courses_data_path = "Server/coursera_courses_english.csv" 
    
    vector_store = VectorStore(df_path=courses_data_path).build()

    
    def recommend_courses(unmatched_skills):
        similar = get_similar_courses(unmatched_skills)
        llm = ChatOpenAI(model_name="gpt-3.5-turbo")
        
        chain = prompt | llm
        response = chain.invoke({"unmatched_skills": unmatched_skills, "course_data": similar})
        return response.content

    print(recommend_courses(sample))