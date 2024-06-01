# import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv() ## load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Hey Act Like a skilled or very experienced ATS (Application Tracking System)
# with a deep understanding of tech field. Your task is to evaluate the resume based on the given job description.
# You must consider the job market is very competitive and you should provide 
# the best assistance for improving the resumes. Assign the percentage Matching based 
# on Job Description and the missing keywords with high accuracy.

def get_gemini_response(job_description, resume_text):
    model = genai.GenerativeModel('gemini-pro')
    input_prompt =f""" you are software developer mentor and a student come to you , he want to beacome {job_description} developer and he gave you following resume data to you:{resume_text}.Your duty is to give him suggestions to improve his resume data.i Want following type of response.
:The response should be in json format as follows: '"percentage_match": which is a number,"missing_keywords":[array of missing keywords],"suggestions":[array of suggestions]', this should be in json object having follwing keys
 make sure that dont send empty arrays for missing skills and suggestion.  if null and empty string in value of json  Give positive feed back in same manner  With Displaying name of candidate"""
    


#      I want response in paragraph format in which  each paragraph in html p element. like :<div>
#    <p>answer </p>  <p>answer </p></div>. dont including headings or * in response
   
    
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
