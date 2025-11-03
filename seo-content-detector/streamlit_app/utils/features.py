import nltk
from nltk.tokenize import sent_tokenize
import textstat
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

#get nltk stuff we need
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

def extract_features(body_text):
    """get text stats"""
    try:
        # Basic metrics
        word_count = len(body_text.split())
        sentence_count = len(sent_tokenize(body_text))
        
        # Readability
        flesch_score = textstat.flesch_reading_ease(body_text)
        
        # Check if thin content
        is_thin = word_count < 500
        
        return {
            'word_count': word_count,
            'sentence_count': sentence_count,
            'flesch_reading_ease': flesch_score,
            'is_thin': is_thin
        }
    except Exception as e:
        return {
            'word_count': 0,
            'sentence_count': 0,
            'flesch_reading_ease': 0,
            'is_thin': True,
            'error': str(e)
        }

def extract_keywords(body_text, n=5):
    """find important words"""
    try:
        vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        tfidf_matrix = vectorizer.fit_transform([body_text])
        feature_names = np.array(vectorizer.get_feature_names_out())
        
        # Get top keywords
        doc_vector = tfidf_matrix.toarray()[0]
        top_indices = doc_vector.argsort()[-n:][::-1]
        keywords = feature_names[top_indices]
        
        return '|'.join(keywords)
    except Exception as e:
        return f"Error: {str(e)}"

def get_tfidf_vector(body_text, vectorizer=None):
    """make text comparable"""
    try:
        if vectorizer is None:
            vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
            vector = vectorizer.fit_transform([body_text])
        else:
            vector = vectorizer.transform([body_text])
        
        return vector.toarray()[0], vectorizer
    except Exception as e:
        return None, None