import os
import shutil
from Server.Input import Input
from Server import AnalyzerAgent

from Server.RecommenderAgent import RecommendationAgent

# Path to the test resume PDF
resume_pdf_path = "./RaviRamResume.pdf"  # Change this to your PDF file


with open("./Client/jd1.txt", "r") as file:
    job_description1 = file.read()

with open("./Client/jd2.txt", "r") as file:
    job_description2 = file.read()
    
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