"""
Authentication API endpoints
Simple PIN-based authentication (no JWT tokens for hackathon MVP)
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import Patient, Doctor
from schemas import PatientLoginRequest, DoctorLoginRequest, LoginResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/patient-login", response_model=LoginResponse)
def patient_login(
    credentials: PatientLoginRequest,
    session: Session = Depends(get_session)
):
    """
    Patient login with phone number + PIN
    
    - **phone_number**: Patient's registered phone number
    - **pin**: 4-digit PIN from yob_pin (format: YYYY#PIN)
    """
    # Find patient by phone
    patient = session.get(Patient, credentials.phone_number)
    
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Extract PIN from yob_pin (format: YYYY#PIN)
    try:
        stored_pin = patient.yob_pin.split('#')[1]
    except IndexError:
        raise HTTPException(status_code=500, detail="Invalid yob_pin format in database")
    
    # Verify PIN
    if stored_pin != credentials.pin:
        raise HTTPException(status_code=401, detail="Invalid PIN")
    
    return LoginResponse(
        success=True,
        user_id=patient.phone_number,
        role="patient",
        name=patient.full_name
    )


@router.post("/doctor-login", response_model=LoginResponse)
def doctor_login(
    credentials: DoctorLoginRequest,
    session: Session = Depends(get_session)
):
    """
    Doctor login with doctor ID + PIN
    
    - **doctor_id**: Doctor's unique ID
    - **pin**: Doctor's PIN code
    """
    # Find doctor by ID
    doctor = session.get(Doctor, credentials.doctor_id)
    
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    # Verify PIN
    if doctor.pin_code != credentials.pin:
        raise HTTPException(status_code=401, detail="Invalid PIN")
    
    return LoginResponse(
        success=True,
        user_id=doctor.id,
        role=f"doctor_{doctor.role_tier.value.lower()}",
        name=doctor.name
    )


@router.post("/admin-login", response_model=LoginResponse)
def admin_login(
    credentials: DoctorLoginRequest,
    session: Session = Depends(get_session)
):
    """
    Admin login (uses doctor credentials for simplicity)
    In production, create separate Admin model
    
    - **doctor_id**: Admin ID (using doctor ID)
    - **pin**: Admin PIN
    """
    # For MVP, admin is just a doctor with ID 1
    # In production, create separate Admin model
    doctor = session.get(Doctor, credentials.doctor_id)
    
    if not doctor or doctor.id != 1:  # Only doctor ID 1 is admin
        raise HTTPException(status_code=403, detail="Not authorized as admin")
    
    if doctor.pin_code != credentials.pin:
        raise HTTPException(status_code=401, detail="Invalid PIN")
    
    return LoginResponse(
        success=True,
        user_id=doctor.id,
        role="admin",
        name=doctor.name
    )
