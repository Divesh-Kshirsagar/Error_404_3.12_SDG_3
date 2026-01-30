/**
 * Patient Auth - Combined Login/Register in one page
 * Auto-registers if patient doesn't exist
 */
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { usePatientLogin } from '../../services/authService';
import { useRegisterPatient } from '../../services/patientService';
import Header from '../common/Header';
import Button from '../common/Button';
import InputField from '../common/InputField';
import Spinner from '../common/Spinner';

export default function PatientAuth() {
    const navigate = useNavigate();
    const [step, setStep] = useState('auth'); // 'auth' or 'register'
    const [formData, setFormData] = useState({
        phone_number: '',
        pin: '',
        full_name: '',
        yob: '',
        chronic_history: '',
    });
    const [error, setError] = useState('');

    const loginMutation = usePatientLogin();
    const registerMutation = useRegisterPatient();

    const handleAuthSubmit = async (e) => {
        e.preventDefault();
        setError('');

        try {
            // Try to login first
            await loginMutation.mutateAsync({
                phone_number: formData.phone_number,
                pin: formData.pin
            });
            navigate('/patient/home');
        } catch (err) {
            // If login fails (patient doesn't exist), go to registration step
            if (err.message.includes('not found') || err.message.includes('404')) {
                setStep('register');
            } else {
                setError(err.message || 'Authentication failed');
            }
        }
    };

    const handleRegisterSubmit = async (e) => {
        e.preventDefault();
        setError('');

        const yob_pin = `${formData.yob}#${formData.pin}`;

        try {
            // Register the patient
            await registerMutation.mutateAsync({
                phone_number: formData.phone_number,
                full_name: formData.full_name,
                yob_pin,
                chronic_history: formData.chronic_history || null,
            });

            // Auto-login after registration
            await loginMutation.mutateAsync({
                phone_number: formData.phone_number,
                pin: formData.pin
            });

            navigate('/patient/home');
        } catch (err) {
            setError(err.message || 'Registration failed');
        }
    };

    const isLoading = loginMutation.isPending || registerMutation.isPending;

    return (
        <div className="min-h-screen bg-gray-100">
            <Header title="Patient Portal" />

            <div className="max-w-md mx-auto mt-12 p-8 bg-white rounded-2xl shadow-xl">
                {step === 'auth' ? (
                    // Step 1: Phone + PIN
                    <form onSubmit={handleAuthSubmit} className="space-y-6">
                        <div className="text-center mb-6">
                            <h2 className="text-2xl font-bold text-gray-800">Welcome!</h2>
                            <p className="text-gray-600 mt-2">Enter your details to continue</p>
                        </div>

                        <InputField
                            label="Phone Number"
                            type="tel"
                            value={formData.phone_number}
                            onChange={(e) => setFormData({ ...formData, phone_number: e.target.value })}
                            placeholder="Enter your phone number"
                            required
                        />

                        <InputField
                            label="PIN (4 digits)"
                            type="password"
                            value={formData.pin}
                            onChange={(e) => setFormData({ ...formData, pin: e.target.value })}
                            placeholder="Enter your PIN"
                            required
                            error={error}
                        />

                        {isLoading ? (
                            <Spinner size="medium" message="Checking..." />
                        ) : (
                            <Button type="submit" variant="primary">
                                Continue
                            </Button>
                        )}
                    </form>
                ) : (
                    // Step 2: Complete Registration (only shown if patient doesn't exist)
                    <form onSubmit={handleRegisterSubmit} className="space-y-6">
                        <div className="text-center mb-6">
                            <h2 className="text-2xl font-bold text-gray-800">New Patient</h2>
                            <p className="text-gray-600 mt-2">Please complete your registration</p>
                        </div>

                        <InputField
                            label="Full Name"
                            value={formData.full_name}
                            onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                            placeholder="Enter your full name"
                            required
                        />

                        <InputField
                            label="Year of Birth"
                            type="number"
                            value={formData.yob}
                            onChange={(e) => setFormData({ ...formData, yob: e.target.value })}
                            placeholder="e.g., 1990"
                            required
                        />

                        <InputField
                            label="Chronic Conditions (Optional)"
                            value={formData.chronic_history}
                            onChange={(e) => setFormData({ ...formData, chronic_history: e.target.value })}
                            placeholder="e.g., Diabetes, Hypertension"
                        />

                        {error && <p className="text-red-600 text-center font-medium">{error}</p>}

                        {isLoading ? (
                            <Spinner size="medium" message="Registering..." />
                        ) : (
                            <div className="space-y-4">
                                <Button type="submit" variant="primary">
                                    Complete Registration
                                </Button>
                                <Button
                                    type="button"
                                    variant="secondary"
                                    onClick={() => {
                                        setStep('auth');
                                        setError('');
                                    }}
                                >
                                    Back
                                </Button>
                            </div>
                        )}
                    </form>
                )}
            </div>
        </div>
    );
}
