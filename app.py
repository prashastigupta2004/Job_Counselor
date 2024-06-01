from flask import Flask, jsonify, render_template, request, redirect, send_file, url_for
import os
import uuid
import pandas as pd
from src.resume_parser import extract_text_from_pdf, extract_skills  # Import the necessary functions
from src.utils import match_skills_with_jobs
from src.ats_checker import get_gemini_response , input_pdf_text
import json
from src.helper import process_gemini_response
from src.predict_job_domain import predict_job_domain_for_user
from src.gemini import get_chat_response 
 
# from utilss.helper import process_gemini_response
# from utilss.predict_job_domain import predict_job_domain_for_user



app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load job postings dataset
job_postings_dataset_path = "notebooks/data/final_datasets.csv"
job_postings_data = pd.read_csv(job_postings_dataset_path)

@app.route('/',methods=['POST','GET'])
def main():

    if(request.method == 'POST'):
        skills=request.form.get('skills')
    
        # print('--------------------------------',skills+'Predictions for job domain')
        job_domain=predict_job_domain_for_user(skills)
        return  render_template('main.html', job_domain=job_domain)
    else:

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

        job_domain = predict_job_domain_for_user(extracted_skills)
        # Match skills with job postings and get matching URLs
        matching_jobs = match_skills_with_jobs(extracted_skills, job_postings_data)

        # Pass the matching URLs to the home template
        return redirect(url_for('home', matching_jobs=matching_jobs,job_domain=job_domain))

@app.route('/check', methods=['GET'])
def check():
 
        return "<h1>Check Works</h1>"
    
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
        resume_text = input_pdf_text(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print ("resume text : : ",resume_text)
        pdf_filename = filename
        # Get job description from the form

        job_description = request.form['job_description']
     # Get Gemini response for ATS recommendation
        gemini_response = get_gemini_response(job_description, resume_text)
        print(gemini_response)
# Convert JSON string to Python dictionary

        try:
            data_dict = process_gemini_response(gemini_response)
        except Exception as e:
            print("0000000000000000000000000000")
            print(e)
            return redirect('/')

        # Print the dictionary
        print(type(data_dict))



        return render_template('gemini_modal.html', data=data_dict)


 
@app.route('/home')
def home():
    matching_jobs = request.args.getlist('matching_jobs')
    job_domain = request.args.get('job_domain', 'Unknown')
    # print("----------->>>>>"+job_domain)
    job_domain=job_domain.capitalize()
    return render_template('result1.html', matching_jobs=matching_jobs,job_domain=job_domain)
@app.route('/dashboard' ,methods=['POST'])
def dash():
    return render_template('dashboard2.html')

@app.route('/dashboard')
def dash2():
    return render_template('dashboard2.html')




@app.route('/chat', methods=['POST'])  # Route to handle chat messages
def chat():
    if request.method == 'POST':
      
        user_message = request.json.get('message')  # Extract the user message from the request
        # Pass the user message to the chatbot model and get the response
        try:
            bot_response = get_chat_response(user_message)
        except Exception as e:
            print("Error", e)
            bot_response = "none"

        return jsonify({'response': bot_response})  # Return the bot response as JSON
    else:
        return jsonify({'response': "none"})

# @app.route('/show_pdf')
# def show_pdf():
#     # Path to your PDF file
    
#  # Replace this with the actual path to your PDF file
#      pdf_path = os.path.join(app.root_path, pdf_folder, pdf_filename)

#     # Return the PDF file
#      return send_file(pdf_path)

@app.route('/atsresume')
def atresume():
    return render_template('atsresume.html')



if __name__ == '__main__':
    app.run(debug=True)  # Turn off debug mode




