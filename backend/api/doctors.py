"""
Doctor API endpoints
Doctor queue management, visit updates, and analytics
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from datetime import datetime
from database import get_session
from models import Visit, Doctor, Patient
from schemas import (
    VisitResponse, VisitUpdate, VisitWithPatient, 
    QueueResponse, MessageResponse
)
from services.queue_service import queue_service
from utils.constants import VisitStatus

router = APIRouter(prefix="/doctors", tags=["Doctors"])

@router.get("/{doctor_id}/queue", response_model=QueueResponse)
def get_doctor_queue(
    doctor_id: int,
    session: Session = Depends(get_session)
):
    """
    Get queue for a doctor (filtered by their role tier)
    
    Returns visits sorted by severity (highest first)
    """
    # Verify doctor exists
    doctor = session.get(Doctor, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    # Get queue visits
    visits = queue_service.get_doctor_queue(session, doctor_id)
    
    # Enrich with patient data
    visits_with_patient = []
    for visit in visits:
        patient = session.get(Patient, visit.patient_phone)
        if patient:
            visit_dict = VisitResponse.model_validate(visit).model_dump()
            visit_dict['patient_name'] = patient.full_name
            visit_dict['patient_chronic_history'] = patient.chronic_history
            visits_with_patient.append(VisitWithPatient(**visit_dict))
    
    # Calculate stats
    total_waiting = len([v for v in visits if v.status == VisitStatus.WAITING])
    highest_severity = max([v.severity_score for v in visits], default=None)
    
    return QueueResponse(
        visits=visits_with_patient,
        total_waiting=total_waiting,
        highest_severity=highest_severity
    )


@router.get("/visits/{visit_id}", response_model=VisitWithPatient)
def get_visit_details(
    visit_id: int,
    session: Session = Depends(get_session)
):
    """Get detailed visit information with patient data"""
    visit = session.get(Visit, visit_id)
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    
    patient = session.get(Patient, visit.patient_phone)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Combine visit and patient data
    visit_dict = VisitResponse.model_validate(visit).model_dump()
    visit_dict['patient_name'] = patient.full_name
    visit_dict['patient_chronic_history'] = patient.chronic_history
    
    return VisitWithPatient(**visit_dict)


@router.put("/visits/{visit_id}", response_model=VisitResponse)
def update_visit(
    visit_id: int,
    update_data: VisitUpdate,
    session: Session = Depends(get_session)
):
    """
    Update visit with doctor notes, prescription, or status
    
    - **doctor_notes**: Clinical notes from doctor
    - **prescription**: Prescription details
    - **status**: Update status (e.g., IN_PROGRESS → COMPLETED)
    """
    visit = session.get(Visit, visit_id)
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    
    # Update fields
    if update_data.doctor_notes is not None:
        visit.doctor_notes = update_data.doctor_notes
    
    if update_data.prescription is not None:
        visit.prescription = update_data.prescription
    
    if update_data.status is not None:
        visit.status = update_data.status
        
        # Set completion time if status is COMPLETED
        if update_data.status == VisitStatus.COMPLETED:
            visit.completed_at = datetime.utcnow()
    
    session.add(visit)
    session.commit()
    session.refresh(visit)
    
    return visit


@router.post("/visits/{visit_id}/start", response_model=MessageResponse)
def start_visit(
    visit_id: int,
    doctor_id: int,
    session: Session = Depends(get_session)
):
    """
    Assign visit to doctor and mark as IN_PROGRESS
    
    - **visit_id**: Visit to start
    - **doctor_id**: Doctor starting the visit (query param)
    """
    success = queue_service.assign_visit_to_doctor(session, visit_id, doctor_id)
    
    if not success:
        raise HTTPException(status_code=400, detail="Failed to assign visit")
    
    return MessageResponse(
        success=True,
        message="Visit started successfully"
    )
