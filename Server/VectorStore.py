import pandas as pd
import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

os.environ["TOKENIZERS_PARALLELISM"] = "false" #remove?
DB_PATH = "./Server/courses_db"


class VectorStore:
    def __init__(self, df_path, validate=False) -> None:
        load_dotenv()
        if os.path.exists(DB_PATH) and len(os.listdir(DB_PATH)) > 0:
            print("Loading existing vector db.....")
            self.vector_store = Chroma(persist_directory=DB_PATH, embedding_function=HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-mpnet-base-v2"), collection_name="courses")
        else:
            print("Creating new vector store....")
            self.vector_store = self.__create_vector_store(df_path)
        self.retriever = None
        if validate:
            self.validate_vector_store_size(df_path)

    def __create_vector_store(self, df_path: str) -> Chroma:
        df = pd.read_csv(df_path)
        texts = df['Course Name'] + ". " + df['Course Description'] + ". Skills: " + df['Skills'].fillna('')
        metadata = df[['Course Name', 'Course Rating', 'Difficulty Level', 'University', 'Course URL']].to_dict(orient="records")
        ids = df.index.astype(str).tolist()

        return Chroma.from_texts(
            texts=texts.tolist(),
            embedding=HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2"),
            metadatas=metadata,
            ids=ids,
            collection_name="courses",
            persist_directory=DB_PATH
        )

    def search_courses(self, query: str, k: int = 3, min_rating: float = 0.0, difficulty: str = None):
        results = self.vector_store.similarity_search_with_score(query, k=k * 2)  # Get more results for filtering
        filtered_results = []
        for doc, score in results:
            try:
                course_rating = doc.metadata.get('Course Rating', 0)
                if isinstance(course_rating, str):
                    try:
                        course_rating = float(course_rating)
                    except (ValueError, TypeError):
                        course_rating = 0.0

                if course_rating >= min_rating:
                    if difficulty and difficulty.lower() in ['beginner', 'intermediate', 'advanced']:
                        doc_difficulty = doc.metadata.get('Difficulty Level', '').lower()
                        if difficulty.lower() == doc_difficulty:
                            filtered_results.append((doc, score))
                    else:
                        filtered_results.append((doc, score))

            except Exception as e:
                filtered_results.append((doc, score))
        return filtered_results[:k]

    def validate_vector_store_size(self, df_path: str) -> bool:
        try:
            df = pd.read_csv(df_path)
            csv_count = len(df)
            collection = self.vector_store._collection
            vector_count = collection.count()

            print(f"\n=== Vector Store Validation ===")
            print(f"CSV records: {csv_count}")
            print(f"Vector store records: {vector_count}")

            if csv_count == vector_count:
                print("✅ Vector store size matches CSV records!")
            else:
                print("Vector store size does NOT match CSV records!")
                print(f"   Difference: {abs(csv_count - vector_count)} records")

            return csv_count == vector_count

        except Exception as e:
            print(f"Error validating vector store size: {e}")
            return False

    def get_vector_store(self) -> Chroma:
        return self.vector_store


if __name__ == "__main__":
    vs = VectorStore(df_path="coursera_courses.csv")  # adjust path if needed

    query = "Recommend a Beginner course to learn Deep learning. specialization"
    results = vs.vector_store.similarity_search(query, k=1)

    for i, doc in enumerate(results, 1):
        print(f"Result {i}")
        print(f"Text: {doc.page_content[:200]}...")  # truncate for brevity
        print(f"Metadata: {doc.metadata}")
        print("—" * 50)
