import csv
import os
import re
import unicodedata
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI

os.environ["TOKENIZERS_PARALLELISM"] = "false"


class RecommendationAgent:
    def __init__(self, course_data_file, model_name="sentence-transformers/all-mpnet-base-v2"):
        self.course_data = self.load_and_clean_csv(course_data_file)
        self.embeddings_model = HuggingFaceEmbeddings(model_name=model_name)
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo")
        self.embedded_courses = self.embed_courses()

    def load_and_clean_csv(self, file_path):
        courses = []
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cleaned_row = {k: self.clean_text(v) for k, v in row.items()}
                courses.append(cleaned_row)
        return courses

    def clean_text(self, text):
        text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        return text.strip()

    def embed_courses(self):
        embedded_courses = []
        for course in self.course_data:
            text_to_embed = course["course_skills"]
            embedding = self.embeddings_model.embed_query(text_to_embed)
            embedded_courses.append({
                "embedding": embedding,
                "course_skills": course["course_skills"],
                "course_title": course["course_title"]
            })
        return embedded_courses

    def recommend_courses_by_similarity(self, unmatched_skills):
        unmatched_skills_text = " ".join(unmatched_skills)
        unmatched_skills_embedding = self.embeddings_model.embed_query(unmatched_skills_text)

        similarities = cosine_similarity(
            [unmatched_skills_embedding],
            [course["embedding"] for course in self.embedded_courses]
        )[0]

        top_indices = np.argsort(similarities)[-5:][::-1]  # Get top 5 similar courses
        return [self.course_data[i] for i in top_indices]

    def create_recommendation_prompt(self, unmatched_skills, course_data):
        template = """
        Given a list of unmatched skills, recommend the top 3 courses from the dataset below that will help the user acquire the missing skills.

        Unmatched Skills: {unmatched_skills}

        Available courses:
        {course_data}

        Recommendations (top 3 courses):
        """
        course_info = "\n".join(
            [f"Course Title: {course['course_title']}, Skills: {course['course_skills']}" for course in course_data]
        )
        prompt = PromptTemplate(input_variables=["unmatched_skills", "course_data"], template=template)
        return prompt.format(unmatched_skills=", ".join(unmatched_skills), course_data=course_info)

    def recommend_courses(self, unmatched_skills):
        similar_courses = self.recommend_courses_by_similarity(unmatched_skills)

        recommendation_prompt = self.create_recommendation_prompt(unmatched_skills, similar_courses)
        prompt = PromptTemplate.from_template(recommendation_prompt)
        chain = prompt | self.llm
        response = chain.invoke({"unmatched_skills": unmatched_skills, "course_data": similar_courses})

        return self.process_recommendations(response)

    def process_recommendations(self, response):
        print(response)
        recommendations = []
        for line in response.content.split('\n'):
            if line.strip().startswith("Course Title:"):
                recommendations.append(line.strip())
                if len(recommendations) == 3:
                    break
        return response.content

# Usage
# recommendation_agent = RecommendationAgent('path_to_your_course_data.csv')
# unmatched_skills = ["Python", "Data Analysis", "Machine Learning"]
# recommendations = recommendation_agent.recommend_courses(unmatched_skills)
# print(recommendations)