from flask import Flask, request, render_template
import os
from collections import defaultdict
import spacy
import numpy as np
import PyPDF2

# Initialize Flask app
app = Flask(__name__)

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
    keyword_count = len([token for token in resume_doc if token.is_alpha])
    skill_count = len([token for token in resume_doc.ents if token.label_ == "SKILL"])
    readability_score = max(min((keyword_count / 500) * 100, 100), 0)
    skill_density_score = min((skill_count / keyword_count) * 100, 100) if keyword_count else 0
    ats_score = 0.4 * readability_score + 0.6 * skill_density_score
    return ats_score

# Analyze resume vs job description with enhanced scoring logic
def analyze_resume_vs_jd(resume_text, jd_text):
    resume_doc = nlp(resume_text)
    jd_doc = nlp(jd_text)
    
    resume_keywords = {token.text.lower() for token in resume_doc if token.is_alpha}
    resume_skills = {token.text.lower() for token in resume_doc.ents if token.label_ == "SKILL"}

    jd_keywords = {token.text.lower() for token in jd_doc if token.is_alpha}
    jd_skills = {token.text.lower() for token in jd_doc.ents if token.label_ == "SKILL"}

    similarity_score = resume_doc.similarity(jd_doc)
    matched_skills = resume_skills.intersection(jd_skills)
    skills_match_percentage = len(matched_skills) / len(jd_skills) * 100 if jd_skills else 0

    work_experience_match = 80 if any(word in resume_keywords for word in ["experience", "worked", "project", "managed", "lead"]) else 0
    education_match = 70 if any(degree in resume_keywords for degree in ["bachelor", "master", "phd", "mba", "degree"]) else 0

    job_title_match = similarity_score * 40
    skills_weighted_score = skills_match_percentage * 0.3
    total_score = job_title_match + skills_weighted_score + work_experience_match + education_match

    overall_match_percentage = min((total_score / 150) * 100, 100)
    general_ats_score = compute_general_ats_score(resume_text)

    response = f"""
    <b>Overall Match Percentage:</b> {overall_match_percentage:.2f}% (Specific to Job Description)<br>
    <b>Resume and Job Description Similarity Score:</b> {similarity_score:.2f}<br>
    <b>Skills Match:</b> {skills_match_percentage:.2f}% (Weighted Score: {skills_weighted_score:.2f}/30)<br>
    <b>Work Experience Match:</b> {work_experience_match}/80<br>
    <b>Education Match:</b> {education_match}/70<br>
    <b>Matched Skills:</b> {', '.join(matched_skills) if matched_skills else 'No specific skill match found'}<br>
    <b>General ATS Score:</b> {general_ats_score:.2f}% (Not specific to any job description)
    """

    resume_score = "High" if overall_match_percentage >= 80 else "Medium" if overall_match_percentage >= 50 else "Low"
    return response, overall_match_percentage, resume_score, general_ats_score

# Flask routes
@app.route('/', methods=['GET', 'POST'])
def index():
    analysis_result = None

    if request.method == 'POST':
        resume_file = request.files.get('resume')
        jd_file = request.files.get('job_description')

        if resume_file and jd_file:
            resume_text = extract_text_from_pdf(resume_file)
            jd_text = extract_text_from_pdf(jd_file)

            analysis_result, resume_score_percentage, resume_score, general_ats_score = analyze_resume_vs_jd(resume_text, jd_text)

    return render_template('index.html', analysis_result=analysis_result)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
