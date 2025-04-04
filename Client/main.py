import streamlit as st
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Server.Input import Input
from Server import AnalyzerAgent
from Server.RecommenderAgent import RecommendationAgent
from langchain_core.caches import InMemoryCache
from langchain_core.globals import set_llm_cache
set_llm_cache(InMemoryCache())

course_data_file = "./Server/downsized_dataset.csv"
analyzer_agent = AnalyzerAgent.AnalyzerAgent()



st.title("Resume Analyzer")
st.info("A tool to check the compatibility of a client resume to job description")

st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQbxSJQjfrstR6vB4kNHKfNTfeI0JbnaooMzQ&s")

job_desc = st.text_area(label="Job Description", 
             placeholder="Enter job description here", height=300, key="job-desc-input")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"], key="resume-pdf-upload")
recommender_checked = st.checkbox("Recommend Courses")
submitted = st.button("Analyze", key="form-submit")


if submitted:
    if uploaded_file and job_desc:
    
        with st.spinner("Processing..."):
            resume_docs, _ = Input().read(uploaded_file)
            full_resume = " ".join([doc.page_content for doc in resume_docs])
            analysis_result = analyzer_agent.analyze_resume(full_resume, job_desc)
            st.write(analysis_result)

            if recommender_checked:
                
                st.header("\nCourse Recommendations")
                recommendation_agent = RecommendationAgent(course_data_file)
                unmatched_skills = []
                for line in analysis_result.split("\n"):
                    if "Unmatched Skills" in line:
                        unmatched_skills = line.split(":")[-1].strip().split(", ")
                    
                recommendations = recommendation_agent.recommend_courses(unmatched_skills) 
                st.write(recommendations)
        
    else:
        st.error("Please upload a resume and enter a job description to begin.")

