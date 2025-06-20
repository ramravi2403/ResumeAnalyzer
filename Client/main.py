from ResumeAnalyzerUI import ResumeAnalyzerUI
import streamlit as st


def main():
    try:
        ui = ResumeAnalyzerUI()
        ui.run()
    except Exception as e:
        st.error(f"Failed to initialize application: {str(e)}")
        st.info("Please ensure all required files and dependencies are available.")


if __name__ == "__main__":
    main()