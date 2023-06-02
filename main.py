from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

# Assume we have some dataset of videos with their metadata and labels
videos = [
    {"title": "Python Tutorial for Beginners", "description": "Learn Python programming", "tags": ["Python", "Programming"], "niche": "technology"},
    {"title": "Easy Chocolate Cake Recipe", "description": "Delicious chocolate cake", "tags": ["Baking", "Cake"], "niche": "cooking"},
]

metadata = [video['title'] + ' ' + video['description'] + ' ' + ' '.join(video['tags']) for video in videos]
labels = [video['niche'] for video in videos]

# Create a pipeline for data preprocessing and training
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', LogisticRegression()),
])

# Train the model
pipeline.fit(metadata, labels)  # Use all data for training in this small example

# Now we can use the trained model to categorize new videos
video = {"title": "How to lose weight", "description": "Effective workout routines", "tags": ["Fitness", "Workout"]}
metadata = video['title'] + ' ' + video['description'] + ' ' + ' '.join(video['tags'])
print(f"Predicted niche: {pipeline.predict([metadata])[0]}")
