import os
import shutil
from Server.Input import Input
from Server import AnalyzerAgent

# Path to the test resume PDF
resume_pdf_path = "../RaviRamResume.pdf"  # Change this to your PDF file

# Sample job description
job_description = """
We are looking for a Data Scientist with expertise in Python, machine learning, and deep learning.
Experience with NLP and cloud platforms (AWS, GCP, or Azure) is preferred.
Candidates should have strong problem-solving skills and a background in mathematics or statistics.
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
    analysis_result = analyzer_agent.analyze_resume(full_resume, job_description)

    # Print the results
    print("\n===== Resume Analysis Result =====\n")
    print(analysis_result)

finally:
    # Clean up temporary directory
    shutil.rmtree(temp_dir, ignore_errors=True)
