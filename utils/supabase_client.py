"""
Supabase Database Client

Handles all database operations:
- Patient records
- Visit records
- Queue state management
- Real-time sync between kiosk and dashboard
"""

from supabase import create_client


def get_supabase_client():
    """Initialize and return Supabase client"""
    pass


def add_patient(patient_data):
    """Add new patient to database"""
    pass


def update_queue(patient_id, queue_type, risk_score):
    """Update queue with new patient based on risk"""
    pass


def get_queue(doctor_type):
    """Fetch queue for specific doctor type (junior/senior)"""
    pass


def mark_patient_seen(patient_id, diagnosis):
    """Mark patient as seen and store diagnosis"""
    pass
