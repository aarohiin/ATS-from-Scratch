import streamlit as st
import os
from collections import defaultdict
import spacy
import numpy as np
import PyPDF2

# Load SpaCy model with NER and word embeddings
nlp = spacy.load("en_core_web_md")

# Extract text from PDF using PyPDF2
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    pdf_text = ""
    for page in pdf_reader.pages:
        pdf_text += page.extract_text() or ""
    return pdf_text.strip()

# Compute a general ATS score based on common resume criteria
def compute_general_ats_score(resume_text):
    resume_doc = nlp(resume_text)
    
    # Criteria for general ATS score
    keyword_count = len([token for token in resume_doc if token.is_alpha])
    skill_count = len([token for token in resume_doc.ents if token.label_ == "SKILL"])
    readability_score = max(min((keyword_count / 500) * 100, 100), 0)  # Based on length
    skill_density_score = min((skill_count / keyword_count) * 100, 100) if keyword_count else 0
    
    # General ATS score calculation (weighted)
    ats_score = 0.4 * readability_score + 0.6 * skill_density_score
    
    return ats_score

# Analyze resume vs job description with enhanced scoring logic
def analyze_resume_vs_jd(resume_text, jd_text):
    resume_doc = nlp(resume_text)
    jd_doc = nlp(jd_text)

    # Extract keywords and entities from resume
    resume_keywords = {token.text.lower() for token in resume_doc if token.is_alpha}
    resume_skills = {token.text.lower() for token in resume_doc.ents if token.label_ == "SKILL"}

    # Extract keywords and entities from job description
    jd_keywords = {token.text.lower() for token in jd_doc if token.is_alpha}
    jd_skills = {token.text.lower() for token in jd_doc.ents if token.label_ == "SKILL"}

    # Calculate semantic similarity
    similarity_score = resume_doc.similarity(jd_doc)

    # Skills matching logic
    matched_skills = resume_skills.intersection(jd_skills)
    skills_match_percentage = len(matched_skills) / len(jd_skills) * 100 if jd_skills else 0

    # Work experience match based on keywords
    work_experience_match = 80 if any(word in resume_keywords for word in ["experience", "worked", "project", "managed", "lead"]) else 0

    # Education match based on degree keywords
    education_match = 70 if any(degree in resume_keywords for degree in ["bachelor", "master", "phd", "mba", "degree"]) else 0

    # Adjusted score calculation with weights
    job_title_match = similarity_score * 40
    skills_weighted_score = skills_match_percentage * 0.3
    total_score = job_title_match + skills_weighted_score + work_experience_match + education_match

    # Normalize the total score to fit in range (0-100)
    overall_match_percentage = min((total_score / 150) * 100, 100)

    # Compute general ATS score
    general_ats_score = compute_general_ats_score(resume_text)

    # Generate detailed response
    response = f"""
    **Overall Match Percentage:** {overall_match_percentage:.2f}% (Specific to Job Description)
    
    **Resume and Job Description Similarity Score:** {similarity_score:.2f}
    
    **Skills Match:** {skills_match_percentage:.2f}% (Weighted Score: {skills_weighted_score:.2f}/30)
    
    **Work Experience Match:** {work_experience_match}/80
    
    **Education Match:** {education_match}/70
    
    **Matched Skills:** {', '.join(matched_skills) if matched_skills else 'No specific skill match found'}
    
    **General ATS Score:** {general_ats_score:.2f}% (Not specific to any job description)
    """

    # Determine Resume Score (High, Medium, Low)
    resume_score = "High" if overall_match_percentage >= 80 else "Medium" if overall_match_percentage >= 50 else "Low"

    return response, overall_match_percentage, resume_score, general_ats_score

# Streamlit App Configuration
st.set_page_config(page_title="ATS Resume Expert", layout='wide')
st.header("ATS Tracking System")

# Upload multiple resumes and job descriptions
resume_files = st.file_uploader("Upload Resumes", type=["pdf"], accept_multiple_files=True)
jd_files = st.file_uploader("Upload Job Descriptions", type=["pdf"], accept_multiple_files=True)

# Create a dictionary to store the uploaded files
files = defaultdict(list)
for file in resume_files:
    files["resumes"].append(file)
for file in jd_files:
    files["jds"].append(file)

# Allow the user to select a resume and a job description
selected_resume = st.selectbox("Select Resume", files["resumes"])
selected_jd = st.selectbox("Select Job Description", files["jds"])

# Buttons for analysis
submit1 = st.button("Analyze Resume")
submit2 = st.button("Percentage Match")

if submit1 or submit2:
    if selected_resume and selected_jd:
        # Extract text from PDFs
        resume_text = extract_text_from_pdf(selected_resume)
        jd_text = extract_text_from_pdf(selected_jd)

        # Perform analysis
        analysis_response, resume_score_percentage, resume_score, general_ats_score = analyze_resume_vs_jd(resume_text, jd_text)

        st.subheader("Analysis of the Resume")
        st.write(analysis_response)
        st.write(f"**Resume Score:** {resume_score} (Based on Match Percentage: {resume_score_percentage:.2f}%)")
        st.write(f"**General ATS Score:** {general_ats_score:.2f}%")

        # Save analysis results if in training mode
        if st.checkbox("Save Analysis Results"):
            save_path = st.text_input("Enter file name to save results (without extension):")
            if save_path:
                with open(f"{save_path}.txt", "w") as f:
                    f.write(analysis_response)
                st.success(f"Results saved as {save_path}.txt")
    else:
        st.write("Please upload both a resume and a job description to proceed.")
