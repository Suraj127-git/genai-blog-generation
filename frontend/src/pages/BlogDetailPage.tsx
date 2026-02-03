import React, { useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from '../hooks/redux';
import { fetchBlog, deleteBlog } from '../features/blogs/blogsSlice';
import { blogsAPI } from '../api/blogs';

const BlogDetailPage: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const dispatch = useAppDispatch();
    const { currentBlog, loading } = useAppSelector((state) => state.blogs);

    useEffect(() => {
        if (id) {
            dispatch(fetchBlog(id));
        }
    }, [dispatch, id]);

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

    const handleDelete = async () => {
        if (!currentBlog) return;
        if (window.confirm('Are you sure you want to delete this blog?')) {
            await dispatch(deleteBlog(currentBlog.id));
            navigate('/history');
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
            </div>
        );
    }

    if (!currentBlog) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="text-center">
                    <p className="text-gray-600 mb-4">Blog not found</p>
                    <Link to="/history" className="btn btn-primary">Back to History</Link>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50">
            <nav className="bg-white shadow-sm mb-8">
                <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between h-16 items-center">
                        <Link to="/dashboard" className="text-xl font-bold text-primary-600">
                            Blog Generation AI
                        </Link>
                        <Link to="/history" className="text-gray-700 hover:text-primary-600">
                            ← Back to History
                        </Link>
                    </div>
                </div>
            </nav>

            <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 pb-12">
                <div className={`card blog-${currentBlog.topic_category}`}>
                    <div className="mb-6">
                        <div className="flex items-start justify-between mb-4">
                            <div className="flex-1">
                                <h1 className="text-4xl font-bold text-gray-900 mb-4">{currentBlog.title}</h1>
                                <div className="flex items-center gap-3 text-sm text-gray-600">
                                    <span className="px-3 py-1 bg-white rounded-lg font-medium">
                                        {currentBlog.topic_category}
                                    </span>
                                    <span>{currentBlog.language}</span>
                                    <span>{new Date(currentBlog.created_at).toLocaleDateString()}</span>
                                    {currentBlog.generation_time && (
                                        <span>⚡ {currentBlog.generation_time.toFixed(2)}s</span>
                                    )}
                                </div>
                            </div>
                        </div>

                        <div className="flex gap-2 mb-6">
                            <button onClick={() => handleDownload('pdf')} className="btn btn-primary">
                                📄 Download PDF
                            </button>
                            <button onClick={() => handleDownload('docx')} className="btn btn-secondary">
                                📝 Download DOCX
                            </button>
                            <button onClick={handleDelete} className="btn btn-danger ml-auto">
                                🗑️ Delete
                            </button>
                        </div>
                    </div>

                    <div className="prose prose-lg max-w-none">
                        {currentBlog.content.split('\n').map((paragraph, index) => (
                            paragraph.trim() && (
                                paragraph.startsWith('# ') ? (
                                    <h1 key={index}>{paragraph.substring(2)}</h1>
                                ) : paragraph.startsWith('## ') ? (
                                    <h2 key={index}>{paragraph.substring(3)}</h2>
                                ) : paragraph.startsWith('### ') ? (
                                    <h3 key={index}>{paragraph.substring(4)}</h3>
                                ) : (
                                    <p key={index}>{paragraph}</p>
                                )
                            )
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default BlogDetailPage;
