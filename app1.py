from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai
import io
import base64
import PyPDF2 as pdf

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader(len(reader.pages)):
        page = reader.pages[page]
        text+=str(page.extract_text())
    return text

# Prompt template    
input_prompt = '''
Hey act like a skilled or a very experienced ATS(Application Tracking System) with a deep knowledge and understanding of the 
technical field software engineering, data science, data analysis and big data engineering. your task is to evaluate the resume 
based on the given job description. You must consider the job market to be very competitive and you should provide best assistance
for improving the resume.  Assign the percentage matching based on the job description and the missing keywords with high accuracy
resume:{text}
description:{jd}

I want the response in one single string having the structure {{"JD Match":"%","Missins Keywords:[]","Profile Summary ":""}}
'''
## Streamlit App

st.title("Smart ATS")
st.text("Improve your Resume ATS")
jd = st.text_area("Paste your JD here")
uploaded_file = st.file_uploader("Upload your resume(PDF)...", type=['pdf'], help=("Please upload the PDF"))

submit = st.button("Submit")


if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt)
        st.subheader(response)


