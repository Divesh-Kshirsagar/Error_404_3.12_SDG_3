/**
 * Patient Details for Doctor - View and update visit
 */
import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getCurrentUser } from '../../services/authService';
import { useVisitDetails, useUpdateVisit } from '../../services/doctorService';
import Header from '../common/Header';
import Button from '../common/Button';
import Spinner from '../common/Spinner';
import SeverityBadge from '../common/SeverityBadge';

export default function PatientDetails() {
    const { visitId } = useParams();
    const navigate = useNavigate();
    const user = getCurrentUser();
    const { data: visit, isLoading } = useVisitDetails(visitId);
    const updateMutation = useUpdateVisit();

    const [notes, setNotes] = useState('');
    const [prescription, setPrescription] = useState('');

    const handleComplete = async () => {
        try {
            await updateMutation.mutateAsync({
                visitId: parseInt(visitId),
                updateData: {
                    doctor_notes: notes,
                    prescription,
                    status: 'COMPLETED',
                },
            });
            alert('Visit completed successfully!');
            navigate('/doctor/queue');
        } catch (err) {
            alert('Error: ' + err.message);
        }
    };

    if (isLoading) return <Spinner size="large" message="Loading patient details..." />;

    return (
        <div className="min-h-screen bg-gray-100">
            <Header title="Patient Details" showLogout={true} />

            <div className="max-w-3xl mx-auto mt-8 p-6 space-y-6">
                {/* Patient Info */}
                <div className="bg-white rounded-xl shadow-lg p-6">
                    <div className="flex justify-between items-start mb-4">
                        <div>
                            <h2 className="text-2xl font-bold text-gray-800">{visit.patient_name}</h2>
                            <p className="text-gray-600">Phone: {visit.patient_phone}</p>
                        </div>
                        <SeverityBadge
                            level={visit.severity_score >= 0.7 ? 'HIGH' : visit.severity_score >= 0.4 ? 'MEDIUM' : 'LOW'}
                            score={visit.severity_score}
                        />
                    </div>

                    {visit.patient_chronic_history && (
                        <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-4">
                            <p className="font-semibold text-yellow-800">Chronic History:</p>
                            <p className="text-yellow-700">{visit.patient_chronic_history}</p>
                        </div>
                    )}

                    <div className="bg-gray-50 rounded-lg p-4">
                        <p className="font-semibold text-gray-800 mb-2">Symptoms:</p>
                        <p className="text-gray-700">{visit.symptoms_raw}</p>
                    </div>
                </div>

                {/* Doctor's Section */}
                <div className="bg-white rounded-xl shadow-lg p-6">
                    <h3 className="text-xl font-bold text-gray-800 mb-4">Clinical Notes</h3>

                    <div className="space-y-4">
                        <div>
                            <label className="block text-lg font-semibold text-gray-700 mb-2">
                                Notes
                            </label>
                            <textarea
                                value={notes}
                                onChange={(e) => setNotes(e.target.value)}
                                placeholder="Enter clinical observations..."
                                rows={5}
                                className="w-full px-4 py-3 text-base border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
                            />
                        </div>

                        <div>
                            <label className="block text-lg font-semibold text-gray-700 mb-2">
                                Prescription
                            </label>
                            <textarea
                                value={prescription}
                                onChange={(e) => setPrescription(e.target.value)}
                                placeholder="Enter prescription details..."
                                rows={4}
                                className="w-full px-4 py-3 text-base border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
                            />
                        </div>
                    </div>

                    <div className="mt-6 space-y-3">
                        {updateMutation.isPending ? (
                            <Spinner size="medium" message="Saving..." />
                        ) : (
                            <>
                                <Button variant="success" onClick={handleComplete}>
                                    Complete Visit
                                </Button>
                                <Button variant="secondary" onClick={() => navigate('/doctor/queue')}>
                                    Back to Queue
                                </Button>
                            </>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
