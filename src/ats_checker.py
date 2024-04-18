# import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv() ## load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
 

def get_gemini_response(job_description, resume_text):
    model = genai.GenerativeModel('gemini-pro')
    input_prompt = f"""
    Hey Act Like a skilled or very experienced ATS (Application Tracking System)
    with a deep understanding of tech field, software engineering, data science, data analysis,
    and big data engineering. Your task is to evaluate the resume based on the given job description.
    You must consider the job market is very competitive and you should provide 
    the best assistance for improving the resumes. Assign the percentage Matching based 
    on JD and the missing keywords with high accuracy. 
    resume: {resume_text}
    description: {job_description}
    """
    response = model.generate_content(input_prompt)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text



## streamlit app
# st.title("Smart ATS")
# st.text("Improve Your Resume ATS")
# job_description = st.text_area("Paste the Job Description")
# uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")

# submit = st.button("Submit")



# if submit:
#     if job_description and uploaded_file is not None:
#         resume_text = input_pdf_text(uploaded_file)
#         response = get_gemini_response(job_description, resume_text)
#         st.subheader("Response:")
#         st.write(response)
