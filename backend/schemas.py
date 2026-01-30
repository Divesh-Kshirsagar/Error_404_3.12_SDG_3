"""
Pydantic schemas for request/response validation
Separate from database models for clean API layer
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from utils.constants import RoleTier, VisitStatus, SeverityLevel

# ============================================================================
# Authentication Schemas
# ============================================================================

class PatientLoginRequest(BaseModel):
    phone_number: str = Field(..., min_length=10, max_length=15)
    pin: str = Field(..., min_length=4, max_length=4)

class DoctorLoginRequest(BaseModel):
    doctor_id: int
    pin: str = Field(..., min_length=4, max_length=10)

class LoginResponse(BaseModel):
    success: bool
    user_id: str | int
    role: str
    name: str

# ============================================================================
# Patient Schemas
# ============================================================================

class PatientRegister(BaseModel):
    phone_number: str = Field(..., min_length=10, max_length=15)
    yob_pin: str = Field(..., description="Format: YYYY#PIN (e.g., 1990#1234)")
    full_name: str = Field(..., min_length=2, max_length=255)
    chronic_history: Optional[str] = None

class PatientResponse(BaseModel):
    phone_number: str
    full_name: str
    chronic_history: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

# ============================================================================
# Visit Schemas
# ============================================================================

class VisitCreate(BaseModel):
    symptoms_raw: str = Field(..., min_length=5, description="Patient's symptom description")
    symptoms_extracted: Optional[dict] = Field(None, description="AI-extracted structured data from frontend")

class VisitUpdate(BaseModel):
    doctor_notes: Optional[str] = None
    prescription: Optional[str] = None
    status: Optional[VisitStatus] = None

class VisitResponse(BaseModel):
    id: int
    patient_phone: str
    symptoms_raw: str
    symptoms_extracted: Optional[dict]
    severity_score: float
    assigned_tier: RoleTier
    status: VisitStatus
    ai_summary: Optional[str]
    doctor_notes: Optional[str]
    prescription: Optional[str]
    doctor_id: Optional[int]
    created_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class VisitWithPatient(VisitResponse):
    """Visit with patient details for doctor queue"""
    patient_name: str
    patient_chronic_history: Optional[str]

# ============================================================================
# Doctor Schemas
# ============================================================================

class DoctorCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    role_tier: RoleTier
    pin_code: str = Field(..., min_length=4, max_length=10)

class DoctorResponse(BaseModel):
    id: int
    name: str
    role_tier: RoleTier
    pin_code: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# ============================================================================
# Queue & Analytics Schemas
# ============================================================================

class QueueResponse(BaseModel):
    visits: list[VisitWithPatient]
    total_waiting: int
    highest_severity: Optional[float]

class AnalyticsResponse(BaseModel):
    total_patients: int
    total_visits: int
    visits_waiting: int
    visits_in_progress: int
    visits_completed: int
    avg_severity_score: float
    online_doctors: int

# ============================================================================
# Generic Response Schemas
# ============================================================================

class MessageResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None
