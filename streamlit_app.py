import streamlit as st
from PyPDF2 import PdfReader
import openai
import os

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to generate HTML resume using OpenAI's API
def generate_html_resume(pdf_text, api_key):
    openai.api_key = api_key
    prompt = f"Generate a professional HTML resume from the following extracted text:\n\n{pdf_text}"
    
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=2000
        )
        return response['choices'][0]['text']
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    st.title("LinkedIn PDF to HTML Resume Generator")
    
    # Input OpenAI API Key
    api_key = st.text_input("Enter your OpenAI API key", type="password")
    
    # Upload PDF file
    pdf_file = st.file_uploader("Upload LinkedIn PDF", type=["pdf"])
    
    if pdf_file and api_key:
        # Extract text from the uploaded PDF
        with st.spinner("Extracting text from PDF..."):
            pdf_text = extract_text_from_pdf(pdf_file)
        
        # Generate HTML resume
        with st.spinner("Generating HTML resume..."):
            html_resume = generate_html_resume(pdf_text, api_key)
        
        # Display the generated HTML resume
        if html_resume:
            st.markdown(html_resume, unsafe_allow_html=True)
        
        # Download link for HTML file
        st.download_button(
            label="Download HTML Resume",
            data=html_resume,
            file_name="resume.html",
            mime="text/html"
        )

if __name__ == "__main__":
    main()
