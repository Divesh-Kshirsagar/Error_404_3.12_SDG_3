/**
 * Common Button component - ATM/Kiosk style
 * Large, easy to tap, minimal design
 */
export default function Button({
    children,
    onClick,
    variant = 'primary',
    fullWidth = true,
    disabled = false,
    size = 'large',
    type = 'button'
}) {
    const baseClasses = 'font-semibold rounded-xl transition-all duration-200 shadow-lg';

    const sizeClasses = {
        large: 'py-6 px-8 text-xl',
        medium: 'py-4 px-6 text-lg',
        small: 'py-3 px-4 text-base',
    };

    const variantClasses = {
        primary: 'bg-blue-600 text-white hover:bg-blue-700 active:bg-blue-800',
        success: 'bg-green-600 text-white hover:bg-green-700 active:bg-green-800',
        danger: 'bg-red-600 text-white hover:bg-red-700 active:bg-red-800',
        secondary: 'bg-gray-200 text-gray-800 hover:bg-gray-300 active:bg-gray-400',
        outline: 'border-2 border-blue-600 text-blue-600 hover:bg-blue-50 active:bg-blue-100',
    };

    const widthClass = fullWidth ? 'w-full' : '';
    const disabledClass = disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer';

    return (
        <button
            type={type}
            onClick={onClick}
            disabled={disabled}
            className={`${baseClasses} ${sizeClasses[size]} ${variantClasses[variant]} ${widthClass} ${disabledClass}`}
        >
            {children}
        </button>
    );
}
