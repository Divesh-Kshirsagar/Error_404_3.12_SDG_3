/**
 * Submit Symptoms - Voice or Text input
 * Integrates Web Audio API for recording and Groq API for processing
 */
import { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { getCurrentUser } from '../../services/authService';
import { useCreateVisit } from '../../services/patientService';
import { startRecording, stopRecording } from '../../services/audioService';
import { processAudioSymptoms } from '../../services/aiService';
import Header from '../common/Header';
import Button from '../common/Button';
import Spinner from '../common/Spinner';

export default function SubmitSymptoms() {
    const navigate = useNavigate();
    const user = getCurrentUser();

    // Form State
    const [symptoms, setSymptoms] = useState('');
    const [extractedData, setExtractedData] = useState(null);
    const [error, setError] = useState('');

    // Audio State
    const [isRecording, setIsRecording] = useState(false);
    const [isProcessingAudio, setIsProcessingAudio] = useState(false);

    const createVisitMutation = useCreateVisit();

    const handleStartRecording = async () => {
        try {
            setError('');
            await startRecording();
            setIsRecording(true);
        } catch (err) {
            setError('Could not start recording: ' + err.message);
        }
    };

    const handleStopRecording = async () => {
        try {
            setIsRecording(false);
            setIsProcessingAudio(true);

            const audioBlob = await stopRecording();

            // Send to Groq for Whisper + LLM processing
            const result = await processAudioSymptoms(audioBlob);

            if (result.success) {
                setSymptoms(result.transcription);
                setExtractedData(result.extracted);
            }
        } catch (err) {
            setError('Audio processing failed: ' + err.message);
        } finally {
            setIsProcessingAudio(false);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        if (symptoms.trim().length < 5) {
            setError('Please describe your symptoms in detail');
            return;
        }

        try {
            const visitData = {
                symptoms_raw: symptoms,
                symptoms_extracted: extractedData, // Send structured AI data if available
            };

            await createVisitMutation.mutateAsync({
                phoneNumber: user.user_id,
                visitData,
            });

            alert('Symptoms submitted successfully!');
            navigate('/patient/home');
        } catch (err) {
            setError(err.message || 'Failed to submit symptoms');
        }
    };

    return (
        <div className="min-h-screen bg-gray-100">
            <Header title="Submit Symptoms" showLogout={true} />

            <div className="max-w-2xl mx-auto mt-8 p-6">
                <div className="bg-white rounded-2xl shadow-xl p-8">
                    {/* Voice Recording Section */}
                    <div className="mb-8 text-center border-b pb-8">
                        <h2 className="text-xl font-semibold text-gray-800 mb-4">
                            🎙️ Tap to Record Symptoms
                        </h2>

                        {isProcessingAudio ? (
                            <Spinner size="medium" message="Processing audio..." />
                        ) : isRecording ? (
                            <div className="animate-pulse">
                                <Button
                                    variant="danger"
                                    fullWidth={false}
                                    onClick={handleStopRecording}
                                    className="bg-red-600 hover:bg-red-700 text-white rounded-full w-24 h-24 p-0 flex items-center justify-center mx-auto shadow-lg"
                                >
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-12 h-12">
                                        <path strokeLinecap="round" strokeLinejoin="round" d="M5.25 7.5A2.25 2.25 0 0 1 7.5 5.25h9a2.25 2.25 0 0 1 2.25 2.25v9a2.25 2.25 0 0 1-2.25 2.25h-9a2.25 2.25 0 0 1-2.25-2.25v-9Z" />
                                    </svg>
                                </Button>
                                <p className="mt-4 text-red-600 font-bold text-lg">Recording... Tap to Stop</p>
                            </div>
                        ) : (
                            <Button
                                variant="primary"
                                fullWidth={false}
                                onClick={handleStartRecording}
                                className="bg-blue-600 hover:bg-blue-700 text-white rounded-full w-24 h-24 p-0 flex items-center justify-center mx-auto shadow-lg transition-transform hover:scale-105"
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-12 h-12">
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M12 18.75a6 6 0 0 0 6-6v-1.5m-6 7.5a6 6 0 0 1-6-6v-1.5m6 7.5v3.75m-3.75 0h7.5M12 15.75a3 3 0 0 1-3-3V4.5a3 3 0 1 1 6 0v8.25a3 3 0 0 1-3 3Z" />
                                </svg>
                            </Button>
                        )}
                    </div>

                    {/* Manual Text Input Section */}
                    <form onSubmit={handleSubmit} className="space-y-6">
                        <div>
                            <label className="block text-xl font-semibold text-gray-700 mb-2">
                                Or type your symptoms
                            </label>
                            <textarea
                                value={symptoms}
                                onChange={(e) => setSymptoms(e.target.value)}
                                placeholder="Tell us what symptoms you're experiencing..."
                                required
                                rows={6}
                                className="w-full px-6 py-4 text-lg border-2 border-gray-300 rounded-xl focus:outline-none focus:ring-4 focus:border-blue-500 focus:ring-blue-200 resize-none"
                            />
                        </div>

                        {error && <p className="text-red-600 text-center font-medium bg-red-50 p-3 rounded-lg">{error}</p>}

                        {createVisitMutation.isPending ? (
                            <Spinner size="medium" message="Submitting..." />
                        ) : (
                            <div className="space-y-4">
                                <Button type="submit" variant="success" disabled={isRecording || isProcessingAudio}>
                                    Submit Symptoms
                                </Button>
                                <Button
                                    type="button"
                                    variant="secondary"
                                    onClick={() => navigate('/patient/home')}
                                    disabled={isRecording || isProcessingAudio}
                                >
                                    Cancel
                                </Button>
                            </div>
                        )}
                    </form>
                </div>
            </div>
        </div>
    );
}
