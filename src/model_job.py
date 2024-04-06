# -*- coding: utf-8 -*-
"""Model_job.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HSYzgHihP-3-h9gcdCjr0y5i9GA6c_mn
"""

# !pip install panda

# !pip install -U scikit-learn

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

data = pd.read_csv('skill_dataset1.csv')

X = data['Skill']
y = data['Job_domain']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

vectorizer = TfidfVectorizer(max_features=1000)  # You can adjust max_features as needed as it will increase accuracy but also lead overfitting
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)

rf_classifier.fit(X_train_vec, y_train)

our_data = pd.read_csv('resume skill data set 3.csv')

X_predict = our_data['Skill']
y_true = our_data['true_job_domain']

X_predict_vec = vectorizer.transform(X_predict)

predicted_job_domains = rf_classifier.predict(X_predict_vec)

print(predicted_job_domains)

our_data['Predicted_job_domain'] = predicted_job_domains

our_data.to_csv('resume skill data set 3.csv', index=False)



final_data=pd.read_csv('resume skill data set 3.csv')

accuracy = accuracy_score(y_true, predicted_job_domains)
print("Accuracy:", accuracy)