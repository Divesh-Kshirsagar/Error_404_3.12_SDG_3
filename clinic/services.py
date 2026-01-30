"""
Grok API Integration Service for Symptom Analysis.

This module provides functions to analyze patient symptoms using the Grok API
and return a risk score for queue prioritization.
"""
import json
import requests
from django.conf import settings


def analyze_symptoms(transcript_text: str) -> dict:
    """
    Analyze patient symptoms using Grok API.
    
    Args:
        transcript_text: The voice transcript of patient symptoms.
        
    Returns:
        A dictionary containing:
        - symptoms: List of extracted symptoms
        - risk_score: Float from 0.0 to 1.0 indicating urgency
    """
    # Default response if API fails or is not configured
    default_response = {
        'name': None,
        'age': None,
        'symptoms': [],
        'risk_score': 0.5
    }
    
    if not settings.GROK_API_KEY:
        # If no API key, return a mock response for development
        return _mock_analyze(transcript_text)
    
    try:
        headers = {
            'Authorization': f'Bearer {settings.GROK_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        prompt = f"""Analyze the following patient symptom description and return a JSON response.
Extract the patient's name and age if mentioned. If not mentioned, set them to null.
Extract the symptoms mentioned and assign a risk score from 0.0 to 1.0 based on urgency.

Risk Score Guidelines:
- 0.0-0.3: Minor issues (cold, mild headache, minor aches)
- 0.4-0.6: Moderate concerns (persistent symptoms, moderate pain)
- 0.7-0.8: Significant issues (high fever, severe pain, breathing difficulty)
- 0.9-1.0: Critical/Emergency (chest pain, stroke symptoms, severe trauma)

Patient Description: {transcript_text}

Respond ONLY with valid JSON in this exact format:
{{"name": "Name" or null, "age": 25 or null, "symptoms": ["symptom1", "symptom2"], "risk_score": 0.5}}"""

        payload = {
            'model': 'grok-3-mini',
            'messages': [
                {
                    'role': 'system',
                    'content': 'You are a medical triage assistant. Analyze symptoms and provide risk assessments. Always respond with valid JSON only.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'temperature': 0.3
        }
        
        response = requests.post(
            settings.GROK_API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        
        result = response.json()
        content = result['choices'][0]['message']['content']
        
        # Parse the JSON response
        parsed = json.loads(content)
        
        # Validate and sanitize the response
        name = parsed.get('name')
        age = parsed.get('age')
        if age:
            try:
                age = int(age)
            except (ValueError, TypeError):
                age = None
                
        symptoms = parsed.get('symptoms', [])
        risk_score = float(parsed.get('risk_score', 0.5))
        
        # Clamp risk score between 0.0 and 1.0
        risk_score = max(0.0, min(1.0, risk_score))
        
        return {
            'name': name,
            'age': age,
            'symptoms': symptoms if isinstance(symptoms, list) else [],
            'risk_score': risk_score
        }
        
    except (requests.RequestException, json.JSONDecodeError, KeyError, ValueError) as e:
        print(f"Error analyzing symptoms: {e}")
        return default_response


def _mock_analyze(transcript_text: str) -> dict:
    """
    Mock symptom analysis for development without API key.
    
    Uses simple keyword matching to simulate risk scoring.
    """
    transcript_lower = transcript_text.lower()
    
    # High-risk keywords
    high_risk_keywords = [
        'chest pain', 'difficulty breathing', 'severe', 'emergency',
        'unconscious', 'stroke', 'heart', 'bleeding heavily', 'cant breathe'
    ]
    
    # Moderate-risk keywords
    moderate_keywords = [
        'fever', 'persistent', 'vomiting', 'dizzy', 'pain',
        'infection', 'swelling', 'cough'
    ]
    
    # Low-risk keywords
    low_risk_keywords = [
        'cold', 'runny nose', 'mild', 'headache', 'tired',
        'sore throat', 'sneeze'
    ]
    
    # Extract symptoms (simple word matching)
    extracted_symptoms = []
    all_keywords = high_risk_keywords + moderate_keywords + low_risk_keywords
    
    for keyword in all_keywords:
        if keyword in transcript_lower:
            extracted_symptoms.append(keyword)
    
    # Calculate risk score
    risk_score = 0.3  # Base score
    
    for keyword in high_risk_keywords:
        if keyword in transcript_lower:
            risk_score = max(risk_score, 0.85)
            break
    
    for keyword in moderate_keywords:
        if keyword in transcript_lower:
            risk_score = max(risk_score, 0.55)
    
    # If no symptoms found, default to moderate
    if not extracted_symptoms:
        extracted_symptoms = ['unspecified symptoms']
        risk_score = 0.5
    
    # Mock extraction for name and age (simple regex-like heuristic for demo)
    import re
    
    extracted_name = None
    extracted_age = None
    
    # Try to find age
    age_match = re.search(r'(\d+)\s*(?:years|yrs|year)\s*old', transcript_lower)
    if age_match:
        extracted_age = int(age_match.group(1))
    
    # Try to find name (simple "my name is X" pattern)
    name_match = re.search(r'my name is\s+([a-zA-Z]+)', transcript_lower)
    if name_match:
        extracted_name = name_match.group(1).title()
    
    return {
        'name': extracted_name,
        'age': extracted_age,
        'symptoms': extracted_symptoms,
        'risk_score': round(risk_score, 2)
    }
