"""
AarogyaQueue Configuration
"""

# Risk Score Thresholds
RISK_LOW_THRESHOLD = 0.4
RISK_MEDIUM_THRESHOLD = 0.7

RISK_LEVELS = {
    'LOW': (0.0, RISK_LOW_THRESHOLD),
    'MEDIUM': (RISK_LOW_THRESHOLD, RISK_MEDIUM_THRESHOLD),
    'HIGH': (RISK_MEDIUM_THRESHOLD, 1.0)
}

# Doctor Tier Assignment
DOCTOR_JUNIOR = 'JUNIOR'
DOCTOR_SENIOR = 'SENIOR'

QUEUE_ASSIGNMENT = {
    'LOW': DOCTOR_JUNIOR,
    'MEDIUM': DOCTOR_SENIOR,
    'HIGH': DOCTOR_SENIOR
}

# Supported Languages
SUPPORTED_LANGUAGES = [
    'en',  # English
    'hi',  # Hindi
    'mr',  # Marathi
]

# Wait Time Estimation
DEFAULT_CONSULTATION_TIME_MINUTES = 15
JUNIOR_DOCTOR_CONSULTATION_TIME_MINUTES = 10
SENIOR_DOCTOR_CONSULTATION_TIME_MINUTES = 20

# Database Configuration
SUPABASE_URL = ""
SUPABASE_KEY = ""

# LLM Configuration
OPENAI_API_KEY = ""
LLM_MODEL = "gpt-4"
LLM_MAX_TOKENS = 500

# Application Settings
MAX_QUEUE_SIZE = 100
KIOSK_TITLE = "AarogyaQueue - Patient Registration"
DASHBOARD_TITLE = "AarogyaQueue - Doctor Dashboard"
