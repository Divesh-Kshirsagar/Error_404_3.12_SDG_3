"""
ML Risk Scoring Model

Custom RandomForest model for patient risk prioritization.
- Loads trained model from disk
- Calculates risk score (0.0 - 1.0) from symptoms
- Assigns risk level (Low/Medium/High)
- NOT a diagnostic tool - for queue prioritization only
"""

import os
import pickle
import numpy as np
from typing import List, Dict, Tuple
from config import (
    RISK_LOW_THRESHOLD,
    RISK_MEDIUM_THRESHOLD,
    QUEUE_ASSIGNMENT,
    DOCTOR_JUNIOR,
    DOCTOR_SENIOR
)


_model = None
_feature_names = None


def load_risk_model(model_path: str = "ml/risk_model.pkl") -> Tuple[object, List[str]]:
    """
    Load pre-trained RandomForest model from disk
    
    Args:
        model_path: Path to pickled model file
    
    Returns:
        tuple: (model, feature_names)
    
    Raises:
        FileNotFoundError: If model file doesn't exist
    """
    global _model, _feature_names
    
    if _model is None:
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)
            _model = model_data['model']
            _feature_names = model_data.get('feature_names', [])
    
    return _model, _feature_names


def get_risk_level_from_score(risk_score: float) -> str:
    """
    Map risk score to risk level category
    
    Args:
        risk_score: Score between 0.0 and 1.0
    
    Returns:
        str: 'LOW', 'MEDIUM', or 'HIGH'
    """
    if risk_score >= RISK_MEDIUM_THRESHOLD:
        return 'HIGH'
    elif risk_score >= RISK_LOW_THRESHOLD:
        return 'MEDIUM'
    else:
        return 'LOW'


def get_doctor_tier_from_risk_level(risk_level: str) -> str:
    """
    Determine which doctor tier should handle this patient
    
    Args:
        risk_level: 'LOW', 'MEDIUM', or 'HIGH'
    
    Returns:
        str: 'JUNIOR' or 'SENIOR'
    """
    return QUEUE_ASSIGNMENT.get(risk_level, DOCTOR_SENIOR)


def prepare_features_from_symptoms(symptoms_data: dict) -> np.ndarray:
    """
    Convert symptom data to model input features
    
    Args:
        symptoms_data: {
            'symptoms': list of str,
            'age': int or None,
            'duration_days': int or None,
            'severity': str or None
        }
    
    Returns:
        np.ndarray: Feature vector for model prediction
    """
    # Common symptom keywords for feature extraction
    symptom_keywords = [
        'fever', 'cough', 'breathlessness', 'chest_pain', 'headache',
        'vomiting', 'diarrhea', 'fatigue', 'dizziness', 'bleeding'
    ]
    
    # Binary features for each symptom
    features = []
    symptoms_lower = [s.lower() for s in symptoms_data.get('symptoms', [])]
    
    for keyword in symptom_keywords:
        has_symptom = any(keyword in symptom for symptom in symptoms_lower)
        features.append(1 if has_symptom else 0)
    
    # Age feature (normalized)
    age = symptoms_data.get('age', 30)
    if age is None:
        age = 30  # Default age if not provided
    features.append(age / 100.0)  # Normalize to 0-1 range
    
    # Duration feature (normalized)
    duration = symptoms_data.get('duration_days', 1)
    if duration is None:
        duration = 1
    features.append(min(duration / 30.0, 1.0))  # Cap at 30 days
    
    # Severity feature (categorical to numeric)
    severity = symptoms_data.get('severity', 'mild')
    severity_map = {'mild': 0.3, 'moderate': 0.6, 'severe': 0.9}
    features.append(severity_map.get(severity, 0.3))
    
    return np.array(features).reshape(1, -1)


def calculate_risk_score(symptoms_data: dict) -> dict:
    """
    Calculate risk score from structured symptom data
    
    Args:
        symptoms_data: {
            'symptoms': list of str,
            'age': int or None,
            'duration_days': int or None,
            'severity': str or None
        }
    
    Returns:
        dict: {
            'success': bool,
            'score': float (0.0 - 1.0),
            'level': str ('LOW', 'MEDIUM', 'HIGH'),
            'doctor_tier': str ('JUNIOR', 'SENIOR'),
            'message': str
        }
    """
    try:
        # For MVP: Use rule-based scoring if model not available
        # This allows the system to work even without a trained model
        try:
            model, _ = load_risk_model()
            features = prepare_features_from_symptoms(symptoms_data)
            risk_score = float(model.predict_proba(features)[0][1])
        except (FileNotFoundError, Exception):
            # Fallback to rule-based scoring
            risk_score = calculate_rule_based_risk_score(symptoms_data)
        
        risk_level = get_risk_level_from_score(risk_score)
        doctor_tier = get_doctor_tier_from_risk_level(risk_level)
        
        return {
            'success': True,
            'score': round(risk_score, 3),
            'level': risk_level,
            'doctor_tier': doctor_tier,
            'message': 'Risk assessment completed'
        }
    except Exception as e:
        return {
            'success': False,
            'score': 0.5,
            'level': 'MEDIUM',
            'doctor_tier': DOCTOR_SENIOR,
            'message': f'Risk calculation failed: {str(e)}'
        }


def calculate_rule_based_risk_score(symptoms_data: dict) -> float:
    """
    Fallback rule-based risk scoring when ML model unavailable
    
    Args:
        symptoms_data: Structured symptom data
    
    Returns:
        float: Risk score between 0.0 and 1.0
    """
    score = 0.0
    symptoms = [s.lower() for s in symptoms_data.get('symptoms', [])]
    
    # High-risk symptoms
    high_risk_keywords = ['chest pain', 'breathlessness', 'bleeding', 'unconscious']
    for keyword in high_risk_keywords:
        if any(keyword in symptom for symptom in symptoms):
            score += 0.3
    
    # Medium-risk symptoms
    medium_risk_keywords = ['fever', 'vomiting', 'severe headache', 'dizziness']
    for keyword in medium_risk_keywords:
        if any(keyword in symptom for symptom in symptoms):
            score += 0.15
    
    # Age factor
    age = symptoms_data.get('age', 30)
    if age and age > 60:
        score += 0.2
    elif age and age < 5:
        score += 0.15
    
    # Duration factor
    duration = symptoms_data.get('duration_days', 1)
    if duration and duration > 7:
        score += 0.1
    
    # Severity factor
    severity = symptoms_data.get('severity', 'mild')
    if severity == 'severe':
        score += 0.2
    elif severity == 'moderate':
        score += 0.1
    
    return min(score, 1.0)
