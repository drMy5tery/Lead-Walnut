import joblib
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import os

def load_model(model_path='streamlit_app/models/quality_model.pkl'):
    """grab our trained model"""
    try:
        if os.path.exists(model_path):
            return joblib.load(model_path)
        return None
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

def load_encoder(encoder_path='streamlit_app/models/label_encoder.pkl'):
    """get the label converter"""
    try:
        if os.path.exists(encoder_path):
            return joblib.load(encoder_path)
        return None
    except Exception as e:
        print(f"Error loading encoder: {e}")
        return None

def predict_quality(features, model, encoder):
    """figure out content quality"""
    try:
        # Create feature array
        feature_array = np.array([[
            features['word_count'],
            features['sentence_count'],
            features['flesch_reading_ease']
        ]])
        
        # Predict
        prediction_encoded = model.predict(feature_array)
        quality_label = encoder.inverse_transform(prediction_encoded)[0]
        
        # Get probability scores
        probabilities = model.predict_proba(feature_array)[0]
        label_probs = {label: prob for label, prob in zip(encoder.classes_, probabilities)}
        
        return quality_label, label_probs
    except Exception as e:
        return "Error", {"Error": str(e)}

def find_similar_content(vector, reference_data_path='data/features.csv', threshold=0.70):
    """find content that looks similar"""
    try:
        if not os.path.exists(reference_data_path):
            return []
        
        # Load reference data
        df = pd.read_csv(reference_data_path)
        
        if 'embedding' not in df.columns:
            return []
        
        # Parse embeddings
        import json
        embeddings = [json.loads(emb) for emb in df['embedding']]
        reference_matrix = np.array(embeddings)
        
        # Calculate similarities
        similarities = cosine_similarity([vector], reference_matrix)[0]
        
        # Find similar content
        similar_content = []
        for i, sim_score in enumerate(similarities):
            if sim_score > threshold:
                similar_content.append({
                    'url': df.iloc[i]['url'],
                    'similarity': round(sim_score, 2),
                    'title': df.iloc[i].get('title', 'Unknown')
                })
        
        # Sort by similarity
        similar_content = sorted(similar_content, key=lambda x: x['similarity'], reverse=True)
        
        return similar_content[:5]  # Return top 5
    except Exception as e:
        print(f"Error finding similar content: {e}")
        return []

def create_quality_label_manual(word_count, flesch_score):
    """backup way to check quality"""
    if word_count > 1500 and 50 <= flesch_score <= 70:
        return 'High'
    elif word_count < 500 or flesch_score < 30:
        return 'Low'
    else:
        return 'Medium'