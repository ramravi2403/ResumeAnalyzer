import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

class AnalyzerAgent:
    def __init__(self):
        dotenv_path = Path('./.env')
        load_dotenv(dotenv_path=dotenv_path)
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
        self.__llm = ChatOpenAI(model_name="gpt-3.5-turbo")
        # self.coursera_courses = pd.read_csv(coursera_courses_filepath)

    def analyze_resume(self, full_resume, job_description):
        template = """
        You are an AI assistant specialized in resume analysis and recruitment. Analyze the given resume and compare it with the job description. 

        Example Response Structure:

        **OVERVIEW**:
        - **Match Percentage**: [Calculate overall match percentage between the resume and job description]
        - **Matched Skills**: [List the skills in job description that match the resume]
        - **Unmatched Skills**: [List the skills in the job description that are missing in the resume]

        **DETAILED ANALYSIS**:
        Provide a detailed analysis about:
        1. Overall match percentage between the resume and job description
        2. List of skills from the job description that match the resume
        3. List of skills from the job description that are missing in the resume

        **Additional Comments**:
        Additional comments about the resume and suggestions for the recruiter or HR manager.

        Resume: {resume}
        Job Description: {job_description}

        Analysis:
        """

        prompt = PromptTemplate(
            input_variables=["resume", "job_description"],
            template=template
        )

        chain = prompt | self.__llm
        response = chain.invoke({"resume": full_resume, "job_description": job_description})

        unmatched_skills = self.extract_unmatched_skills(response.content)

        # Get recommendations for missing skills
        # skill_recommendations = self.get_course_recommendations(unmatched_skills)
        print(unmatched_skills)
        return response.content
    


    def extract_unmatched_skills(self, analysis_response):
        # Simple extraction logic; could be more complex based on the response format
        # Assuming unmatched skills are listed in a section labeled "Unmatched Skills"
        unmatched_skills = []
        lines = analysis_response.split("\n")
        for line in lines:
            if line.startswith("- Unmatched Skills:"):
                unmatched_skills = line.split(":")[1].strip().split(", ")
        return unmatched_skills

    def get_course_recommendations(self, unmatched_skills):
        recommended_courses = []
        for skill in unmatched_skills:
            # Search for courses that cover the missing skill
            matching_courses = self.coursera_courses[self.coursera_courses['skills'].str.contains(skill, case=False, na=False)]
            for _, course in matching_courses.iterrows():
                recommended_courses.append({
                    "course_title": course['title'],
                    "course_url": course['url'],
                    "skills": course['skills']
                })
        return recommended_courses