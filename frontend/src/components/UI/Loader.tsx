import React from 'react';

interface LoaderProps {
    size?: 'sm' | 'md' | 'lg';
    overlay?: boolean;
    message?: string;
}

const Loader: React.FC<LoaderProps> = ({
    size = 'md',
    overlay = false,
    message
}) => {
    const sizeClasses = {
        sm: 'h-6 w-6',
        md: 'h-10 w-10',
        lg: 'h-16 w-16',
    };

    const spinner = (
        <div className="flex flex-col items-center justify-center gap-3">
            <div className={`animate-spin rounded-full border-b-2 border-primary-600 ${sizeClasses[size]}`}></div>
            {message && <p className="text-sm text-gray-600">{message}</p>}
        </div>
    );

    if (overlay) {
        return (
            <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                <div className="bg-white rounded-lg p-6">
                    {spinner}
                </div>
            </div>
        );
    }

    return (
        <div className="flex items-center justify-center py-12">
            {spinner}
        </div>
    );
};

export default Loader;
