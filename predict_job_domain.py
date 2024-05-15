import pickle

def predict_job_domain_for_user(skills):
    # Load the trained SVM classifier and TF-IDF vectorizer
    with open('svm_classifier_model.pkl', 'rb') as file:
        loaded_model = pickle.load(file)
    with open('vectorizer.pkl', 'rb') as file:
        loaded_vectorizer = pickle.load(file)

    # Preprocess the user skills
    preprocessed_skills = skills.lower()  # You can add more preprocessing steps here

    # Transform preprocessed skills into TF-IDF features using the loaded vectorizer
    skills_tfidf = loaded_vectorizer.transform([preprocessed_skills])

    # Predict the job domain for the user skills
    predicted_domain = loaded_model.predict(skills_tfidf)

    return predicted_domain[0]


