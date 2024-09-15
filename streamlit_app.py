import streamlit as st
from PyPDF2 import PdfReader
import openai

# HTML template with basic styling
html_template = """
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
        }}
        h1, h2, h3 {{
            color: #333;
        }}
    </style>
</head>
<body>
    <h1>Professional Resume</h1>
    {resume_content}
</body>
</html>
"""

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()  # Extracting text from each page

    # Ensure text extracted is not empty or malformed
    if not text.strip():
        return None
    return text

# Function to split text into chunks that fit within OpenAI token limits
def split_text_to_fit_limit(text, max_tokens=1500):
    chunks = []
    words = text.split()

    current_chunk = []
    for word in words:
        if len(current_chunk) + len(word.split()) <= max_tokens:
            current_chunk.append(word)
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

# Function to generate an HTML resume using OpenAI
def generate_html_resume(pdf_text, api_key):
    openai.api_key = api_key
    chunks = split_text_to_fit_limit(pdf_text, max_tokens=2000)  # Split into chunks to avoid token limits
    
    resume_parts = []
    for chunk in chunks:
        prompt = f"Generate a professional HTML resume from the following extracted text:\n\n{chunk}"
        
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=2000
            )
            resume_parts.append(response['choices'][0]['text'])
        except Exception as e:
            return f"Error: {str(e)}"
    
    # Combine all parts and return final HTML content
    return html_template.format(resume_content="".join(resume_parts))

# Streamlit App
def main():
    st.title("PDF to HTML Resume Generator")
    
    # Input fields for API key and PDF upload
    api_key = st.text_input("Enter your OpenAI API key", type="password")
    pdf_file = st.file_uploader("Upload PDF File", type=["pdf"])

    # Generate resume button
    if pdf_file and api_key:
        pdf_text = extract_text_from_pdf(pdf_file)

        # If PDF text extraction fails
        if not pdf_text:
            st.error("The PDF content could not be extracted. Please check the file.")
        else:
            st.write("PDF text extracted successfully.")
            
            # Generate the HTML resume
            st.write("Generating the resume...")
            html_resume = generate_html_resume(pdf_text, api_key)
            
            if "Error" in html_resume:
                st.error(html_resume)
            else:
                # Display the generated HTML
                st.markdown(html_resume, unsafe_allow_html=True)

                # Download button for the generated HTML
                st.download_button(
                    label="Download HTML Resume",
                    data=html_resume,
                    file_name="resume.html",
                    mime="text/html"
                )

if __name__ == "__main__":
    main()
