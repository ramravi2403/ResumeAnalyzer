import streamlit as st
from Client.AgentLoader import AgentLoader
from Server import Input
from langchain_core.caches import InMemoryCache
from langchain_core.globals import set_llm_cache
from Server.VectorStore import VectorStore


class ResumeAnalyzerApp:
    def __init__(self, csv_path: str = "./Server/coursera_courses.csv") -> None:
        self.vector_store = ResumeAnalyzerApp._load_vector_store(csv_path)
        self.analyzer_agent = ResumeAnalyzerApp._load_agents()

    @staticmethod
    @st.cache_resource
    def _load_vector_store(csv_path) -> VectorStore:
        with st.spinner("Loading vector database...."):
            return VectorStore(df_path=csv_path)

    @staticmethod
    @st.cache_resource
    def _load_agents():
        set_llm_cache(InMemoryCache())
        with st.spinner("Loading agents..."):
            analyzer_agent = AgentLoader.load('analyzer')
            # recommender_agent = AgentLoader.load('recommender', data_file=_self.course_data_file)
            return analyzer_agent

    def format_course_recommendation(self, skill, doc, score) -> dict:
        course_name = doc.metadata.get('Course Name', 'Course name not available')
        university = doc.metadata.get('University', 'University not specified')
        rating = doc.metadata.get('Course Rating', 'N/A')
        difficulty = doc.metadata.get('Difficulty Level', 'Not specified')
        course_link = doc.metadata.get('Course URL')

        return {
            'skill': skill,
            'course_name': course_name,
            'university': university,
            'rating': rating,
            'difficulty': difficulty,
            'match_score': score,
            'course_link': course_link,
            'snippet': doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
        }

    def extract_unmatched_skills(self, analysis_result):
        unmatched_skills = []
        for line in analysis_result.split("\n"):
            if "Unmatched Skills" in line:
                skills_text = line.split(":")[-1].strip()
                unmatched_skills = [skill.strip() for skill in skills_text.split(",") if skill.strip()]
                break
        return unmatched_skills

    def search_courses_for_skill(self, skill, difficulty=None, min_rating=0.0, num_recommendations=2, user_context=""):

        difficulty_filter = None if difficulty == "All" else difficulty
        query = f"Learn {skill} course"
        if user_context:
            query += f" {user_context}"

        try:
            results = self.vector_store.search_courses(
                query=query,
                k=num_recommendations,
                min_rating=min_rating,
                difficulty=difficulty_filter
            )
            return results, query
        except Exception as e:
            raise Exception(f"Error searching for courses related to '{skill}': {str(e)}")

    def analyze_resume(self, resume_content, job_description):
        if not self.analyzer_agent:
            raise Exception("Analyzer agent not initialized. Call initialize_resources() first.")
        return self.analyzer_agent.analyze_resume(resume_content, job_description)

    def process_resume_file(self, uploaded_file):
        resume_docs, _ = Input().read(uploaded_file)
        return " ".join([doc.page_content for doc in resume_docs])

    def get_course_recommendations(self, unmatched_skills, difficulty="All", min_rating=4.0, num_recommendations=2,
                                   user_context=""):
        recommendations = {}

        for skill in unmatched_skills:
            try:
                results, query = self.search_courses_for_skill(
                    skill, difficulty, min_rating, num_recommendations, user_context
                )

                course_info_list = []
                for doc, score in results:
                    course_info = self.format_course_recommendation(skill, doc, score)
                    course_info_list.append(course_info)

                recommendations[skill] = {
                    'query': query,
                    'courses': course_info_list
                }
            except Exception as e:
                recommendations[skill] = {
                    'query': f"Learn {skill} course",
                    'error': str(e),
                    'courses': []
                }

        return recommendations

