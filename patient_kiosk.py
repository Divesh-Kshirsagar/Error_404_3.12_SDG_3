"""
Patient Kiosk Interface (Streamlit)

Entry point for patients to:
- Enter phone number and year of birth
- Describe symptoms via voice/text
- Review extracted data
- Receive token number and wait time
"""

import streamlit as st
from utils.supabase_client import get_supabase_client
from utils.voice_processing import process_voice_input
from ml.risk_model import calculate_risk_score
from config import RISK_THRESHOLDS


def main():
    """Main entry point for patient kiosk interface"""
    pass


if __name__ == "__main__":
    main()
