"""
Risk prediction service using ML model
Ports logic from original predict_risk.py
"""
import pickle
import os
from pathlib import Path
from typing import Optional
import pandas as pd
from utils.constants import SeverityLevel, RISK_THRESHOLD_HIGH, RISK_THRESHOLD_MEDIUM

# Path to the ML model (from original project)
MODEL_PATH = Path(__file__).parent.parent / "CIH-1-master" / "telemedicine-queue" / "risk_model.pkl"

class RiskService:
    """Risk prediction service using pickled ML model"""
    
    def __init__(self):
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load the pickled ML model on startup"""
        try:
            if not MODEL_PATH.exists():
                print(f"⚠️  Warning: ML model not found at {MODEL_PATH}")
                print("   Risk scores will use heuristic fallback")
                return
            
            with open(MODEL_PATH, 'rb') as f:
                self.model = pickle.load(f)
            print(f"✅ ML model loaded from {MODEL_PATH}")
        except Exception as e:
            print(f"❌ Error loading ML model: {e}")
            print("   Falling back to heuristic risk scoring")
    
    def calculate_severity_score(
        self, 
        symptoms_raw: str, 
        symptoms_extracted: Optional[dict] = None
    ) -> float:
        """
        Calculate severity score (0-1 float)
        
        Args:
            symptoms_raw: Raw symptom text from patient
            symptoms_extracted: AI-extracted structured data (optional)
        
        Returns:
            float: Severity score between 0 and 1
        """
        if self.model and symptoms_extracted:
            # Use ML model if available and we have structured data
            return self._predict_with_model(symptoms_extracted)
        else:
            # Fallback to keyword-based heuristic
            return self._heuristic_score(symptoms_raw)
    
    def _predict_with_model(self, symptoms_data: dict) -> float:
        """Use ML model to predict risk score"""
        try:
            # Convert symptom data to features the model expects
            # This depends on how the original model was trained
            # For now, using a simple feature extraction
            
            # Example feature extraction (customize based on your model)
            features = self._extract_features(symptoms_data)
            df = pd.DataFrame([features])
            
            # Predict probability
            score = self.model.predict_proba(df)[0][1]  # Probability of high risk
            return float(score)
        except Exception as e:
            print(f"⚠️  Error in ML prediction: {e}, using heuristic")
            return self._heuristic_score(str(symptoms_data))
    
    def _extract_features(self, symptoms_data: dict) -> dict:
        """
        Extract features from symptom data for ML model
        Customize this based on your model's training features
        """
        # Placeholder - customize based on your model
        return {
            "has_fever": "fever" in str(symptoms_data).lower(),
            "has_chest_pain": "chest" in str(symptoms_data).lower(),
            "has_breathing_issue": any(word in str(symptoms_data).lower() 
                                      for word in ["breath", "breathing", "breathless"]),
            "has_severe_pain": "severe" in str(symptoms_data).lower(),
            # Add more features as needed
        }
    
    def _heuristic_score(self, symptoms_text: str) -> float:
        """
        Simple keyword-based heuristic for risk scoring
        Used when ML model is unavailable
        """
        text_lower = symptoms_text.lower()
        score = 0.3  # Base score
        
        # High-risk keywords
        high_risk_keywords = [
            "chest pain", "heart attack", "stroke", "unconscious", 
            "severe bleeding", "head injury", "can't breathe", "difficulty breathing"
        ]
        for keyword in high_risk_keywords:
            if keyword in text_lower:
                score += 0.3
        
        # Medium-risk keywords
        medium_risk_keywords = [
            "high fever", "vomiting", "severe pain", "dizzy", "fainted"
        ]
        for keyword in medium_risk_keywords:
            if keyword in text_lower:
                score += 0.15
        
        # Cap at 1.0
        return min(score, 1.0)
    
    def get_severity_level(self, score: float) -> SeverityLevel:
        """
        Convert severity score to severity level
        
        Args:
            score: Severity score (0-1)
        
        Returns:
            SeverityLevel enum
        """
        if score >= RISK_THRESHOLD_HIGH:
            return SeverityLevel.HIGH
        elif score >= RISK_THRESHOLD_MEDIUM:
            return SeverityLevel.MEDIUM
        else:
            return SeverityLevel.LOW

# Global instance
risk_service = RiskService()
