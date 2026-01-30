"""
Patient Kiosk Interface (Streamlit)

Entry point for patients to:
- Enter phone number and year of birth
- Describe symptoms via voice/text
- Review extracted data
- Receive token number and wait time
"""

import streamlit as st
import random
from datetime import datetime
from utils.supabase_client import get_supabase
from utils.auth import verify_patient, register_patient
from utils.voice_processing import process_text_input
from ml.risk_model import calculate_risk_score
from config import (
    SUPPORTED_LANGUAGES,
    KIOSK_TITLE,
    JUNIOR_DOCTOR_CONSULTATION_TIME_MINUTES,
    SENIOR_DOCTOR_CONSULTATION_TIME_MINUTES
)


def create_visit_record(patient_id, symptoms_data, risk_result, transcript):
    """
    Create a visit record in Supabase
    
    Args:
        patient_id: Patient identifier
        symptoms_data: Extracted symptom information
        risk_result: Risk calculation result
        transcript: Original symptom description text
    
    Returns:
        dict: Visit record with id and status
    """
    try:
        supabase = get_supabase()
        
        visit_data = {
            'patient_id': patient_id,
            'symptoms': symptoms_data.get('symptoms', []),
            'transcript': transcript,
            'risk_score': risk_result.get('score'),
            'risk_level': risk_result.get('level'),
            'doctor_tier': risk_result.get('doctor_tier'),
            'status': 'WAITING',
            'created_at': datetime.now().isoformat()
        }
        
        response = supabase.table('visits').insert(visit_data).execute()
        
        if response.data and len(response.data) > 0:
            return {
                'success': True,
                'visit': response.data[0],
                'message': 'Visit record created'
            }
        else:
            return {
                'success': False,
                'visit': None,
                'message': 'Failed to create visit record'
            }
    except Exception as e:
        return {
            'success': False,
            'visit': None,
            'message': f'Database error: {str(e)}'
        }


def init_session_state():
    """Initialize session state variables"""
    if 'step' not in st.session_state:
        st.session_state.step = 'language'
    if 'language' not in st.session_state:
        st.session_state.language = 'en'
    if 'patient_data' not in st.session_state:
        st.session_state.patient_data = {}
    if 'extracted_data' not in st.session_state:
        st.session_state.extracted_data = {}
    if 'risk_result' not in st.session_state:
        st.session_state.risk_result = {}
    if 'token_number' not in st.session_state:
        st.session_state.token_number = None
    if 'symptoms_text' not in st.session_state:
        st.session_state.symptoms_text = ""


def show_language_selection():
    """Step 1: Language selection"""
    st.title("🏥 AarogyaQueue")
    st.markdown("### Select Your Language / अपनी भाषा चुनें")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🇬🇧 English", key="lang_en", use_container_width=True):
            st.session_state.language = 'en'
            st.session_state.step = 'registration'
            st.rerun()
    
    with col2:
        if st.button("🇮🇳 हिंदी", key="lang_hi", use_container_width=True):
            st.session_state.language = 'hi'
            st.session_state.step = 'registration'
            st.rerun()
    
    with col3:
        if st.button("🇮🇳 मराठी", key="lang_mr", use_container_width=True):
            st.session_state.language = 'mr'
            st.session_state.step = 'registration'
            st.rerun()


def show_registration():
    """Step 2: Phone number and year of birth"""
    st.title("📝 Patient Registration")
    
    st.markdown("### Enter Your Details")
    
    phone = st.text_input(
        "Phone Number",
        placeholder="10-digit mobile number",
        max_chars=10,
        key="phone_input"
    )
    
    yob = st.number_input(
        "Year of Birth",
        min_value=1900,
        max_value=2024,
        value=1990,
        step=1,
        key="yob_input"
    )
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("⬅️ Back", use_container_width=True):
            st.session_state.step = 'language'
            st.rerun()
    
    with col2:
        if st.button("Next ➡️", use_container_width=True, type="primary"):
            if len(phone) == 10 and phone.isdigit():
                st.session_state.patient_data['phone'] = phone
                st.session_state.patient_data['yob'] = yob
                st.session_state.step = 'symptoms'
                st.rerun()
            else:
                st.error("Please enter a valid 10-digit phone number")


def show_symptom_input():
    """Step 3: Symptom input"""
    st.title("🎤 Describe Your Problem")
    
    st.markdown("### Tell us what's bothering you")
    st.info("Speak clearly or type your symptoms below")
    
    # For MVP: Text input (voice would be added via audio_input widget)
    symptoms_text = st.text_area(
        "Your Symptoms",
        placeholder="Example: I have fever and cough for 3 days. I am 45 years old.",
        height=150,
        key="symptoms_input"
    )
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("⬅️ Back", use_container_width=True):
            st.session_state.step = 'registration'
            st.rerun()
    
    with col2:
        if st.button("Process 🔄", use_container_width=True, type="primary"):
            if symptoms_text.strip():
                with st.spinner("Processing your information..."):
                    result = process_text_input(symptoms_text)
                    
                    if result['success']:ymptoms_text = symptoms_text  # Save transcript
                        st.session_state.s
                        st.session_state.extracted_data = result['data']
                        st.session_state.step = 'review'
                        st.rerun()
                    else:
                        st.error(f"Failed to process: {result['message']}")
            else:
                st.warning("Please describe your symptoms")


def show_review_and_confirm():
    """Step 4: Review extracted data"""
    st.title("✅ Review Your Information")
    
    data = st.session_state.extracted_data
    
    st.markdown("### Please confirm the following details:")
    
    # Display extracted information
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Name", data.get('name') or "Not provided")
        st.metric("Age", data.get('age') or "Not provided")
    
    with col2:
        st.metric("Duration", f"{data.get('duration_days') or 'N/A'} days")
        st.metric("Severity", data.get('severity') or "Not specified")
    
    st.markdown("**Symptoms:**")
    if data.get('symptoms'):
        for symptom in data['symptoms']:
            st.markdown(f"- {symptom}")
    else:
        st.markdown("- No specific symptoms extracted")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("⬅️ Edit", use_container_width=True):
            st.session_state.step = 'symptoms'
            st.rerun()
    
    with col2:
        if st.button("Confirm ✓", use_container_width=True, type="primary"):
            with st.spinner("Generating your token..."):
                # Calculate risk score
                risk_result = calculate_risk_score(st.session_state.extracted_data)
                st.session_state.risk_result = risk_result
                
                # Generate token
                st.session_state.token_number = f"T{random.randint(1000, 9999)}"
                
                patient_id = None
                try:
                    patient_info = verify_patient(
                        st.session_state.patient_data['phone'],
                        st.session_state.patient_data['yob']
                    )
                    
                    if patient_info['success']:
                        patient_id = patient_info['patient'].get('id')
                    else:
                        # Register new patient
                        registration = register_patient(
                            st.session_state.patient_data['phone'],
                            st.session_state.patient_data['yob'],
                            st.session_state.extracted_data.get('name')
                        )
                        if registration['success']:
                            patient_id = registration['patient'].get('id')
                    
                    # Create visit record
                    if patient_id:
                        visit_result = create_visit_record(
                            patient_id=patient_id,
                            symptoms_data=st.session_state.extracted_data,
                            risk_result=risk_result,
                            transcript=st.session_state.symptoms_text
                        )
                        
                        if not visit_result['success']:
                            st.warning(f"Visit record: {visit_result['message']}")
                    else:
                        st.warning("Could not create patient record")ere)
                    # For MVP: Just move to token display
                    
                except Exception as e:
                    st.warning(f"Database unavailable: {str(e)}")
                
                st.session_state.step = 'token'
                st.rerun()


def show_token_and_wait_time():
    """Step 5: Display token and wait time"""
    st.title("🎫 Your Token")
    
    risk_result = st.session_state.risk_result
    token = st.session_state.token_number
    
    # Large token display
    st.markdown(f"""
    <div style='text-align: center; padding: 40px; background-color: #f0f2f6; border-radius: 10px;'>
        <h1 style='font-size: 80px; margin: 0;'>{token}</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Risk level and queue assignment
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Risk Level", risk_result.get('level', 'UNKNOWN'))
    
    with col2:
        st.metric("Assigned To", f"{risk_result.get('doctor_tier', 'SENIOR')} Doctor")
    
    with col3:
        # Estimate wait time (simplified calculation)
        queue_position = random.randint(1, 10)  # Mock queue position
        if risk_result.get('doctor_tier') == 'JUNIOR':
            wait_time = queue_position * JUNIOR_DOCTOR_CONSULTATION_TIME_MINUTES
        else:
            wait_time = queue_position * SENIOR_DOCTOR_CONSULTATION_TIME_MINUTES
        
        st.metric("Estimated Wait", f"{wait_time} min")
    
    st.success("✅ You have been added to the queue. Please wait for your token to be called.")
    
    st.markdown("---")
    
    if st.button("🏠 Return to Home", use_container_width=True, type="primary"):
        # Reset session
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


def main():
    """Main entry point for patient kiosk interface"""
    st.set_page_config(
        page_title=KIOSK_TITLE,
        page_icon="🏥",
        layout="centered"
    )
    
    # Custom CSS for large buttons and clean UI
    st.markdown("""
    <style>
        .stButton > button {
            height: 80px;
            font-size: 24px;
            font-weight: bold;
        }
        .stTextInput > div > div > input {
            font-size: 20px;
            height: 60px;
        }
        .stNumberInput > div > div > input {
            font-size: 20px;
            height: 60px;
        }
        .stTextArea > div > div > textarea {
            font-size: 18px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    init_session_state()
    
    # Route to appropriate step
    if st.session_state.step == 'language':
        show_language_selection()
    elif st.session_state.step == 'registration':
        show_registration()
    elif st.session_state.step == 'symptoms':
        show_symptom_input()
    elif st.session_state.step == 'review':
        show_review_and_confirm()
    elif st.session_state.step == 'token':
        show_token_and_wait_time()


if __name__ == "__main__":
    main()
