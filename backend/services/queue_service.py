"""
Queue assignment and management service
Assigns patients to appropriate doctor tier based on severity
"""
from sqlmodel import Session, select
from models import Visit, Doctor
from utils.constants import RoleTier, VisitStatus, QUEUE_ASSIGNMENT, SeverityLevel
from typing import Optional

class QueueService:
    """Queue management and assignment logic"""
    
    def assign_to_tier(self, severity_level: SeverityLevel) -> RoleTier:
        """
        Assign patient to doctor tier based on severity
        
        HIGH severity → SENIOR doctors
        MEDIUM/LOW severity → JUNIOR doctors
        
        Args:
            severity_level: Patient severity level
        
        Returns:
            RoleTier enum
        """
        return QUEUE_ASSIGNMENT[severity_level]
    
    def get_queue_position(self, session: Session, visit_id: int) -> int:
        """
        Calculate patient's position in queue
        
        Args:
            session: Database session
            visit_id: Visit ID to find position for
        
        Returns:
            int: Queue position (1-indexed)
        """
        # Get the visit
        visit = session.get(Visit, visit_id)
        if not visit:
            return 0
        
        # Count visits in same tier with higher severity or earlier creation
        query = select(Visit).where(
            Visit.assigned_tier == visit.assigned_tier,
            Visit.status == VisitStatus.WAITING,
            (Visit.severity_score > visit.severity_score) | 
            ((Visit.severity_score == visit.severity_score) & (Visit.created_at < visit.created_at))
        )
        
        earlier_visits = session.exec(query).all()
        return len(earlier_visits) + 1
    
    def estimate_wait_time(self, queue_position: int) -> int:
        """
        Estimate wait time in minutes based on queue position
        
        Args:
            queue_position: Position in queue (1-indexed)
        
        Returns:
            int: Estimated wait time in minutes
        """
        # Assume average consultation time: 15 minutes
        avg_consultation_time = 15
        return (queue_position - 1) * avg_consultation_time
    
    def get_doctor_queue(
        self, 
        session: Session, 
        doctor_id: int
    ) -> list[Visit]:
        """
        Get queue for a specific doctor (filtered by their role tier)
        
        Args:
            session: Database session
            doctor_id: Doctor ID
        
        Returns:
            List of visits sorted by severity (highest first)
        """
        # Get doctor
        doctor = session.get(Doctor, doctor_id)
        if not doctor:
            return []
        
        # Get visits assigned to this doctor's tier, waiting or in progress
        query = select(Visit).where(
            Visit.assigned_tier == doctor.role_tier,
            Visit.status.in_([VisitStatus.WAITING, VisitStatus.IN_PROGRESS])
        ).order_by(Visit.severity_score.desc(), Visit.created_at.asc())
        
        visits = session.exec(query).all()
        return list(visits)
    
    def assign_visit_to_doctor(
        self, 
        session: Session, 
        visit_id: int, 
        doctor_id: int
    ) -> bool:
        """
        Assign a visit to a doctor and mark as IN_PROGRESS
        
        Args:
            session: Database session
            visit_id: Visit ID
            doctor_id: Doctor ID
        
        Returns:
            bool: True if successful
        """
        visit = session.get(Visit, visit_id)
        doctor = session.get(Doctor, doctor_id)
        
        if not visit or not doctor:
            return False
        
        # Verify doctor tier matches visit assignment
        if doctor.role_tier != visit.assigned_tier:
            print(f"⚠️  Doctor tier mismatch: {doctor.role_tier} != {visit.assigned_tier}")
            return False
        
        visit.doctor_id = doctor_id
        visit.status = VisitStatus.IN_PROGRESS
        session.add(visit)
        session.commit()
        session.refresh(visit)
        
        return True

# Global instance
queue_service = QueueService()
