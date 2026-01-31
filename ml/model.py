import pickle
import re
import pandas as pd
import warnings
from pathlib import Path

# Suppress sklearn version warnings for clean demo output
warnings.filterwarnings('ignore', category=UserWarning, module='sklearn')

# Model path
MODEL_PATH = Path(__file__).parent / 'risk_model.pkl'

def load_model():
    with open(MODEL_PATH, 'rb') as f:
        return pickle.load(f)

def extract_features_from_symptoms(symptoms_text, age):
    """Extract binary features from symptom text"""
    text_lower = symptoms_text.lower()
    
    # Critical/Emergency keywords that should trigger high risk
    critical_keywords = [
        'heart attack', 'stroke', 'unconscious', 'bleeding', 'hemorrhage',
        'cancer', 'tumor', 'malignant', 'carcinoma', 'oncology',
        'hiv', 'aids', 'seizure', 'convulsion', 'paralysis', 'paralyzed',
        'suicide', 'overdose', 'poisoning', 'sepsis', 'septic',
        'aneurysm', 'embolism', 'thrombosis', 'infarction',
        'trauma', 'fracture', 'severe', 'critical', 'emergency',
        'life-threatening', 'code blue', 'cardiac arrest', 'respiratory failure',
        'organ failure', 'kidney failure', 'liver failure', 'coma',
        'stabbing', 'gunshot', 'accident', 'collision'
    ]
    
    # Check for critical conditions
    has_critical = any(keyword in text_lower for keyword in critical_keywords)
    
    # Severity indicators
    severity_words = ['severe', 'extreme', 'intense', 'unbearable', 'excruciating', 
                     'massive', 'heavy', 'critical', 'acute', 'sudden']
    has_severity = any(word in text_lower for word in severity_words)
    
    features = {
        'age_normalized': age / 100,
        'chest_pain': 1 if any(word in text_lower for word in ['chest', 'heart', 'cardiac']) else 0,
        'breathing_difficulty': 1 if any(word in text_lower for word in ['breath', 'breathing', 'shortness']) else 0,
        'fever': 1 if any(word in text_lower for word in ['fever', 'temperature', 'hot']) else 0,
        'headache': 1 if any(word in text_lower for word in ['head', 'headache', 'migraine']) else 0,
        'emergency_keywords': 1 if has_critical or has_severity else 0
    }
    
    return list(features.values())

def predict_risk_score(symptoms_text, age):
    model = load_model()
    features = extract_features_from_symptoms(symptoms_text, age)
    
    # Use DataFrame to maintain feature names (avoids sklearn warnings)
    feature_names = ['age_normalized', 'chest_pain', 'breathing_difficulty', 
                     'fever', 'headache', 'emergency_keywords']
    features_df = pd.DataFrame([features], columns=feature_names)
    
    risk_score = model.predict(features_df)[0]
    return max(0.0, min(1.0, risk_score))

# Test function
if __name__ == "__main__":
    test_cases = [
        ("chest pain and shortness of breath", 65),
        ("mild headache", 25),
        ("heart attack symptoms", 70)
    ]
    
    for symptoms, age in test_cases:
        risk = predict_risk_score(symptoms, age)
        print(f"Symptoms: '{symptoms}', Age: {age} → Risk: {risk:.2f}")