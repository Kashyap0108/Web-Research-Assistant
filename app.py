import streamlit as st
from utils.search_utils import perform_web_search
from utils.content_extractor import extract_content
from utils.llm_handler import generate_report
from utils.document_generator import generate_pdf, generate_docx
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page config at the very beginning
st.set_page_config(
    page_title="Web Research Assistant",
    layout="wide"
)

def main():
    st.title("Web Research Assistant")
    
    # Get API keys from environment variables or Streamlit secrets
    gemini_api_key = os.getenv("GEMINI_API_KEY") or st.secrets["GEMINI_API_KEY"]
    serpapi_key = os.getenv("SERPAPI_KEY") or st.secrets["SERPAPI_KEY"]
    
    with st.form("search_form"):
        query = st.text_input("Enter your research query:")
        report_length = st.selectbox(
            "Select report length:",
            ["Short", "Medium", "Detailed"]
        )
        submitted = st.form_submit_button("Generate Report")
        
    if submitted and query:
        try:
            with st.spinner("🔍 Searching the web..."):
                search_results = perform_web_search(query, serpapi_key)
                
            if not search_results:
                st.error("No search results found. Please try a different query.")
                return
                
            with st.spinner("📑 Extracting content..."):
                content = extract_content(search_results)
                
            with st.spinner("🤖 Generating report..."):
                report = generate_report(content, report_length, gemini_api_key)
                
            if report is None:
                st.warning("Could not generate the report. Please try again later.")
                return
                
            st.success("Report generated successfully!")
            
            # Display the report
            st.markdown("### Generated Report")
            st.markdown(report)
            
            # Export options
            col1, col2 = st.columns(2)
            
            # Convert report to PDF
            pdf_content = generate_pdf(report)
            col1.download_button(
                "Download PDF",
                data=pdf_content,
                file_name="research_report.pdf",
                mime="application/pdf"
            )
            
            # Convert report to DOCX
            docx_content = generate_docx(report)
            col2.download_button(
                "Download DOCX",
                data=docx_content,
                file_name="research_report.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.info("Please try again or contact support if the problem persists.")

if __name__ == "__main__":
    main()
