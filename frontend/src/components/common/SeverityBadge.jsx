/**
 * Severity Badge component - color-coded severity indicator
 */
export default function SeverityBadge({ level, score }) {
    const badgeStyles = {
        HIGH: 'bg-red-100 text-red-800 border-red-300',
        MEDIUM: 'bg-yellow-100 text-yellow-800 border-yellow-300',
        LOW: 'bg-green-100 text-green-800 border-green-300',
    };

    const badgeIcons = {
        HIGH: '🔴',
        MEDIUM: '🟡',
        LOW: '🟢',
    };

    return (
        <span className={`inline-flex items-center gap-2 px-4 py-2 rounded-full border-2 font-semibold text-base ${badgeStyles[level]}`}>
            <span>{badgeIcons[level]}</span>
            <span>{level}</span>
            {score !== undefined && <span className="text-sm">({(score * 100).toFixed(0)}%)</span>}
        </span>
    );
}
