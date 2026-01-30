"""
Doctor Dashboard Interface (Streamlit)

Dashboard for doctors to:
- Select role (Junior/Senior)
- View assigned queue based on patient risk
- See patient summaries with risk scores
- Enter diagnosis and move to next patient
"""

import streamlit as st
from datetime import datetime
from utils.supabase_client import get_supabase
from utils.auth import verify_doctor
from config import DASHBOARD_TITLE, DOCTOR_JUNIOR, DOCTOR_SENIOR


def fetch_next_patient(doctor_tier):
    """
    Fetch next waiting patient for specified doctor tier
    
    Args:
        doctor_tier: 'JUNIOR' or 'SENIOR'
    
    Returns:
        dict: {
            'success': bool,
            'patient': dict or None,
            'message': str
        }
    """
    try:
        supabase = get_supabase()
        
        # Fetch visits with status=WAITING and matching doctor_tier
        # Ordered by risk_score DESC (highest risk first)
        response = supabase.table('visits').select('*').eq(
            'status', 'WAITING'
        ).eq(
            'doctor_tier', doctor_tier
        ).order('risk_score', desc=True).limit(1).execute()
        
        if response.data and len(response.data) > 0:
            return {
                'success': True,
                'patient': response.data[0],
                'message': 'Patient loaded'
            }
        else:
            return {
                'success': False,
                'patient': None,
                'message': 'No patients in queue'
            }
    except Exception as e:
        return {
            'success': False,
            'patient': None,
            'message': f'Database error: {str(e)}'
        }


def mark_patient_completed(visit_id, diagnosis, doctor_notes=""):
    """
    Mark patient visit as completed with diagnosis
    
    Args:
        visit_id: Visit record ID
        diagnosis: Doctor's diagnosis
        doctor_notes: Optional notes
    
    Returns:
        dict: Success status
    """
    try:
        supabase = get_supabase()
        
        update_data = {
            'status': 'COMPLETED',
            'diagnosis': diagnosis,
            'doctor_notes': doctor_notes,
            'completed_at': datetime.now().isoformat()
        }
        
        response = supabase.table('visits').update(
            update_data
        ).eq('id', visit_id).execute()
        
        if response.data:
            return {
                'success': True,
                'message': 'Patient marked as completed'
            }
        else:
            return {
                'success': False,
                'message': 'Failed to update visit'
            }
    except Exception as e:
        return {
            'success': False,
            'message': f'Database error: {str(e)}'
        }


def init_session_state():
    """Initialize session state"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'doctor_info' not in st.session_state:
        st.session_state.doctor_info = {}
    if 'current_patient' not in st.session_state:
        st.session_state.current_patient = None
    if 'doctor_notes' not in st.session_state:
        st.session_state.doctor_notes = ""


def show_login():
    """Doctor login screen"""
    st.title("🩺 Doctor Login")
    
    col1, col2 = st.columns(2)
    
    with col1:
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
    
    with col2:
        role = st.selectbox(
            "Role",
            options=[DOCTOR_JUNIOR, DOCTOR_SENIOR],
            key="login_role"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Login 🔐", use_container_width=True, type="primary"):
            if username and password:
                result = verify_doctor(username, password, role)
                
                if result['success']:
                    st.session_state.authenticated = True
                    st.session_state.doctor_info = result['doctor']
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error(result['message'])
            else:
                st.warning("Please enter username and password")


def get_risk_badge_color(risk_level):
    """Get color for risk level badge"""
    colors = {
        'LOW': 'green',
        'MEDIUM': 'orange',
        'HIGH': 'red'
    }
    return colors.get(risk_level, 'gray')


def show_patient_card(patient_data):
    """Display patient information card"""
    
    # Header with token and risk
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        st.markdown(f"### 🎫 Token: {patient_data.get('id', 'N/A')}")
    
    with col2:
        risk_level = patient_data.get('risk_level', 'UNKNOWN')
        risk_score = patient_data.get('risk_score', 0.0)
        color = get_risk_badge_color(risk_level)
        
        st.markdown(f"""
        <div style='background-color: {color}; color: white; padding: 15px; 
        border-radius: 5px; text-align: center; font-weight: bold;'>
            {risk_level} RISK ({risk_score:.2f})
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        queue_position = st.empty()  # Placeholder for queue count
    
    st.markdown("---")
    
    # Patient Summary
    st.markdown("### 📋 AI Summary")
    
    # Transcript
    if patient_data.get('transcript'):
        st.info(f"**Patient Description:** {patient_data['transcript']}")
    
    # Symptoms
    st.markdown("**Symptoms:**")
    symptoms = patient_data.get('symptoms', [])
    if symptoms:
        for symptom in symptoms:
            st.markdown(f"- {symptom}")
    else:
        st.markdown("- No specific symptoms extracted")
    
    st.markdown("---")


def show_dashboard():
    """Main dashboard view"""
    st.title(f"🩺 {DASHBOARD_TITLE}")
    
    # Doctor info header
    doctor = st.session_state.doctor_info
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        st.markdown(f"**Dr. {doctor.get('username', 'Unknown')}** | Role: **{doctor.get('role', 'N/A')}**")
    
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.session_state.current_patient = None
            st.rerun()
    
    with col3:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.current_patient = None
            st.rerun()
    
    st.markdown("---")
    
    # Load next patient if none currently loaded
    if st.session_state.current_patient is None:
        with st.spinner("Loading next patient..."):
            result = fetch_next_patient(doctor.get('role'))
            
            if result['success']:
                st.session_state.current_patient = result['patient']
            else:
                st.info("✅ No patients waiting in your queue")
                st.markdown("### Queue is empty. Please wait for patients.")
                return
    
    # Display current patient
    patient = st.session_state.current_patient
    show_patient_card(patient)
    
    # Doctor's workspace
    st.markdown("### 🖊️ Your Notes & Diagnosis")
    
    # Notes area
    doctor_notes = st.text_area(
        "Clinical Notes (Optional)",
        value=st.session_state.doctor_notes,
        height=100,
        placeholder="Add any observations or notes here...",
        key="notes_input"
    )
    
    # Diagnosis input
    diagnosis = st.text_area(
        "Final Diagnosis *",
        height=120,
        placeholder="Enter diagnosis here (required)",
        key="diagnosis_input"
    )
    
    # Action buttons
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("")  # Spacer
    
    with col2:
        if st.button("Submit & Next ➡️", use_container_width=True, type="primary"):
            if diagnosis.strip():
                with st.spinner("Saving..."):
                    # Mark patient as completed
                    result = mark_patient_completed(
                        patient.get('id'),
                        diagnosis,
                        doctor_notes
                    )
                    
                    if result['success']:
                        st.success("✅ Patient completed!")
                        
                        # Clear current patient to auto-load next
                        st.session_state.current_patient = None
                        st.session_state.doctor_notes = ""
                        
                        # Small delay then reload
                        import time
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error(f"Failed to save: {result['message']}")
            else:
                st.warning("⚠️ Please enter a diagnosis before submitting")


def main():
    """Main entry point for doctor dashboard"""
    st.set_page_config(
        page_title=DASHBOARD_TITLE,
        page_icon="🩺",
        layout="wide"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
        .stButton > button {
            height: 50px;
            font-size: 18px;
            font-weight: bold;
        }
        .stTextArea > div > div > textarea {
            font-size: 16px;
        }
        h3 {
            margin-top: 10px;
            margin-bottom: 10px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    init_session_state()
    
    # Route based on authentication
    if not st.session_state.authenticated:
        show_login()
    else:
        show_dashboard()


if __name__ == "__main__":
    main()
