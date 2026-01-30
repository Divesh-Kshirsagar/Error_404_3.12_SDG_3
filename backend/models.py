"""
Database models using SQLModel (SQLAlchemy + Pydantic)
Converted from PostgreSQL/Supabase schema to SQLite
"""
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship, JSON, Column
from utils.constants import RoleTier, VisitStatus

class Patient(SQLModel, table=True):
    """Patient model - stores patient information"""
    __tablename__ = "patients"
    
    phone_number: str = Field(primary_key=True, max_length=15, description="Patient phone (unique identifier)")
    yob_pin: str = Field(max_length=10, description="Year of birth + PIN for authentication")
    full_name: str = Field(max_length=255, description="Patient full name")
    chronic_history: Optional[str] = Field(default=None, description="Chronic health conditions")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Registration timestamp")
    
    # Relationships
    visits: list["Visit"] = Relationship(back_populates="patient")


class Doctor(SQLModel, table=True):
    """Doctor model - stores doctor information and role"""
    __tablename__ = "doctors"
    
    id: Optional[int] = Field(default=None, primary_key=True, description="Auto-increment doctor ID")
    name: str = Field(max_length=255, description="Doctor full name")
    role_tier: RoleTier = Field(description="JUNIOR or SENIOR tier")
    pin_code: str = Field(max_length=10, description="Doctor PIN for authentication")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Account creation timestamp")
    
    # Relationships
    visits: list["Visit"] = Relationship(back_populates="doctor")


class Visit(SQLModel, table=True):
    """Visit model - stores patient visits and queue information"""
    __tablename__ = "visits"
    
    id: Optional[int] = Field(default=None, primary_key=True, description="Auto-increment visit ID")
    patient_phone: str = Field(foreign_key="patients.phone_number", description="Patient phone (FK)")
    
    # Symptom data
    symptoms_raw: str = Field(description="Raw symptom text from patient")
    symptoms_extracted: Optional[dict] = Field(default=None, sa_column=Column(JSON), description="Structured JSON from AI extraction")
    
    # Risk and assignment
    severity_score: float = Field(description="ML model risk score (0-1)")
    assigned_tier: RoleTier = Field(description="Assigned doctor tier (JUNIOR/SENIOR)")
    status: VisitStatus = Field(default=VisitStatus.WAITING, description="Visit status")
    
    # Doctor notes
    ai_summary: Optional[str] = Field(default=None, description="AI-generated summary (optional)")
    doctor_notes: Optional[str] = Field(default=None, description="Doctor's clinical notes")
    prescription: Optional[str] = Field(default=None, description="Prescription details")
    
    # Doctor assignment
    doctor_id: Optional[int] = Field(default=None, foreign_key="doctors.id", description="Assigned doctor (FK)")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Visit creation time")
    completed_at: Optional[datetime] = Field(default=None, description="Visit completion time")
    
    # Relationships
    patient: Patient = Relationship(back_populates="visits")
    doctor: Optional[Doctor] = Relationship(back_populates="visits")
