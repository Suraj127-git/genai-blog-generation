import React from 'react';
import { useAppDispatch } from '../../hooks/redux';
import { deleteDocument } from '../../features/documents/documentsSlice';

interface Document {
    id: string;
    filename: string;
    file_type: string;
    file_size: number;
    content_preview?: string;
    uploaded_at: string;
}

interface DocumentListProps {
    documents: Document[];
    onSelectDocument?: (docId: string) => void;
    selectedDocuments?: string[];
}

const DocumentList: React.FC<DocumentListProps> = ({
    documents,
    onSelectDocument,
    selectedDocuments = []
}) => {
    const dispatch = useAppDispatch();

    const handleDelete = async (docId: string, e: React.MouseEvent) => {
        e.stopPropagation();
        if (window.confirm('Are you sure you want to delete this document?')) {
            await dispatch(deleteDocument(docId));
        }
    };

    const handleSelect = (docId: string) => {
        if (onSelectDocument) {
            onSelectDocument(docId);
        }
    };

    const getFileIcon = (fileType: string) => {
        switch (fileType.toLowerCase()) {
            case 'pdf':
                return '📄';
            case 'docx':
                return '📝';
            case 'txt':
                return '📃';
            default:
                return '📄';
        }
    };

    const formatFileSize = (bytes: number) => {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
        return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
    };

    if (documents.length === 0) {
        return (
            <div className="text-center py-8 text-gray-500">
                <p>No documents uploaded yet</p>
            </div>
        );
    }

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {documents.map((doc) => {
                const isSelected = selectedDocuments.includes(doc.id);

                return (
                    <div
                        key={doc.id}
                        onClick={() => handleSelect(doc.id)}
                        className={`card cursor-pointer transition-all duration-200 border-2 ${isSelected
                                ? 'border-primary-500 bg-primary-50'
                                : 'border-gray-200 hover:border-primary-300 hover:shadow-md'
                            }`}
                    >
                        <div className="flex items-start gap-3">
                            <div className={`flex-shrink-0 w-12 h-12 rounded-lg flex items-center justify-center text-2xl ${isSelected ? 'bg-primary-100' : 'bg-gray-100'
                                }`}>
                                {getFileIcon(doc.file_type)}
                            </div>

                            <div className="flex-1 min-w-0">
                                <h4 className="font-medium text-gray-900 truncate mb-1">
                                    {doc.filename}
                                </h4>
                                <div className="flex items-center gap-2 text-xs text-gray-500 mb-2">
                                    <span className="px-2 py-1 bg-gray-100 rounded uppercase">
                                        {doc.file_type}
                                    </span>
                                    <span>{formatFileSize(doc.file_size)}</span>
                                </div>
                                {doc.content_preview && (
                                    <p className="text-xs text-gray-600 line-clamp-2 mb-2">
                                        {doc.content_preview}
                                    </p>
                                )}
                                <div className="flex items-center justify-between">
                                    <span className="text-xs text-gray-400">
                                        {new Date(doc.uploaded_at).toLocaleDateString()}
                                    </span>
                                    <button
                                        onClick={(e) => handleDelete(doc.id, e)}
                                        className="text-red-600 hover:text-red-700 text-xs font-medium"
                                    >
                                        Delete
                                    </button>
                                </div>
                            </div>
                        </div>

                        {isSelected && (
                            <div className="mt-3 pt-3 border-t border-primary-200">
                                <p className="text-xs text-primary-700 font-medium flex items-center gap-1">
                                    <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                                    </svg>
                                    Selected for blog generation
                                </p>
                            </div>
                        )}
                    </div>
                );
            })}
        </div>
    );
};

export default DocumentList;
