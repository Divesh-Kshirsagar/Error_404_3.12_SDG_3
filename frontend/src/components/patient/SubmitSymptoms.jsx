/**
 * Submit Symptoms - Text input for symptoms
 * Note: Audio recording feature can be added later
 */
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getCurrentUser } from '../../services/authService';
import { useCreateVisit } from '../../services/patientService';
import Header from '../common/Header';
import Button from '../common/Button';
import Spinner from '../common/Spinner';

export default function SubmitSymptoms() {
    const navigate = useNavigate();
    const user = getCurrentUser();
    const [symptoms, setSymptoms] = useState('');
    const [error, setError] = useState('');

    const createVisitMutation = useCreateVisit();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        if (symptoms.trim().length < 10) {
            setError('Please describe your symptoms in detail (at least 10 characters)');
            return;
        }

        try {
            const visitData = {
                symptoms_raw: symptoms,
                symptoms_extracted: null, // AI extraction will be added later
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

            <div className="max-w-2xl mx-auto mt-12 p-8">
                <div className="bg-white rounded-2xl shadow-xl p-8">
                    <form onSubmit={handleSubmit} className="space-y-6">
                        <div>
                            <label className="block text-xl font-semibold text-gray-700 mb-4">
                                Describe your symptoms *
                            </label>
                            <textarea
                                value={symptoms}
                                onChange={(e) => setSymptoms(e.target.value)}
                                placeholder="Tell us what symptoms you're experiencing..."
                                required
                                rows={8}
                                className="w-full px-6 py-5 text-lg border-2 border-gray-300 rounded-xl focus:outline-none focus:ring-4 focus:border-blue-500 focus:ring-blue-200 resize-none"
                            />
                        </div>

                        {error && <p className="text-red-600 text-center font-medium">{error}</p>}

                        {createVisitMutation.isPending ? (
                            <Spinner size="medium" message="Submitting..." />
                        ) : (
                            <div className="space-y-4">
                                <Button type="submit" variant="success">
                                    Submit Symptoms
                                </Button>
                                <Button type="button" variant="secondary" onClick={() => navigate('/patient/home')}>
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
