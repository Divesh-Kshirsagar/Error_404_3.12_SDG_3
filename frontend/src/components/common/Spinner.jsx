/**
 * Spinner/Loading component
 */
export default function Spinner({ size = 'medium', message = 'Loading...' }) {
    const sizeClasses = {
        small: 'w-8 h-8',
        medium: 'w-16 h-16',
        large: 'w-24 h-24',
    };

    return (
        <div className="flex flex-col items-center justify-center py-12">
            <div className={`${sizeClasses[size]} border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin`}></div>
            {message && <p className="mt-4 text-lg text-gray-600">{message}</p>}
        </div>
    );
}
