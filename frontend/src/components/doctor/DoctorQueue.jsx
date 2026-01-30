/**
 * Doctor Queue - Shows patients assigned to doctor's tier
 */
import { useNavigate } from 'react-router-dom';
import { getCurrentUser } from '../../services/authService';
import { useDoctorQueue } from '../../services/doctorService';
import Header from '../common/Header';
import Button from '../common/Button';
import Spinner from '../common/Spinner';
import SeverityBadge from '../common/SeverityBadge';

export default function DoctorQueue() {
    const navigate = useNavigate();
    const user = getCurrentUser();
    const { data: queueData, isLoading, error } = useDoctorQueue(user?.user_id);

    if (isLoading) return <Spinner size="large" message="Loading queue..." />;
    if (error) return <div className="p-8 text-red-600 text-center text-xl">Error: {error.message}</div>;

    const { visits = [], total_waiting = 0 } = queueData || {};

    return (
        <div className="min-h-screen bg-gray-100">
            <Header title={`Dr. ${user?.name || 'Doctor'} - Queue`} showLogout={true} />

            <div className="max-w-4xl mx-auto mt-8 p-6">
                {/* Stats */}
                <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
                    <div className="flex justify-between items-center">
                        <div>
                            <h2 className="text-2xl font-bold text-gray-800">Your Queue</h2>
                            <p className="text-gray-600 mt-1">{total_waiting} patients waiting</p>
                        </div>
                        <div className="text-right">
                            <p className="text-sm text-gray-600">Role</p>
                            <p className="text-xl font-bold text-green-600">{user?.role?.toUpperCase()}</p>
                        </div>
                    </div>
                </div>

                {/* Patient List */}
                {visits.length === 0 ? (
                    <div className="bg-white rounded-xl shadow-lg p-12 text-center">
                        <p className="text-2xl text-gray-500">No patients in queue</p>
                    </div>
                ) : (
                    <div className="space-y-4">
                        {visits.map((visit) => (
                            <div
                                key={visit.id}
                                className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow cursor-pointer"
                                onClick={() => navigate(`/doctor/patient/${visit.id}`)}
                            >
                                <div className="flex justify-between items-start mb-3">
                                    <div>
                                        <h3 className="text-xl font-bold text-gray-800">{visit.patient_name}</h3>
                                        <p className="text-gray-600">Phone: {visit.patient_phone}</p>
                                    </div>
                                    <SeverityBadge
                                        level={visit.severity_score >= 0.7 ? 'HIGH' : visit.severity_score >= 0.4 ? 'MEDIUM' : 'LOW'}
                                        score={visit.severity_score}
                                    />
                                </div>

                                <div className="bg-gray-50 rounded-lg p-4 mb-3">
                                    <p className="text-gray-800 text-base"><strong>Symptoms:</strong> {visit.symptoms_raw}</p>
                                </div>

                                {visit.patient_chronic_history && (
                                    <p className="text-sm text-gray-600"><strong>History:</strong> {visit.patient_chronic_history}</p>
                                )}

                                <div className="mt-4">
                                    <Button size="medium" variant="success" fullWidth={false}>
                                        View Details →
                                    </Button>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}
