/**
 * Input Field component - Large, clear, easy to read
 */
export default function InputField({
    label,
    type = 'text',
    value,
    onChange,
    placeholder = '',
    required = false,
    disabled = false,
    error = null
}) {
    return (
        <div className="w-full mb-6">
            {label && (
                <label className="block text-lg font-semibold text-gray-700 mb-3">
                    {label} {required && <span className="text-red-500">*</span>}
                </label>
            )}
            <input
                type={type}
                value={value}
                onChange={onChange}
                placeholder={placeholder}
                required={required}
                disabled={disabled}
                className={`w-full px-6 py-5 text-xl border-2 rounded-xl focus:outline-none focus:ring-4 transition-all ${error
                        ? 'border-red-500 focus:border-red-500 focus:ring-red-200'
                        : 'border-gray-300 focus:border-blue-500 focus:ring-blue-200'
                    } ${disabled ? 'bg-gray-100 cursor-not-allowed' : 'bg-white'}`}
            />
            {error && (
                <p className="mt-2 text-red-600 text-base font-medium">{error}</p>
            )}
        </div>
    );
}
