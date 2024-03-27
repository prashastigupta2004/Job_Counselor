import os
from flask import Flask, request

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'resume' not in request.files:
        return 'No file part in the request'

    resume = request.files['resume']
    if resume.filename == '':
        return 'No selected file'

    if resume:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], resume.filename)
        resume.save(filename)
        return f'File uploaded successfully. Filename: {resume.filename}'

if __name__ == '__main__':
    app.run(debug=True)

