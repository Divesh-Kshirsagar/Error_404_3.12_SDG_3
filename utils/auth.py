"""
Authentication Logic

Handles authentication for:
- Patient verification (phone + YOB)
- Doctor login and role selection
- Session management
"""

from utils.supabase_client import get_supabase


def verify_patient(phone_number: str, yob: int) -> dict:
    """
    Verify patient identity using phone and YOB
    
    Args:
        phone_number: 10-digit phone number
        yob: Year of birth
    
    Returns:
        dict: {
            'success': bool,
            'patient': dict or None,
            'message': str
        }
    """
    try:
        supabase = get_supabase()
        response = supabase.table('patients').select('*').eq(
            'phone_number', phone_number
        ).eq('yob', yob).execute()
        
        if response.data and len(response.data) > 0:
            return {
                'success': True,
                'patient': response.data[0],
                'message': 'Patient verified successfully'
            }
        else:
            return {
                'success': False,
                'patient': None,
                'message': 'Patient not found'
            }
    except Exception as e:
        return {
            'success': False,
            'patient': None,
            'message': f'Verification failed: {str(e)}'
        }


def register_patient(phone_number: str, yob: int, name: str = None) -> dict:
    """
    Register new patient in the system
    
    Args:
        phone_number: 10-digit phone number
        yob: Year of birth
        name: Optional patient name
    
    Returns:
        dict: {
            'success': bool,
            'patient': dict or None,
            'message': str
        }
    """
    try:
        existing = verify_patient(phone_number, yob)
        if existing['success']:
            return {
                'success': False,
                'patient': None,
                'message': 'Patient already registered'
            }
        
        supabase = get_supabase()
        patient_data = {
            'phone_number': phone_number,
            'yob': yob,
            'name': name
        }
        
        response = supabase.table('patients').insert(patient_data).execute()
        
        if response.data and len(response.data) > 0:
            return {
                'success': True,
                'patient': response.data[0],
                'message': 'Patient registered successfully'
            }
        else:
            return {
                'success': False,
                'patient': None,
                'message': 'Registration failed'
            }
    except Exception as e:
        return {
            'success': False,
            'patient': None,
            'message': f'Registration failed: {str(e)}'
        }


def verify_doctor(username: str, password: str, role: str = None) -> dict:
    """
    Authenticate doctor login
    
    Args:
        username: Doctor username/ID
        password: Doctor password
        role: Optional role filter (JUNIOR/SENIOR)
    
    Returns:
        dict: {
            'success': bool,
            'doctor': dict or None,
            'message': str
        }
    """
    try:
        supabase = get_supabase()
        query = supabase.table('doctors').select('*').eq(
            'username', username
        ).eq('password', password)
        
        if role:
            query = query.eq('role', role)
        
        response = query.execute()
        
        if response.data and len(response.data) > 0:
            doctor = response.data[0]
            return {
                'success': True,
                'doctor': {
                    'id': doctor.get('id'),
                    'username': doctor.get('username'),
                    'role': doctor.get('role')
                },
                'message': 'Doctor authenticated successfully'
            }
        else:
            return {
                'success': False,
                'doctor': None,
                'message': 'Invalid credentials or role mismatch'
            }
    except Exception as e:
        return {
            'success': False,
            'doctor': None,
            'message': f'Authentication failed: {str(e)}'
        }

