"""
Voice Processing Pipeline

Handles voice input processing:
1. Speech-to-text conversion (using LLM/Whisper)
2. Structured data extraction from natural language
3. Symptom parsing and normalization
"""

import os
import json
from openai import OpenAI


def convert_speech_to_text(audio_file) -> dict:
    """
    Convert audio to text using OpenAI Whisper
    
    Args:
        audio_file: Audio file object (bytes or file-like)
    
    Returns:
        dict: {
            'success': bool,
            'text': str or None,
            'message': str
        }
    """
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        if not audio_file:
            return {
                'success': False,
                'text': None,
                'message': 'No audio provided'
            }
        
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        
        return {
            'success': True,
            'text': transcript.text,
            'message': 'Transcription successful'
        }
    except Exception as e:
        return {
            'success': False,
            'text': None,
            'message': f'Transcription failed: {str(e)}'
        }


def extract_patient_data_from_text(text: str) -> dict:
    """
    Extract structured patient data from natural language text
    
    Uses LLM to parse text like:
    "My name is Ramesh, I am 45 years old, I have fever and cough for 3 days"
    
    Args:
        text: Patient's description in natural language
    
    Returns:
        dict: {
            'success': bool,
            'data': {
                'name': str or None,
                'age': int or None,
                'symptoms': list of str,
                'duration_days': int or None,
                'severity': str or None
            } or None,
            'message': str
        }
    """
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        if not text or text.strip() == "":
            return {
                'success': False,
                'data': None,
                'message': 'No text provided'
            }
        
        prompt = f"""Extract patient information from the following text.
Return ONLY a JSON object with these fields:
- name: patient's name (string or null)
- age: patient's age in years (number or null)
- symptoms: list of symptoms mentioned (array of strings, empty if none)
- duration_days: how many days symptoms have been present (number or null)
- severity: mild, moderate, or severe (string or null)

Text: {text}

Important: Do NOT diagnose. Only extract what the patient said."""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a medical data extraction assistant. Extract only what patients say, do not diagnose."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        extracted_text = response.choices[0].message.content.strip()
        
        # Remove markdown code blocks if present
        if extracted_text.startswith("```"):
            extracted_text = extracted_text.split("```")[1]
            if extracted_text.startswith("json"):
                extracted_text = extracted_text[4:]
            extracted_text = extracted_text.strip()
        
        data = json.loads(extracted_text)
        
        # Ensure symptoms is always a list
        if 'symptoms' not in data or not isinstance(data['symptoms'], list):
            data['symptoms'] = []
        
        return {
            'success': True,
            'data': {
                'name': data.get('name'),
                'age': data.get('age'),
                'symptoms': data.get('symptoms', []),
                'duration_days': data.get('duration_days'),
                'severity': data.get('severity')
            },
            'message': 'Data extracted successfully'
        }
    except json.JSONDecodeError:
        return {
            'success': False,
            'data': None,
            'message': 'Failed to parse extracted data'
        }
    except Exception as e:
        return {
            'success': False,
            'data': None,
            'message': f'Extraction failed: {str(e)}'
        }


def process_voice_input(audio_file) -> dict:
    """
    Full pipeline: audio → text → structured data
    
    Args:
        audio_file: Audio file object or None (if using text directly)
    
    Returns:
        dict: {
            'success': bool,
            'text': str or None,
            'data': dict or None,
            'message': str
        }
    """
    # Step 1: Convert speech to text
    speech_result = convert_speech_to_text(audio_file)
    
    if not speech_result['success']:
        return {
            'success': False,
            'text': None,
            'data': None,
            'message': speech_result['message']
        }
    
    # Step 2: Extract structured data
    extraction_result = extract_patient_data_from_text(speech_result['text'])
    
    if not extraction_result['success']:
        return {
            'success': False,
            'text': speech_result['text'],
            'data': None,
            'message': extraction_result['message']
        }
    
    return {
        'success': True,
        'text': speech_result['text'],
        'data': extraction_result['data'],
        'message': 'Voice processing completed successfully'
    }


def process_text_input(text: str) -> dict:
    """
    Process text input directly (when patient types instead of speaking)
    
    Args:
        text: Patient's typed description
    
    Returns:
        dict: Same format as process_voice_input
    """
    extraction_result = extract_patient_data_from_text(text)
    
    if not extraction_result['success']:
        return {
            'success': False,
            'text': text,
            'data': None,
            'message': extraction_result['message']
        }
    
    return {
        'success': True,
        'text': text,
        'data': extraction_result['data'],
        'message': 'Text processing completed successfully'
    }

