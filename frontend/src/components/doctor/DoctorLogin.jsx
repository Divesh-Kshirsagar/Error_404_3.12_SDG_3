/**
 * Doctor Login - Simple ID + PIN
 */
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDoctorLogin } from '../../services/authService';
import Header from '../common/Header';
import Button from '../common/Button';
import InputField from '../common/InputField';
import Spinner from '../common/Spinner';

export default function DoctorLogin() {
    const navigate = useNavigate();
    const [doctorId, setDoctorId] = useState('');
    const [pin, setPin] = useState('');
    const [error, setError] = useState('');

    const loginMutation = useDoctorLogin();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        try {
            await loginMutation.mutateAsync({
                doctor_id: parseInt(doctorId),
                pin
            });
            navigate('/doctor/queue');
        } catch (err) {
            setError(err.message || 'Login failed');
        }
    };

    return (
        <div className="min-h-screen bg-gray-100">
            <Header title="Doctor Login" />

            <div className="max-w-md mx-auto mt-12 p-8 bg-white rounded-2xl shadow-xl">
                <form onSubmit={handleSubmit} className="space-y-6">
                    <div className="text-center mb-6">
                        <h2 className="text-2xl font-bold text-gray-800">Doctor Portal</h2>
                        <p className="text-gray-600 mt-2">Enter your credentials</p>
                    </div>

                    <InputField
                        label="Doctor ID"
                        type="number"
                        value={doctorId}
                        onChange={(e) => setDoctorId(e.target.value)}
                        placeholder="Enter your doctor ID"
                        required
                    />

                    <InputField
                        label="PIN"
                        type="password"
                        value={pin}
                        onChange={(e) => setPin(e.target.value)}
                        placeholder="Enter your PIN"
                        required
                        error={error}
                    />

                    {loginMutation.isPending ? (
                        <Spinner size="medium" message="Logging in..." />
                    ) : (
                        <Button type="submit" variant="success">
                            Login
                        </Button>
                    )}
                </form>
            </div>
        </div>
    );
}
