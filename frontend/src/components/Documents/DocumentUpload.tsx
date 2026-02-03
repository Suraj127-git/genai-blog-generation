import React, { useCallback } from 'react';
import { useAppDispatch } from '../../hooks/redux';
import { uploadDocument } from '../../features/documents/documentsSlice';

interface DocumentUploadProps {
    onUploadSuccess?: (docId: string) => void;
}

const DocumentUpload: React.FC<DocumentUploadProps> = ({ onUploadSuccess }) => {
    const dispatch = useAppDispatch();
    const [isDragging, setIsDragging] = React.useState(false);
    const [uploading, setUploading] = React.useState(false);
    const [error, setError] = React.useState<string | null>(null);

    const handleDragOver = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(true);
    }, []);

    const handleDragLeave = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);
    }, []);

    const handleDrop = useCallback(async (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);

        const files = Array.from(e.dataTransfer.files);
        if (files.length > 0) {
            await handleFileUpload(files[0]);
        }
    }, []);

    const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const files = e.target.files;
        if (files && files.length > 0) {
            await handleFileUpload(files[0]);
        }
    };

    const handleFileUpload = async (file: File) => {
        setError(null);

        // Validate file type
        const validExtensions = ['.pdf', '.txt', '.docx'];
        const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase();

        if (!validExtensions.includes(fileExtension)) {
            setError('Invalid file type. Only PDF, TXT, and DOCX files are allowed.');
            return;
        }

        // Validate file size (10MB)
        const maxSize = 10 * 1024 * 1024;
        if (file.size > maxSize) {
            setError('File size exceeds 10MB limit.');
            return;
        }

        setUploading(true);
        try {
            const result = await dispatch(uploadDocument(file));
            if (uploadDocument.fulfilled.match(result)) {
                if (onUploadSuccess) {
                    onUploadSuccess(result.payload.id);
                }
            } else if (uploadDocument.rejected.match(result)) {
                setError(result.payload as string || 'Upload failed');
            }
        } catch (err) {
            setError('Upload failed. Please try again.');
        } finally {
            setUploading(false);
        }
    };

    return (
        <div>
            <div
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                className={`border-2 border-dashed rounded-lg p-8 text-center transition-all ${isDragging
                        ? 'border-primary-500 bg-primary-50'
                        : 'border-gray-300 hover:border-primary-400 bg-white'
                    }`}
            >
                <input
                    type="file"
                    accept=".pdf,.txt,.docx"
                    onChange={handleFileSelect}
                    className="hidden"
                    id="file-upload-input"
                    disabled={uploading}
                />

                <label htmlFor="file-upload-input" className="cursor-pointer">
                    <div className="flex flex-col items-center">
                        {uploading ? (
                            <>
                                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mb-4"></div>
                                <p className="text-sm font-medium text-gray-700">Uploading...</p>
                            </>
                        ) : (
                            <>
                                <svg
                                    className="w-12 h-12 text-gray-400 mb-4"
                                    fill="none"
                                    stroke="currentColor"
                                    viewBox="0 0 24 24"
                                >
                                    <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        strokeWidth={2}
                                        d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                                    />
                                </svg>
                                <p className="text-sm font-medium text-gray-700 mb-1">
                                    {isDragging ? 'Drop file here' : 'Click to upload or drag and drop'}
                                </p>
                                <p className="text-xs text-gray-500">
                                    PDF, TXT, DOCX (max 10MB)
                                </p>
                            </>
                        )}
                    </div>
                </label>
            </div>

            {error && (
                <div className="mt-3 bg-red-50 border border-red-200 text-red-800 px-4 py-2 rounded-lg text-sm">
                    {error}
                </div>
            )}
        </div>
    );
};

export default DocumentUpload;
