import pickle
def predict_job_domain_for_user(skills):

    with open('svm_classifier_model.pkl', 'rb') as file:
        loaded_model = pickle.load(file)

    # Load the saved vectorizer from the pickle file
    with open('vectorizer.pkl', 'rb') as file:
        loaded_vectorizer = pickle.load(file)
    

    

    # Preprocess the single comment in the same way as your training data
    # For example, you may need to convert to lowercase, remove punctuation, etc.

    # Transform the preprocessed comment into TF-IDF features using the loaded vectorizer
    X_single_comment_tfidf = loaded_vectorizer.transform([skills.replace(',',' ').lower()])

    # Predict sentiment for the single comment
    predicted_sentiment = loaded_model.predict([X_single_comment_tfidf])

    print("Predicted sentiment for the single comment: ye src se ", predicted_sentiment)
    return predicted_sentiment[0]

