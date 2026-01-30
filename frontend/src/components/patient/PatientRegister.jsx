/**
 * Patient Registration - Simple form
 */
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useRegisterPatient } from '../../services/patientService';
import Header from '../common/Header';
import Button from '../common/Button';
import InputField from '../common/InputField';
import Spinner from '../common/Spinner';

export default function PatientRegister() {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        phone_number: '',
        full_name: '',
        yob: '',
        pin: '',
        chronic_history: '',
    });
    const [error, setError] = useState('');

    const registerMutation = useRegisterPatient();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        // Combine YOB and PIN
        const yob_pin = `${formData.yob}#${formData.pin}`;

        try {
            await registerMutation.mutateAsync({
                phone_number: formData.phone_number,
                full_name: formData.full_name,
                yob_pin,
                chronic_history: formData.chronic_history || null,
            });

            alert('Registration successful! Please login.');
            navigate('/patient');
        } catch (err) {
            setError(err.message || 'Registration failed');
        }
    };

    return (
        <div className="min-h-screen bg-gray-100">
            <Header title="Patient Registration" />

            <div className="max-w-md mx-auto mt-12 p-8 bg-white rounded-2xl shadow-xl">
                <form onSubmit={handleSubmit} className="space-y-6">
                    <InputField
                        label="Full Name"
                        value={formData.full_name}
                        onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                        required
                    />

                    <InputField
                        label="Phone Number"
                        type="tel"
                        value={formData.phone_number}
                        onChange={(e) => setFormData({ ...formData, phone_number: e.target.value })}
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
                        label="4-Digit PIN"
                        type="password"
                        value={formData.pin}
                        onChange={(e) => setFormData({ ...formData, pin: e.target.value })}
                        placeholder="Create a PIN"
                        required
                    />

                    <InputField
                        label="Chronic Conditions (Optional)"
                        value={formData.chronic_history}
                        onChange={(e) => setFormData({ ...formData, chronic_history: e.target.value })}
                        placeholder="e.g., Diabetes, Hypertension"
                    />

                    {error && <p className="text-red-600 text-center">{error}</p>}

                    {registerMutation.isPending ? (
                        <Spinner size="medium" message="Registering..." />
                    ) : (
                        <>
                            <Button type="submit" variant="primary">Register</Button>
                            <Button type="button" variant="secondary" onClick={() => navigate('/patient')}>
                                Back to Login
                            </Button>
                        </>
                    )}
                </form>
            </div>
        </div>
    );
}
