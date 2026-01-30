"""
Doctor Dashboard Interface (Streamlit)

Dashboard for doctors to:
- Select role (Junior/Senior)
- View assigned queue based on patient risk
- See patient summaries with risk scores
- Enter diagnosis and move to next patient
"""

import streamlit as st
from utils.supabase_client import get_supabase_client
from utils.auth import verify_doctor
from config import QUEUE_TYPES


def main():
    """Main entry point for doctor dashboard"""
    pass


if __name__ == "__main__":
    main()
