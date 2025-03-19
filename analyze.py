import json
from transformers import pipeline
from sentence_transformers import SentenceTransformer
import numpy as np

# Function to load class names dynamically
def load_classes():
    with open("classes.json", "r") as file:
        data = json.load(file)
    return data["classes"]

# Load email classes dynamically
EMAIL_CLASSES = load_classes()

sentiment_pipeline = pipeline("sentiment-analysis")
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def get_sentiment(text):
    response = sentiment_pipeline(text)
    return response

def compute_embeddings(embeddings=None):
    if embeddings is None:
        embeddings = EMAIL_CLASSES  # Use dynamically loaded classes
    embeddings = model.encode(embeddings)
    return zip(EMAIL_CLASSES, embeddings)

def classify_email(text):
    # Encode the input text
    text_embedding = model.encode([text])[0]
    
    # Get embeddings for all classes
    class_embeddings = compute_embeddings()
    
    # Calculate distances and return results
    results = []
    for class_name, class_embedding in class_embeddings:
        # Compute cosine similarity between text and class embedding
        similarity = np.dot(text_embedding, class_embedding) / (np.linalg.norm(text_embedding) * np.linalg.norm(class_embedding))
        results.append({
            "class": class_name,
            "similarity": float(similarity)  # Convert tensor to float for JSON serialization
        })
    
    # Sort by similarity score descending
    results.sort(key=lambda x: x["similarity"], reverse=True)
    
    return results

print(classify_email("I love playing soccer"))
