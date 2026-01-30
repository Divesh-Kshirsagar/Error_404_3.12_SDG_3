/**
 * Patient Home - Dashboard with options
 */
import { useNavigate } from 'react-router-dom';
import { getCurrentUser } from '../../services/authService';
import Header from '../common/Header';
import Button from '../common/Button';

export default function PatientHome() {
    const navigate = useNavigate();
    const user = getCurrentUser();

    return (
        <div className="min-h-screen bg-gray-100">
            <Header title="Patient Portal" showLogout={true} />

            <div className="max-w-2xl mx-auto mt-12 p-8">
                <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
                    <h2 className="text-2xl font-bold text-gray-800 mb-2">
                        Welcome, {user?.name}!
                    </h2>
                    <p className="text-gray-600 text-lg">
                        What would you like to do today?
                    </p>
                </div>

                <div className="space-y-6">
                    <Button
                        variant="primary"
                        onClick={() => navigate('/patient/submit-symptoms')}
                    >
                        📝 Submit Symptoms
                    </Button>

                    <Button
                        variant="secondary"
                        onClick={() => navigate('/patient/history')}
                    >
                        📋 View Visit History
                    </Button>
                </div>
            </div>
        </div>
    );
}
