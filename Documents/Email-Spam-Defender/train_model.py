import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib

# Load your labeled email data CSV
data = pd.read_csv('email_data.csv')

# Combine subject + body into one text column
data['text'] = data['subject'].astype(str) + ' ' + data['body'].astype(str)

# Vectorize text data
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(data['text'])
y = data['label']

# Train Naive Bayes classifier
clf = MultinomialNB()
clf.fit(X, y)

# Save model and vectorizer
joblib.dump(clf, 'spam_classifier.joblib')
joblib.dump(vectorizer, 'vectorizer.joblib')

print("Model training complete and saved.")
