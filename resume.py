import streamlit as st
import google.generativeai as genai
import PyPDF2
import docx
import numpy as np
import os
import time
import re
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your-gemini-api-key")
genai.configure(api_key=GEMINI_API_KEY)

# Define generation config
generation_config = genai.types.GenerationConfig(
    temperature=0.7,
    top_p=0.9,
    max_output_tokens=5000,
)


def extract_skills(resume_text):
            
    prompt = f"""
    You are a career assistant. From the following resume content, extract all the relevant professional skills.
    Include programming languages, tools, technologies, frameworks, cloud services, and soft skills.
    Return the result as a clean comma-separated list with no extra commentary.

    Resume:
    \"\"\"
    {resume_text}
    \"\"\"
    """

    try:
        response = genai.GenerativeModel("gemini-2.0-flash").generate_content(prompt)
        # Clean and split the response into a list
        raw_output = response.text.strip()
        skills = [skill.strip() for skill in raw_output.split(",") if skill.strip()]
        return skills
    except Exception as e:
        print("Error during Gemini skill extraction:", e)
        return []


# Function to read PDF file
def read_pdf(file):
    with open(file, "rb") as f:
        pdf_reader = PyPDF2.PdfReader(f)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Function to read DOCX file
def read_docx(file):
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text
    return text

# Function to get career paths based on skills using Gemini
def get_career_paths(skills):
    # Prompt Gemini with the extracted skills to generate a career path
    prompt = f" Act like you are reading skills from a resume of a person and Given the skills: {', '.join(skills)}, suggest some relevant career paths. And also suggest high paying job roles in each pathways"
    response = genai.GenerativeModel("gemini-2.0-flash").generate_content(prompt)
    return response.text

# Streamlit UI for file upload
def resume_analyzer():
    st.markdown("Resume Analyzer for Career Pathways")
    uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
    if uploaded_file:
        with st.chat_message("assistant"):
            with st.spinner("Analyzing resume..."):
                if uploaded_file.type == "application/pdf":
                    resume_text = read_pdf(uploaded_file)
                elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    resume_text = read_docx(uploaded_file)
                else:
                    resume_text = ""

                skills = extract_skills(resume_text)
                
                career_paths="Hello World"
                if skills:
                    st.write(f"Mentioned Skills in resume: {', '.join(skills)}")               
                    # Get career suggestions based on the skills

                    career_paths = get_career_paths(skills)
                    placeholder = st.empty()
                    displayed_text = ""
                    # Word-by-word streaming
                    blocks = re.split(r"(?<=\n)\n+", career_paths.strip())
                    for block in blocks:
                        block = block.strip()
                        words = block.split(" ")
                        for word in words:
                            displayed_text += word + " "
                            placeholder.markdown(displayed_text + "▌", unsafe_allow_html=True)
                            time.sleep(0.01)
                        displayed_text += "\n\n"
                        placeholder.markdown(displayed_text + "▌", unsafe_allow_html=True)
                        time.sleep(0.1)   
                    placeholder.markdown(displayed_text, unsafe_allow_html=True)
                else:
                    st.write("No skills were identified in your resume.")