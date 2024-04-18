import pandas as pd
import pickle

def save_object(file_path, obj):
    """
    Save a Python object to a file using pickle.

    Args:
    - file_path (str): File path to save the object
    - obj: Python object to be saved
    """
    with open(file_path, 'wb') as file:
        pickle.dump(obj, file)

def load_object(file_path):
    """
    Load a Python object from a file using pickle.

    Args:
    - file_path (str): File path to load the object from

    Returns:
    - obj: Loaded Python object
    """
    with open(file_path, 'rb') as file:
        obj = pickle.load(file)
    return obj

def match_skills_with_jobs(extracted_skills, job_postings_data):
    # matching_urls = []
    matching_jobs = []
    for _, row in job_postings_data.iterrows():
        try:
          
            job_skills = row['Skills']
            # print("---------------",job_skills)
            # Check if job_skills is a string, otherwise continue to the next row
            if not isinstance(job_skills, str):
                continue

            # Split the job skills string into a list of skills
            job_skills = job_skills.split(',')  # Assuming skills are separated by commas

        except (KeyError, TypeError, AttributeError) as e:
            print(f"Error occurred while processing row: {row}, Error: {e}")
            continue
        
        # Debug print to check job skills
        print("-----------Job Skills:", job_skills)  
        
        # Check if any of the extracted skills match the job skills
        if any(skill.lower() in extracted_skills for skill in job_skills):
            matching_jobs.append(
            {
                "title": row.get('Title','Software Engineer').split(','),
                "company_name": row.get('Company','Company XYZ'),
                "job_location": row.get('Location','Remote').split(','),
                "url": row.get('URL','URL not found'),
                "job_skills": row.get('Skills','ReacT').split(','),
            })

    return matching_jobs
