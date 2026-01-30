"""
Voice Processing Pipeline

Handles voice input processing:
1. Speech-to-text conversion (using LLM/Whisper)
2. Structured data extraction from natural language
3. Symptom parsing and normalization
"""


def speech_to_text(audio_input):
    """
    Convert voice input to text
    
    Args:
        audio_input: Audio file or stream
    
    Returns:
        str: Transcribed text
    """
    pass


def extract_symptoms(text_input):
    """
    Extract structured data from patient description
    
    Uses LLM to parse free-form text like:
    "I have fever and cough for 3 days"
    
    Args:
        text_input (str): Patient's symptom description
    
    Returns:
        dict: {
            'symptoms': list,
            'duration_days': int,
            'severity': str,
            'age': int
        }
    """
    pass


def process_voice_input(audio_or_text):
    """
    Full pipeline: voice → text → structured data
    
    Args:
        audio_or_text: Audio input or text string
    
    Returns:
        dict: Structured symptom data
    """
    pass
