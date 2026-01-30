/**
 * Audio recording service using Web Audio API
 * Records audio from user's microphone
 */

let mediaRecorder = null;
let audioChunks = [];

// ============================================================================
// Recording Functions
// ============================================================================

export const startRecording = async () => {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

        mediaRecorder = new MediaRecorder(stream, {
            mimeType: 'audio/webm', // Supported by most browsers
        });

        audioChunks = [];

        mediaRecorder.addEventListener('dataavailable', (event) => {
            if (event.data.size > 0) {
                audioChunks.push(event.data);
            }
        });

        mediaRecorder.start();
        return true;
    } catch (error) {
        console.error('Error starting recording:', error);
        throw new Error('Failed to access microphone. Please grant permission.');
    }
};

export const stopRecording = () => {
    return new Promise((resolve, reject) => {
        if (!mediaRecorder || mediaRecorder.state === 'inactive') {
            reject(new Error('No active recording'));
            return;
        }

        mediaRecorder.addEventListener('stop', () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });

            // Stop all tracks
            mediaRecorder.stream.getTracks().forEach(track => track.stop());

            resolve(audioBlob);
        });

        mediaRecorder.stop();
    });
};

export const isRecording = () => {
    return mediaRecorder && mediaRecorder.state === 'recording';
};

export const cancelRecording = () => {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
        mediaRecorder.stream.getTracks().forEach(track => track.stop());
        audioChunks = [];
    }
};

// ============================================================================
// Audio Playback (for preview)
// ============================================================================

export const createAudioURL = (audioBlob) => {
    return URL.createObjectURL(audioBlob);
};

export const revokeAudioURL = (url) => {
    URL.revokeObjectURL(url);
};
