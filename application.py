from flask import Flask, render_template, request, redirect, url_for
import os
import uuid
import pandas as pd
from src.resume_parser import extract_text_from_pdf, extract_skills  # Import the necessary functions
from src.utils import match_skills_with_jobs

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load job postings dataset
job_postings_dataset_path = "notebooks/data/final_datasets.csv"
job_postings_data = pd.read_csv(job_postings_dataset_path)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'resume' not in request.files:
        return redirect(request.url)

    resume = request.files['resume']
    if resume.filename == '':
        return redirect(request.url)

    if resume:
        # Save the uploaded resume
        filename = str(uuid.uuid4()) + '.pdf'
        resume.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Extract skills from the uploaded resume
        resume_text = extract_text_from_pdf(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        extracted_skills = extract_skills(resume_text)

        # Match skills with job postings and get matching URLs
        matching_urls = match_skills_with_jobs(extracted_skills, job_postings_data)

        # Pass the matching URLs to the home template
        return redirect(url_for('home', matching_urls=matching_urls))

@app.route('/home')
def home():
    matching_urls = request.args.getlist('matching_urls')
    return render_template('home.html', matching_urls=matching_urls)
@app.route('/dashboard')
def dash():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)  # Turn off debug mode




