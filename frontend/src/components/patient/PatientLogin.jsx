/**
 * Patient Login - ATM/Kiosk style
 */
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { usePatientLogin } from '../../services/authService';
import Header from '../common/Header';
import Button from '../common/Button';
import InputField from '../common/InputField';
import Spinner from '../common/Spinner';

export default function PatientLogin() {
    const navigate = useNavigate();
    const [phoneNumber, setPhoneNumber] = useState('');
    const [pin, setPin] = useState('');
    const [error, setError] = useState('');

    const loginMutation = usePatientLogin();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        try {
            await loginMutation.mutateAsync({ phone_number: phoneNumber, pin });
            navigate('/patient/home');
        } catch (err) {
            setError(err.message || 'Login failed');
        }
    };

    return (
        <div className="min-h-screen bg-gray-100">
            <Header title="Patient Login" />

            <div className="max-w-md mx-auto mt-12 p-8 bg-white rounded-2xl shadow-xl">
                <form onSubmit={handleSubmit} className="space-y-6">
                    <InputField
                        label="Phone Number"
                        type="tel"
                        value={phoneNumber}
                        onChange={(e) => setPhoneNumber(e.target.value)}
                        placeholder="Enter your phone number"
                        required
                    />

                    <InputField
                        label="PIN"
                        type="password"
                        value={pin}
                        onChange={(e) => setPin(e.target.value)}
                        placeholder="Enter your 4-digit PIN"
                        required
                        error={error}
                    />

                    {loginMutation.isPending ? (
                        <Spinner size="medium" message="Logging in..." />
                    ) : (
                        <>
                            <Button type="submit" variant="primary">
                                Login
                            </Button>
                            <Button
                                type="button"
                                variant="secondary"
                                onClick={() => navigate('/patient/register')}
                            >
                                New Patient? Register
                            </Button>
                        </>
                    )}
                </form>
            </div>
        </div>
    );
}
