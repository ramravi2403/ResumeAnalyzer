import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate


class AnalyzerAgent:
    def __init__(self):
        load_dotenv()
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
        self.__llm = ChatOpenAI(model_name="gpt-4-turbo")

    def analyze_resume(self,full_resume, job_description):

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

        return response.content
