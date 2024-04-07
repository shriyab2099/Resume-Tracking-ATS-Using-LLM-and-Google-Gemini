import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf

from dotenv import load_dotenv

load_dotenv() ## load all env variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Gemini pro response
def get_gemini_response(input):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(input)
    return response.text


##extract image from pdf
def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text = ""
    ##read each page
    for page in reader.pages:
        text += page.extract_text()  # Extract text from the page
    return text

##prompt template
input_prompt="""
Hey Act Like a skilled or very experience ATS (Application Tracking System)
with a deep understanding of tech field, software engineering, data science, data analyst 
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide
best assistance for improving the resumes. Assign the percentage Matching based
on Jd and
the missing keywords with high accuracy
resume: {text}
description: {jd}

I want the response in one single string having the structure
{{"JD Match" : "%","MissingKeywords:[]","Profile Summary:""}}
"""

# streamlit app
st.title("Smart ATS")
st.text("Improve your ATS")
jd=st.text_area("Paste the job description")
uploaded_file=st.file_uploader("Upload Your Resume", type="pdf", help="Please upload your file")

submit= st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt.format(text=text, jd=jd))
        st.subheader(response)
