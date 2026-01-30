/**
 * Header component for all pages
 */
import { useNavigate } from 'react-router-dom';
import { logout } from '../../services/authService';

export default function Header({ title, showLogout = false }) {
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/');
    };

    return (
        <header className="bg-blue-600 text-white py-6 px-6 shadow-lg">
            <div className="max-w-4xl mx-auto flex justify-between items-center">
                <h1 className="text-3xl font-bold">{title}</h1>
                {showLogout && (
                    <button
                        onClick={handleLogout}
                        className="bg-white text-blue-600 px-6 py-3 rounded-lg font-semibold hover:bg-gray-100"
                    >
                        Logout
                    </button>
                )}
            </div>
        </header>
    );
}
