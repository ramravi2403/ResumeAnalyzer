import os
import shutil
from Server.Input import Input
from Server import AnalyzerAgent

from Server.RecommenderAgent import RecommendationAgent

# Path to the test resume PDF
resume_pdf_path = "./RaviRamResume.pdf"  # Change this to your PDF file

# Sample job description
job_description = """
We are looking for a Data Scientist with expertise in Python, machine learning, and deep learning.
Experience with NLP and cloud platforms (AWS, GCP, or Azure) is preferred.
Candidates should have strong problem-solving skills and a background in mathematics or statistics.
"""
job_description2 = """

Working at Atlassian Atlassians can choose where they work – whether in an office, from home, or a combination of the two. That way, Atlassians have more control over supporting their family, personal goals, and other priorities. We can hire people in any country where we have a legal entity. Interviews and onboarding are conducted virtually, a part of being a distributed-first company.

Atlassian is seeking a Senior Machine Learning Scientist to join our Central AI team located in Bellevue WA. The Central AI organization constructs the fundamental infrastructure, data pipeline, frameworks, models, and other capabilities to expedite AI feature development throughout the entire company.

Your future team

The Central AI org is part of the larger Atlassian Intelligence program. Its purpose is to accelerate AI innovation across all our products and platform, provide cohesive AI experiences and setup up an Atlassian AI infrastructure for the future.

While it's anticipated that the majority of AI-driven initiatives will be developed and executed by federated product teams within Atlassian, the role of Central AI is pivotal to this process. Central AI is tasked with constructing the underlying infrastructure and capacities, which are crucial for the seamless integration and optimal functionality of AI across various departments. By doing so, Central AI ensures that different teams within the organization do not work in silos but have access to a unified foundation that promotes efficiency and collaboration. Additionally, Central AI is responsible for developing some of the core shared experiences typical in the AI domain, such as search, knowledge discovery and conversation.


What you’ll do

As a Senior Machine Learning engineer, you will work on the development and implementation of the cutting edge machine learning algorithms, training sophisticated models, collaborating with product, engineering, and analytics teams, to build the AI functionalities into each Atlassian products and services. Your daily responsibilities will encompass a broad spectrum of tasks such as designing system and model architectures, conducting rigorous experimentation and model evaluations, and providing guidance to junior ML engineers. Your role is pivotal, stretching beyond these tasks, ensuring AI's transformative potential is realized across our offerings.


Your background

On the first day, we'll expect you to have

Bachelor's or Master's degree (preferably a Computer Science degree or equivalent experience)

3+ years of related industry experience in the data science domain

Expertise in Python or Java with and the ability to write performant production-quality code, familiarity with SQL, knowledge of Spark and cloud data environments (e.g. AWS, Databricks)

Experience building and scaling machine learning models in business applications using large amounts of data

Ability to communicate and explain data science concepts to diverse audiences, craft a compelling story

Focus on business practicality and the 80/20 rule; very high bar for output quality, but recognize the business benefit of "having something now" vs "perfection sometime in the future"

Agile development mindset, appreciating the benefit of constant iteration and improvement

It's great, but not required, if you have

Experience working in a consumer or B2C space for a SaaS product provider, or the enterprise/B2B space

Experience in developing deep learning-based models and working on LLM-related applications

Excelling in solving ambiguous and complex problems, being able to navigate through uncertain situations, breaking down complex challenges into manageable components and developing innovative solutions
"""
# Ensure the file exists
if not os.path.exists(resume_pdf_path):
    raise FileNotFoundError(f"Resume file '{resume_pdf_path}' not found!")

# Create a temporary directory
temp_dir = "temp"
os.makedirs(temp_dir, exist_ok=True)

try:
    # Load and split the PDF file
    resume_docs, _ = Input().read(resume_pdf_path)

    # Combine all document contents into one text string
    full_resume = " ".join([doc.page_content for doc in resume_docs])

    # Analyze the resume
    analyzer_agent = AnalyzerAgent.AnalyzerAgent()
    # analyzer_agent = AnalyzerAgentWithRecommendation('/Users/ramgopalravi/ResumeAnalyzer/Server/coursera_courses_english.csv')

    #analysis_result = analyzer_agent.analyze_resume(full_resume, job_description)

    # Print the results
    #print("\n===== Resume Analysis Result =====\n")
    #print(analysis_result)
    #unmatched_skills = []
    #for line in analysis_result.split("\n"):
    #    if "Unmatched Skills" in line:
    #        unmatched_skills = line.split(":")[-1].strip().split(", ")
    #print(unmatched_skills)
    unmatched_skills = ['NLP', 'cloud platforms (AWS', 'GCP', 'Azure)', 'background in mathematics or statistics']
    course_data_file = "./Server/coursera_courses_english.csv"

    # Initialize the Recommendation Agent
    recommendation_agent = RecommendationAgent(course_data_file)

    # Load courses and embed them
    embedded_courses = recommendation_agent.embed_courses()

    # List of unmatched skills (could come from the resume analysis)

    # Get course recommendations
    recommendations = recommendation_agent.recommend_courses(unmatched_skills)

    # Print the results
    print("\n===== Course Recommendations =====\n")
    print(recommendations)

    # Step 3: Recommend Courses for Unmatched Skills



finally:
    # Clean up temporary directory
    shutil.rmtree(temp_dir, ignore_errors=True)


def test():
    unidentified_skills = []
    for line in analysis_result.split('\n'):
        if 'Unmatched Skills' in line:
            unidentified_skills = line.split(':')[-1].strip().split(', ')

    # Get course recommendations
    recommended_courses = analyzer_agent.recommend_courses(unidentified_skills)

    print('Recommended Courses:')
    for course in recommended_courses:
        print(f"Title: {course['course_title']}")
        print(f"Organization: {course['course_organization']}")
        print(f"URL: {course['course_url']}")
        print('---')
    if unmatched_skills:
        recommendation_agent = RecommendationAgent(
            './Server/coursera_courses_english.csv')
        recommended_courses = recommendation_agent.recommend_courses(unmatched_skills)