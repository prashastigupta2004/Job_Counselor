from flask import Flask, jsonify, render_template, request, redirect, url_for
import os
import uuid
import pandas as pd
from src.resume_parser import extract_text_from_pdf, extract_skills  # Import the necessary functions
from src.utils import match_skills_with_jobs
from src.ats_checker import get_gemini_response , input_pdf_text


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
        matching_jobs = match_skills_with_jobs(extracted_skills, job_postings_data)

        # Pass the matching URLs to the home template
        return redirect(url_for('home', matching_jobs=matching_jobs))

@app.route('/improvecv',methods=['POST'])
def improvementcv():
    

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
        # Get job description from the form
        job_description = request.form['job_description']
     # Get Gemini response for ATS recommendation
        gemini_response = get_gemini_response(job_description, resume_text)

        return render_template('gemini_modal.html', gemini_response=gemini_response)


@app.route('/checkjob',methods=['POST'])
def checkjob():
     if 'job_skills' in request.form:
        job_skills = request.form['job_skills']
        # Process the job skills data as needed
        # For example, you can print it to the console or perform any other operations

        # Once processed, you can send back a response to the frontend
        return jsonify({'message': 'Job skills received successfully'})
     else:
        return jsonify({'error': 'Job skills not found in the request'})

@app.route('/home')
def home():
    matching_jobs = request.args.getlist('matching_jobs')
    return render_template('result1.html', matching_jobs=matching_jobs)
@app.route('/dashboard')
def dash():
    return render_template('dashboard2.html')

@app.route('/atsresume')
def atresume():
    return render_template('atsresume.html')


if __name__ == '__main__':
    app.run(debug=True)  # Turn off debug mode




