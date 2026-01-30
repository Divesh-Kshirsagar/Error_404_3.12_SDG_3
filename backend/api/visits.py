"""
Admin/Visit management API endpoints
System-wide visit listing, analytics, and doctor management
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, func
from database import get_session
from models import Visit, Doctor, Patient
from schemas import (
    DoctorCreate, DoctorResponse, VisitResponse, 
    AnalyticsResponse, MessageResponse
)
from utils.constants import VisitStatus

router = APIRouter(prefix="/admin", tags=["Admin"])

# ============================================================================
# Analytics Endpoints
# ============================================================================

@router.get("/analytics/dashboard", response_model=AnalyticsResponse)
def get_dashboard_analytics(session: Session = Depends(get_session)):
    """
    Get system-wide statistics for admin dashboard
    
    Returns:
    - Total patients, visits, doctors
    - Visit status breakdown
    - Average severity score
    """
    # Total patients
    total_patients = session.exec(
        select(func.count(Patient.phone_number))
    ).one()
    
    # Total visits
    total_visits = session.exec(
        select(func.count(Visit.id))
    ).one()
    
    # Visits by status
    visits_waiting = session.exec(
        select(func.count(Visit.id)).where(Visit.status == VisitStatus.WAITING)
    ).one()
    
    visits_in_progress = session.exec(
        select(func.count(Visit.id)).where(Visit.status == VisitStatus.IN_PROGRESS)
    ).one()
    
    visits_completed = session.exec(
        select(func.count(Visit.id)).where(Visit.status == VisitStatus.COMPLETED)
    ).one()
    
    # Average severity score
    avg_severity = session.exec(
        select(func.avg(Visit.severity_score))
    ).one() or 0.0
    
    # Total doctors
    online_doctors = session.exec(
        select(func.count(Doctor.id))
    ).one()
    
    return AnalyticsResponse(
        total_patients=total_patients,
        total_visits=total_visits,
        visits_waiting=visits_waiting,
        visits_in_progress=visits_in_progress,
        visits_completed=visits_completed,
        avg_severity_score=round(avg_severity, 2),
        online_doctors=online_doctors
    )


# ============================================================================
# Doctor Management Endpoints
# ============================================================================

@router.get("/doctors", response_model=list[DoctorResponse])
def list_all_doctors(session: Session = Depends(get_session)):
    """Get list of all doctors"""
    query = select(Doctor).order_by(Doctor.role_tier, Doctor.name)
    doctors = session.exec(query).all()
    return list(doctors)


@router.post("/doctors", response_model=DoctorResponse, status_code=201)
def create_doctor(
    doctor_data: DoctorCreate,
    session: Session = Depends(get_session)
):
    """
    Create a new doctor (admin only)
    
    - **name**: Doctor's full name
    - **role_tier**: JUNIOR or SENIOR
    - **pin_code**: Doctor's PIN for authentication
    """
    doctor = Doctor(**doctor_data.model_dump())
    session.add(doctor)
    session.commit()
    session.refresh(doctor)
    return doctor


@router.delete("/doctors/{doctor_id}", response_model=MessageResponse)
def delete_doctor(
    doctor_id: int,
    session: Session = Depends(get_session)
):
    """Delete a doctor (admin only)"""
    doctor = session.get(Doctor, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    session.delete(doctor)
    session.commit()
    
    return MessageResponse(
        success=True,
        message=f"Doctor {doctor.name} deleted successfully"
    )


# ============================================================================
# Visit Management Endpoints
# ============================================================================

@router.get("/visits", response_model=list[VisitResponse])
def list_all_visits(
    status: VisitStatus | None = None,
    session: Session = Depends(get_session)
):
    """
    Get all visits with optional status filter
    
    - **status**: Optional filter by WAITING, IN_PROGRESS, or COMPLETED
    """
    query = select(Visit)
    
    if status:
        query = query.where(Visit.status == status)
    
    query = query.order_by(Visit.created_at.desc())
    visits = session.exec(query).all()
    
    return list(visits)
