import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from '../hooks/redux';
import { generateBlog, clearCurrentBlog, clearError } from '../features/blogs/blogsSlice';
import { fetchDocuments, uploadDocument } from '../features/documents/documentsSlice';
import { blogsAPI } from '../api/blogs';

const GenerateBlogPage: React.FC = () => {
    const navigate = useNavigate();
    const dispatch = useAppDispatch();
    const { currentBlog, generating, error } = useAppSelector((state) => state.blogs);
    const { documents, uploading } = useAppSelector((state) => state.documents);

    const [formData, setFormData] = useState({
        topic: '',
        language: 'english',
        model: '',
        document_ids: [] as string[],
    });

    const [uploadedFile, setUploadedFile] = useState<File | null>(null);

    useEffect(() => {
        dispatch(fetchDocuments());
        dispatch(clearCurrentBlog());
        dispatch(clearError());
    }, [dispatch]);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    const handleDocumentSelect = (docId: string) => {
        const isSelected = formData.document_ids.includes(docId);
        if (isSelected) {
            setFormData({
                ...formData,
                document_ids: formData.document_ids.filter(id => id !== docId),
            });
        } else {
            setFormData({
                ...formData,
                document_ids: [...formData.document_ids, docId],
            });
        }
    };

    const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            setUploadedFile(file);
            const result = await dispatch(uploadDocument(file));
            if (uploadDocument.fulfilled.match(result)) {
                // Auto-select the uploaded document
                setFormData({
                    ...formData,
                    document_ids: [...formData.document_ids, result.payload.id],
                });
            }
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        const result = await dispatch(generateBlog(formData));
        if (generateBlog.fulfilled.match(result)) {
            // Blog generated successfully - scroll to view
            window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
        }
    };

    const handleDownload = async (format: 'pdf' | 'docx') => {
        if (!currentBlog) return;

        try {
            const blob = await blogsAPI.downloadBlog(currentBlog.id, format);
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${currentBlog.title}.${format}`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } catch (error) {
            console.error('Download failed:', error);
        }
    };

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Navbar */}
            <nav className="bg-white shadow-sm">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between h-16 items-center">
                        <div className="flex items-center gap-6">
                            <Link to="/dashboard" className="text-2xl font-bold text-primary-600">
                                Blog Generation AI
                            </Link>
                            <div className="flex gap-4">
                                <Link to="/dashboard" className="text-gray-700 hover:text-primary-600">
                                    Dashboard
                                </Link>
                                <Link to="/generate" className="text-primary-600 font-medium">
                                    Generate
                                </Link>
                                <Link to="/history" className="text-gray-700 hover:text-primary-600">
                                    History
                                </Link>
                            </div>
                        </div>
                    </div>
                </div>
            </nav>

            {/* Main Content */}
            <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                <div className="mb-8">
                    <h2 className="text-3xl font-bold text-gray-900 mb-2">Generate New Blog</h2>
                    <p className="text-gray-600">Create AI-powered content from topics or documents</p>
                </div>

                {/* Generation Form */}
                <form onSubmit={handleSubmit} className="card mb-8">
                    {error && (
                        <div className="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded-lg mb-6">
                            {error}
                        </div>
                    )}

                    <div className="space-y-6">
                        <div>
                            <label htmlFor="topic" className="block text-sm font-medium text-gray-700 mb-2">
                                Blog Topic *
                            </label>
                            <textarea
                                id="topic"
                                name="topic"
                                required
                                rows={3}
                                className="input"
                                placeholder="Enter your blog topic or keywords (e.g., 'The Future of Artificial Intelligence')"
                                value={formData.topic}
                                onChange={handleChange}
                            />
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <label htmlFor="language" className="block text-sm font-medium text-gray-700 mb-2">
                                    Language
                                </label>
                                <select
                                    id="language"
                                    name="language"
                                    className="input"
                                    value={formData.language}
                                    onChange={handleChange}
                                >
                                    <option value="english">English</option>
                                    <option value="hindi">Hindi</option>
                                    <option value="french">French</option>
                                    <option value="spanish">Spanish</option>
                                    <option value="german">German</option>
                                </select>
                            </div>

                            <div>
                                <label htmlFor="model" className="block text-sm font-medium text-gray-700 mb-2">
                                    AI Model (Optional)
                                </label>
                                <select
                                    id="model"
                                    name="model"
                                    className="input"
                                    value={formData.model}
                                    onChange={handleChange}
                                >
                                    <option value="">Default (llama-3.3-70b)</option>
                                    <option value="llama-3.3-70b-versatile">Llama 3.3 70B Versatile</option>
                                    <option value="llama-3.1-8b-instant">Llama 3.1 8B Instant</option>
                                </select>
                            </div>
                        </div>

                        {/* Document Upload */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Upload Document (Optional)
                            </label>
                            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-primary-400 transition-colors">
                                <input
                                    type="file"
                                    accept=".pdf,.txt,.docx"
                                    onChange={handleFileUpload}
                                    className="hidden"
                                    id="file-upload"
                                />
                                <label htmlFor="file-upload" className="cursor-pointer">
                                    <div className="flex flex-col items-center">
                                        <svg className="w-12 h-12 text-gray-400 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                                        </svg>
                                        <p className="text-sm text-gray-600">
                                            {uploading ? 'Uploading...' : 'Click to upload or drag and drop'}
                                        </p>
                                        <p className="text-xs text-gray-500 mt-1">PDF, TXT, DOCX (max 10MB)</p>
                                    </div>
                                </label>
                            </div>
                        </div>

                        {/* Document Selection */}
                        {documents.length > 0 && (
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">
                                    Or Select Existing Documents
                                </label>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                                    {documents.slice(0, 6).map((doc) => (
                                        <div
                                            key={doc.id}
                                            onClick={() => handleDocumentSelect(doc.id)}
                                            className={`p-4 rounded-lg border-2 cursor-pointer transition-all ${formData.document_ids.includes(doc.id)
                                                    ? 'border-primary-500 bg-primary-50'
                                                    : 'border-gray-200 hover:border-primary-300'
                                                }`}
                                        >
                                            <div className="flex items-start gap-3">
                                                <div className="flex-shrink-0">
                                                    <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${formData.document_ids.includes(doc.id) ? 'bg-primary-100' : 'bg-gray-100'
                                                        }`}>
                                                        <svg className={`w-5 h-5 ${formData.document_ids.includes(doc.id) ? 'text-primary-600' : 'text-gray-600'
                                                            }`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                                        </svg>
                                                    </div>
                                                </div>
                                                <div className="flex-1 min-w-0">
                                                    <p className="text-sm font-medium text-gray-900 truncate">{doc.filename}</p>
                                                    <p className="text-xs text-gray-500 mt-1">
                                                        {(doc.file_size / 1024).toFixed(1)} KB • {doc.file_type.toUpperCase()}
                                                    </p>
                                                </div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {formData.document_ids.length > 0 && (
                            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                                <p className="text-sm text-blue-800">
                                    <strong>{formData.document_ids.length}</strong> document(s) selected.
                                    The AI will use these as context for blog generation.
                                </p>
                            </div>
                        )}

                        <div>
                            <button
                                type="submit"
                                disabled={generating || !formData.topic}
                                className="w-full btn btn-primary text-lg py-3"
                            >
                                {generating ? (
                                    <span className="flex items-center justify-center gap-2">
                                        <svg className="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                        </svg>
                                        Generating Blog...
                                    </span>
                                ) : (
                                    '✨ Generate Blog with AI'
                                )}
                            </button>
                        </div>
                    </div>
                </form>

                {/* Generated Blog Display */}
                {currentBlog && (
                    <div className={`card blog-${currentBlog.topic_category}`}>
                        <div className="mb-6 flex items-center justify-between">
                            <div>
                                <h3 className="text-2xl font-bold text-gray-900 mb-2">{current Blog.title}</h3>
                                <div className="flex items-center gap-3 text-sm text-gray-600">
                                    <span className="px-2 py-1 bg-white rounded-lg">
                                        {currentBlog.topic_category}
                                    </span>
                                    <span>{currentBlog.language}</span>
                                    {currentBlog.generation_time && (
                                        <span>⚡ {currentBlog.generation_time.toFixed(2)}s</span>
                                    )}
                                </div>
                            </div>
                            <div className="flex gap-2">
                                <button
                                    onClick={() => handleDownload('pdf')}
                                    className="btn btn-secondary"
                                >
                                    📄 PDF
                                </button>
                                <button
                                    onClick={() => handleDownload('docx')}
                                    className="btn btn-secondary"
                                >
                                    📝 DOCX
                                </button>
                            </div>
                        </div>

                        <div className="prose prose-lg max-w-none">
                            {currentBlog.content.split('\n').map((paragraph, index) => (
                                paragraph.trim() && (
                                    <p key={index} className="mb-4">{paragraph}</p>
                                )
                            ))}
                        </div>

                        <div className="mt-8 pt-6 border-t border-gray-200 flex gap-3">
                            <button
                                onClick={() => navigate('/history')}
                                className="btn btn-primary"
                            >
                                View in History
                            </button>
                            <button
                                onClick={() => {
                                    dispatch(clearCurrentBlog());
                                    window.scrollTo({ top: 0, behavior: 'smooth' });
                                }}
                                className="btn btn-secondary"
                            >
                                Generate Another
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default GenerateBlogPage;
