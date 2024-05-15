import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
import pickle

def train_classifier():
    # Load the first dataset for training
    data = pd.read_csv('skill_dataset1.csv')

    # Extract features (skills) and target variable (job domains)
    X = data['Skills']
    y = data['Job_domain']

    # Convert skills into TF-IDF features
    vectorizer = TfidfVectorizer()
    X_tfidf = vectorizer.fit_transform(X)

    # Train the Support Vector Machine (SVM) classifier
    svm_classifier = SVC(kernel='linear')
    svm_classifier.fit(X_tfidf, y)

    # Save the trained model and vectorizer
    with open('svm_classifier_model.pkl', 'wb') as file:
        pickle.dump(svm_classifier, file)
    with open('vectorizer.pkl', 'wb') as file:
        pickle.dump(vectorizer, file)

def predict_domain_for_user(user_skills):
    # Load the trained SVM classifier and TF-IDF vectorizer
    with open('svm_classifier_model.pkl', 'rb') as file:
        loaded_model = pickle.load(file)
    with open('vectorizer.pkl', 'rb') as file:
        loaded_vectorizer = pickle.load(file)

    # Preprocess the user skills
    preprocessed_skills = user_skills.lower()  # You can add more preprocessing steps here

    # Transform preprocessed skills into TF-IDF features using the loaded vectorizer
    skills_tfidf = loaded_vectorizer.transform([preprocessed_skills])

    # Predict the job domain for the user skills
    predicted_domain = loaded_model.predict(skills_tfidf)

    return predicted_domain[0]

# Call the train_classifier() function to train the classifier and save the model and vectorizer
train_classifier()
