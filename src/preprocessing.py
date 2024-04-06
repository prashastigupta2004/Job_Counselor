# preprocessing.py

import pandas as pd

# Define a dictionary mapping abbreviated forms to full forms
abbreviation_mapping = {
    "ml": "machine learning",
    "dl": "deep learning",
    "ai": "artificial intelligence"
    # Add more mappings as needed
}

def convert_abbreviations_to_full_forms(skill):
    """
    Function to convert abbreviations to full forms within a skill.
    """
    # Split the skill into individual words
    words = skill.split(',')
    
    # Iterate through each word and replace the abbreviation with the full form
    for i, word in enumerate(words):
        # Get the lowercase word to match with the abbreviation mapping
        lower_word = word.strip().lower()
        full_form = abbreviation_mapping.get(lower_word, word)  # Get the full form or keep the word unchanged
        words[i] = full_form.strip()
    
    # Join the words back together to form the updated skill
    updated_skill = ', '.join(words)
    return updated_skill

def preprocess_skills_data(df):
    """
    Preprocess the skills data by converting abbreviations to full forms and converting to lowercase.
    """
    # Convert the 'Skills' column to lowercase
    df['Skills'] = df['Skills'].str.lower()
    
    # Apply abbreviation expansion to the 'Skills' column
    df['Skills'] = df['Skills'].apply(convert_abbreviations_to_full_forms)
    
    # Convert skills in the 'Skills' column to lowercase
    df['Skills'] = df['Skills'].str.lower()
    
    return df

# def match_skills_with_jobs(extracted_skills, job_dataset):
    """
    Match extracted skills with job dataset and return matching URLs.
    """
    matching_urls = []

    # Iterate through each job posting in the dataset
    for index, job in job_dataset.iterrows():
        job_skills = job['Skills']  # Extract skills from the 'Skills' column
        
        # Check if job_skills is a string, otherwise continue to the next row
        if not isinstance(job_skills, str):
            continue

        # Count the number of matching skills between the resume and job posting
        num_matching_skills = sum(skill in job_skills for skill in extracted_skills)

        # If at least two skills match, consider the job relevant and add its URL to the list
        if num_matching_skills >= 2:
            matching_urls.append(job['URL'])

    return matching_urls
