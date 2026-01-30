from enum import Enum

class RoleTier(str, Enum):
    """Doctor role tier for queue assignment"""
    JUNIOR = "JUNIOR"
    SENIOR = "SENIOR"

class VisitStatus(str, Enum):
    """Visit status throughout the queue workflow"""
    WAITING = "WAITING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

class SeverityLevel(str, Enum):
    """Patient severity classification"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

# Risk score thresholds for severity classification
RISK_THRESHOLD_HIGH = 0.7  # severity_score >= 0.7 → HIGH
RISK_THRESHOLD_MEDIUM = 0.4  # severity_score >= 0.4 → MEDIUM, else LOW

# Queue assignment rules
QUEUE_ASSIGNMENT = {
    SeverityLevel.HIGH: RoleTier.SENIOR,
    SeverityLevel.MEDIUM: RoleTier.JUNIOR,
    SeverityLevel.LOW: RoleTier.JUNIOR,
}
