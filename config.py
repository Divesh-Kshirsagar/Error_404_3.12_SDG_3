"""
Configuration & Constants

Central configuration for AarogyaQueue system.
Modify thresholds and settings here.
"""

# Risk Score Thresholds
RISK_THRESHOLDS = {
    'high': 0.7,      # Score >= 0.7 → High risk
    'medium': 0.4,    # Score 0.4-0.7 → Medium risk
    'low': 0.0        # Score < 0.4 → Low risk
}

# Queue Assignment
QUEUE_TYPES = {
    'senior': ['high', 'medium'],   # Senior doctors handle high & medium
    'junior': ['low']                # Junior doctors handle low risk
}

# Supabase Configuration (use environment variables in production)
SUPABASE_URL = ""
SUPABASE_KEY = ""

# OpenAI Configuration (for LLM extraction)
OPENAI_API_KEY = ""

# Application Settings
MAX_QUEUE_SIZE = 100
ESTIMATED_CONSULTATION_TIME = 15  # minutes per patient

# UI Settings
KIOSK_TITLE = "AarogyaQueue - Patient Registration"
DASHBOARD_TITLE = "AarogyaQueue - Doctor Dashboard"
