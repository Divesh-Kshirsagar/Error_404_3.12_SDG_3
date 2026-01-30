"""
Authentication Logic

Handles authentication for:
- Patient verification (phone + YOB)
- Doctor login and role selection
- Session management
"""


def verify_patient(phone_number, year_of_birth):
    """
    Verify patient identity using phone and YOB
    
    Args:
        phone_number (str): 10-digit phone number
        year_of_birth (int): Year of birth
    
    Returns:
        dict: Patient info or None if new patient
    """
    pass


def verify_doctor(doctor_id, password):
    """
    Authenticate doctor login
    
    Args:
        doctor_id (str): Doctor ID
        password (str): Password
    
    Returns:
        dict: Doctor info with role (junior/senior)
    """
    pass
