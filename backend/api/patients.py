"""
Patient API endpoints
Patient registration, profile, and visit management
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from datetime import datetime
from database import get_session
from models import Patient, Visit
from schemas import (
    PatientRegister, PatientResponse, VisitCreate, VisitResponse, MessageResponse
)
from services.risk_service import risk_service
from services.queue_service import queue_service

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.post("/register", response_model=PatientResponse, status_code=201)
def register_patient(
    patient_data: PatientRegister,
    session: Session = Depends(get_session)
):
    """
    Register a new patient
    
    - **phone_number**: Unique phone number (10-15 digits)
    - **yob_pin**: Year of birth + PIN (format: YYYY#PIN, e.g., 1990#1234)
    - **full_name**: Patient's full name
    - **chronic_history**: Optional chronic health conditions
    """
    # Check if patient already exists
    existing = session.get(Patient, patient_data.phone_number)
    if existing:
        raise HTTPException(status_code=400, detail="Patient already registered")
    
    # Create patient
    patient = Patient(**patient_data.model_dump())
    session.add(patient)
    session.commit()
    session.refresh(patient)
    
    return patient


@router.get("/{phone_number}", response_model=PatientResponse)
def get_patient(
    phone_number: str,
    session: Session = Depends(get_session)
):
    """Get patient profile by phone number"""
    patient = session.get(Patient, phone_number)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.post("/{phone_number}/visits", response_model=VisitResponse, status_code=201)
def create_visit(
    phone_number: str,
    visit_data: VisitCreate,
    session: Session = Depends(get_session)
):
    """
    Create a new visit for patient
    
    Frontend sends:
    - **symptoms_raw**: Raw symptom text (either typed or transcribed from audio)
    - **symptoms_extracted**: Optional AI-extracted JSON data from frontend Groq processing
    
    Backend processes:
    - Calculate severity score using ML model
    - Assign to appropriate doctor tier
    - Return visit with queue position
    """
    # Verify patient exists
    patient = session.get(Patient, phone_number)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Calculate severity score
    severity_score = risk_service.calculate_severity_score(
        symptoms_raw=visit_data.symptoms_raw,
        symptoms_extracted=visit_data.symptoms_extracted
    )
    
    # Determine severity level and assign tier
    severity_level = risk_service.get_severity_level(severity_score)
    assigned_tier = queue_service.assign_to_tier(severity_level)
    
    # Create visit
    visit = Visit(
        patient_phone=phone_number,
        symptoms_raw=visit_data.symptoms_raw,
        symptoms_extracted=visit_data.symptoms_extracted,
        severity_score=severity_score,
        assigned_tier=assigned_tier,
        status="WAITING"
    )
    
    session.add(visit)
    session.commit()
    session.refresh(visit)
    
    return visit


@router.get("/{phone_number}/visits", response_model=list[VisitResponse])
def get_patient_visits(
    phone_number: str,
    session: Session = Depends(get_session)
):
    """Get all visits for a patient, sorted by most recent first"""
    # Verify patient exists
    patient = session.get(Patient, phone_number)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Get all visits
    query = select(Visit).where(
        Visit.patient_phone == phone_number
    ).order_by(Visit.created_at.desc())
    
    visits = session.exec(query).all()
    return list(visits)
