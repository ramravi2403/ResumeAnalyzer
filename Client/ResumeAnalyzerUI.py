import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Server.ResumeAnalyzerApp import ResumeAnalyzerApp


class ResumeAnalyzerUI:
    def __init__(self):

        st.set_page_config(page_title="Resume Analyzer", layout="wide")
        self.app = ResumeAnalyzerApp()


    def render_header(self):
        st.title("📄 Resume Analyzer")
        st.info("A tool to check the compatibility of a client resume to job description")
        st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQbxSJQjfrstR6vB4kNHKfNTfeI0JbnaooMzQ&s")

    def render_input_section(self):
        job_desc = st.text_area(
            label="Job Description",
            placeholder="Enter job description here",
            height=300,
            key="job-desc-input"
        )

        uploaded_file = st.file_uploader(
            "Upload Resume (PDF)",
            type=["pdf"],
            key="resume-pdf-upload"
        )

        return job_desc, uploaded_file

    def render_recommendation_settings(self):
        recommender_checked = st.checkbox("Recommend Courses")
        if recommender_checked:
            col1, col2, col3 = st.columns(3)
            with col1:
                difficulty = st.selectbox("Select Difficulty", ["All", "Beginner", "Intermediate", "Advanced"])
            with col2:
                min_rating = st.slider("Minimum Rating", min_value=0.0, max_value=5.0, value=4.0, step=0.1)
            with col3:
                num_recommendations = st.slider("Courses per skill", min_value=1, max_value=5, value=2)

            user_context = st.text_input(
                "Extra preferences (e.g., cloud, short, hands-on)",
                placeholder="Additional context for course recommendations"
            )

            return recommender_checked, difficulty, min_rating, num_recommendations, user_context

        return recommender_checked, None, None, None, None

    def display_course_card(self, course_info):
        with st.container():
            col1, col2 = st.columns([3, 1])

            with col1:
                if course_info['course_link']:
                    st.markdown(f"### [{course_info['course_name']}]({course_info['course_link']})")
                else:
                    st.markdown(f"### {course_info['course_name']}")

                st.markdown(f"**🎓 University:** {course_info['university']}")
                st.markdown(f"**📖 Snippet:** {course_info['snippet']}")

            with col2:
                st.metric("⭐ Rating", course_info['rating'])
                st.markdown(f"**📊 Difficulty:** {course_info['difficulty']}")
                st.markdown(f"**🎯 Match Score:** {course_info['match_score']:.3f}")

            st.divider()

    def display_course_recommendations(self, recommendations):
        if not recommendations:
            st.success("🎉 Great! No unmatched skills found. Your resume seems well-aligned with the job description.")
            return
        skills = list(recommendations.keys())
        st.subheader("🔍 Detected Unmatched Skills")
        st.write(", ".join(skills))

        for i, (skill, data) in enumerate(recommendations.items()):
            st.subheader(f"📚 Recommendations for: **{skill}**")
            st.caption(f"🔎 Search Query: {data['query']}")

            if 'error' in data:
                st.error(f"Error: {data['error']}")
            elif data['courses']:
                for course_info in data['courses']:
                    self.display_course_card(course_info)
            else:
                st.warning(f"No courses found for '{skill}' with the specified filters. Try adjusting your criteria.")

            if i < len(recommendations) - 1:  # Add separator between skills
                st.markdown("---")

    def process_analysis(self, uploaded_file, job_desc, recommend_courses, difficulty, min_rating, num_recommendations,
                         user_context):
        with st.spinner("Processing resume and analyzing skills..."):
            try:
                resume_content = self.app.process_resume_file(uploaded_file)
                analysis_result = self.app.analyze_resume(resume_content, job_desc)
                st.header("📊 Resume Analysis Results")
                st.write(analysis_result)

                if recommend_courses:
                    st.header("🎓 Course Recommendations")
                    unmatched_skills = self.app.extract_unmatched_skills(analysis_result)
                    recommendations = self.app.get_course_recommendations(
                        unmatched_skills, difficulty, min_rating, num_recommendations, user_context
                    )
                    self.display_course_recommendations(recommendations)

            except Exception as e:
                st.error(f"An error occurred during processing: {str(e)}")

    def run(self):
        self.render_header()
        job_desc, uploaded_file = self.render_input_section()
        recommend_courses, difficulty, min_rating, num_recommendations, user_context = self.render_recommendation_settings()
        submitted = st.button("🚀 Analyze", key="form-submit", type="primary")
        if submitted:
            if uploaded_file and job_desc:
                self.process_analysis(
                    uploaded_file, job_desc, recommend_courses,
                    difficulty, min_rating, num_recommendations, user_context
                )
            else:
                st.error("⚠️ Please upload a resume and enter a job description to begin analysis.")


