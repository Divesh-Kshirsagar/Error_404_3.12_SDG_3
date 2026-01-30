/**
 * Admin Dashboard - Analytics and Doctor Management
 */
import { getCurrentUser } from '../../services/authService';
import { useAnalytics, useAllDoctors } from '../../services/adminService';
import Header from '../common/Header';
import Spinner from '../common/Spinner';

export default function AdminDashboard() {
    const user = getCurrentUser();
    const { data: analytics, isLoading: analyticsLoading } = useAnalytics();
    const { data: doctors, isLoading: doctorsLoading } = useAllDoctors();

    if (analyticsLoading || doctorsLoading) {
        return <Spinner size="large" message="Loading dashboard..." />;
    }

    const stats = [
        { label: 'Total Patients', value: analytics?.total_patients || 0, color: 'blue' },
        { label: 'Total Visits', value: analytics?.total_visits || 0, color: 'green' },
        { label: 'Waiting', value: analytics?.visits_waiting || 0, color: 'yellow' },
        { label: 'In Progress', value: analytics?.visits_in_progress || 0, color: 'orange' },
        { label: 'Completed', value: analytics?.visits_completed || 0, color: 'green' },
        { label: 'Avg Severity', value: (analytics?.avg_severity_score * 100).toFixed(0) + '%', color: 'red' },
    ];

    return (
        <div className="min-h-screen bg-gray-100">
            <Header title={`Admin - ${user?.name || 'Dashboard'}`} showLogout={true} />

            <div className="max-w-6xl mx-auto mt-8 p-6 space-y-6">
                {/* Stats Grid */}
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                    {stats.map((stat, idx) => (
                        <div key={idx} className="bg-white rounded-xl shadow-lg p-6 text-center">
                            <p className="text-gray-600 text-sm font-semibold mb-2">{stat.label}</p>
                            <p className="text-4xl font-bold text-gray-800">{stat.value}</p>
                        </div>
                    ))}
                </div>

                {/* Doctors List */}
                <div className="bg-white rounded-xl shadow-lg p-6">
                    <h2 className="text-2xl font-bold text-gray-800 mb-4">Doctors ({doctors?.length || 0})</h2>
                    <div className="space-y-3">
                        {doctors?.map((doctor) => (
                            <div key={doctor.id} className="flex justify-between items-center p-4 bg-gray-50 rounded-lg">
                                <div>
                                    <p className="font-semibold text-gray-800">{doctor.name}</p>
                                    <p className="text-sm text-gray-600">ID: {doctor.id}</p>
                                </div>
                                <span className={`px-4 py-2 rounded-full font-semibold ${doctor.role_tier === 'SENIOR'
                                        ? 'bg-purple-100 text-purple-800'
                                        : 'bg-blue-100 text-blue-800'
                                    }`}>
                                    {doctor.role_tier}
                                </span>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}
