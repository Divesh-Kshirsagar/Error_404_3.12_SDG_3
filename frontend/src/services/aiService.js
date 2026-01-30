/**
 * AI Service using Groq API for transcription and symptom extraction
 * Runs on the frontend (client-side processing)
 */

const GROQ_API_KEY = import.meta.env.VITE_GROQ_API_KEY;
const GROQ_API_URL = 'https://api.groq.com/openai/v1';

// ============================================================================
// Groq Whisper Transcription
// ============================================================================

export const transcribeAudio = async (audioBlob) => {
    if (!GROQ_API_KEY) {
        throw new Error('Groq API key not configured');
    }

    const formData = new FormData();
    formData.append('file', audioBlob, 'audio.webm');
    formData.append('model', 'whisper-large-v3');
    formData.append('language', 'en'); // or 'hi' for Hindi
    formData.append('response_format', 'json');

    const response = await fetch(`${GROQ_API_URL}/audio/transcriptions`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${GROQ_API_KEY}`,
        },
        body: formData,
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error?.message || 'Transcription failed');
    }

    const data = await response.json();
    return data.text;
};

// ============================================================================
// Groq LLM Symptom Extraction
// ============================================================================

export const extractSymptoms = async (transcribedText) => {
    if (!GROQ_API_KEY) {
        throw new Error('Groq API key not configured');
    }

    const systemPrompt = `You are a medical assistant. Extract symptoms from patient descriptions and return structured JSON.
Return ONLY valid JSON in this exact format:
{
  "symptoms": ["symptom1", "symptom2"],
  "severity": "low|medium|high",
  "duration": "description of duration if mentioned",
  "notes": "any additional relevant details"
}`;

    const response = await fetch(`${GROQ_API_URL}/chat/completions`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${GROQ_API_KEY}`,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            model: 'llama-3.3-70b-versatile',
            messages: [
                { role: 'system', content: systemPrompt },
                { role: 'user', content: `Extract symptoms from: "${transcribedText}"` }
            ],
            temperature: 0.1,
            max_tokens: 500,
        }),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error?.message || 'Symptom extraction failed');
    }

    const data = await response.json();
    const content = data.choices[0]?.message?.content;

    try {
        // Try to parse JSON response
        const extracted = JSON.parse(content);
        return extracted;
    } catch (e) {
        // Fallback if LLM didn't return valid JSON
        console.error('Failed to parse LLM response:', content);
        return {
            symptoms: [transcribedText],
            severity: 'medium',
            duration: null,
            notes: 'AI extraction failed, using raw text'
        };
    }
};

// ============================================================================
// Combined Processing
// ============================================================================

export const processAudioSymptoms = async (audioBlob) => {
    try {
        // Step 1: Transcribe audio to text
        const transcribedText = await transcribeAudio(audioBlob);

        // Step 2: Extract structured symptoms from text
        const extractedData = await extractSymptoms(transcribedText);

        return {
            success: true,
            transcription: transcribedText,
            extracted: extractedData,
        };
    } catch (error) {
        throw new Error(`Audio processing failed: ${error.message}`);
    }
};
