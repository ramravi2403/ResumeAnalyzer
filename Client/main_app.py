import streamlit as st
import os
import shutil
import tempfile
from backend.pdf_ingestion import load_split_pdf
from backend.vector_store import create_vector_store
from backend.analysis import analyze_resume

def render_main_app():
    # Apply custom CSS to adjust the sidebar width
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            min-width: 25%;
            max-width: 25%;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    with st.sidebar:
        st.header("Upload Resume")
        resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
        job_description = st.text_area("Enter Job Description", height=300)

        if resume_file and job_description:
            with tempfile.TemporaryDirectory() as temp_dir:
                resume_path = os.path.join(temp_dir, resume_file.name)
                with open(resume_path, "wb") as f:
                    f.write(resume_file.getbuffer())
                
                try:
                    with st.spinner("Processing resume..."):
                        resume_docs, resume_chunks = load_split_pdf(resume_path)
                        vector_store = create_vector_store(resume_chunks)
                        st.session_state.vector_store = vector_store
                    
                    if st.button("Analyze Resume", help="Click to analyze the resume"):
                        with st.spinner("Analyzing resume against job description..."):
                            full_resume = " ".join([doc.page_content for doc in resume_docs])
                            analysis = analyze_resume(full_resume, job_description)
                            st.session_state.analysis = analysis
                            st.success("Analysis Complete")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.info("Please upload a resume and enter a job description to begin.")
    
    if "analysis" in st.session_state:
        st.header("Resume-Job Compatibility Analysis")
        st.write(st.session_state.analysis)
    else:
        st.header("Resume Analysis Tool")
        st.info("Tool to check compatibility of client resume to job description.")
        todo = ["Upload a Resume", "Enter a Job Description", "Click on Analyze Resume"]
        st.markdown("\n".join([f"##### {i+1}. {item}" for i, item in enumerate(todo)]))
