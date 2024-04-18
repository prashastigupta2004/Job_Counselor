import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

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

# Load the second dataset for testing
test_data = pd.read_csv('final_dataset 1.csv')

# Replace missing values with empty strings
test_data['Skills'] = test_data['Skills'].fillna('')

# Extract skills from the "Skills" column of the second dataset
test_skills = test_data['Skills']

# Transform skills into TF-IDF features using the same vectorizer trained on the first dataset
X_test_tfidf = vectorizer.transform(test_skills)

# Predict job domains on the test set
y_pred_test = svm_classifier.predict(X_test_tfidf)

# Convert any float values in the 'Job_domain' column to strings
test_data['Job_domain'] = test_data['Job_domain'].astype(str)

# Calculate accuracy on the second dataset
accuracy = accuracy_score(test_data['Job_domain'], y_pred_test)
print("Accuracy on the Second Dataset:", accuracy)


# Add predicted job domains to the test dataset
test_data['Predicted_Job_domain'] = y_pred_test

# Print the predicted job domains for the second dataset
print("Predicted Job Domains for Second Dataset:")
print(test_data[['Title', 'Skills', 'Predicted_Job_domain','Job_domain']])