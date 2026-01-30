"""
Database migration and seed data script
Initializes database with test doctors for development
"""
from database import get_session_context, create_db_and_tables
from models import Doctor, Patient
from utils.constants import RoleTier

def seed_doctors():
    """Create initial test doctors"""
    doctors_data = [
        {
            "name": "Dr. Priya Sharma",
            "role_tier": RoleTier.SENIOR,
            "pin_code": "1234",
        },
        {
            "name": "Dr. Rajesh Kumar",
            "role_tier": RoleTier.SENIOR,
            "pin_code": "5678",
        },
        {
            "name": "Dr. Anita Desai",
            "role_tier": RoleTier.JUNIOR,
            "pin_code": "2345",
        },
        {
            "name": "Dr. Vikram Singh",
            "role_tier": RoleTier.JUNIOR,
            "pin_code": "6789",
        },
        {
            "name": "Dr. Meena Patel",
            "role_tier": RoleTier.JUNIOR,
            "pin_code": "3456",
        },
    ]
    
    with get_session_context() as session:
        # Check if doctors already exist
        existing_doctors = session.query(Doctor).first()
        if existing_doctors:
            print("⚠️  Doctors already exist, skipping seed")
            return
        
        # Create doctors
        for data in doctors_data:
            doctor = Doctor(**data)
            session.add(doctor)
        
        session.commit()
        print(f"✅ Seeded {len(doctors_data)} doctors")

def seed_test_patient():
    """Create a test patient for development"""
    test_patient_data = {
        "phone_number": "9876543210",
        "yob_pin": "1990#1111",  # YOB: 1990, PIN: 1111
        "full_name": "Test Patient",
        "chronic_history": "Hypertension",
    }
    
    with get_session_context() as session:
        # Check if test patient exists
        existing_patient = session.query(Patient).filter(
            Patient.phone_number == test_patient_data["phone_number"]
        ).first()
        
        if existing_patient:
            print("⚠️  Test patient already exists, skipping")
            return
        
        patient = Patient(**test_patient_data)
        session.add(patient)
        session.commit()
        print("✅ Created test patient (Phone: 9876543210, PIN: 1111)")

def run_migration():
    """Main migration function"""
    print("🔄 Starting database migration...")
    
    # Create tables
    create_db_and_tables()
    
    # Seed data
    seed_doctors()
    seed_test_patient()
    
    print("✅ Migration completed successfully!")
    print("\n📝 Test Credentials:")
    print("=" * 50)
    print("SENIOR Doctors:")
    print("  - Dr. Priya Sharma (PIN: 1234)")
    print("  - Dr. Rajesh Kumar (PIN: 5678)")
    print("\nJUNIOR Doctors:")
    print("  - Dr. Anita Desai (PIN: 2345)")
    print("  - Dr. Vikram Singh (PIN: 6789)")
    print("  - Dr. Meena Patel (PIN: 3456)")
    print("\nTest Patient:")
    print("  - Phone: 9876543210")
    print("  - PIN: 1111")
    print("=" * 50)

if __name__ == "__main__":
    run_migration()
