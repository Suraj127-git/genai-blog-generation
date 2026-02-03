import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from '../hooks/redux';
import { fetchBlogHistory, deleteBlog } from '../features/blogs/blogsSlice';

const HistoryPage: React.FC = () => {
    const dispatch = useAppDispatch();
    const { history, total, page, totalPages, loading } = useAppSelector((state) => state.blogs);
    const [search, setSearch] = useState('');
    const [selectedCategory, setSelectedCategory] = useState('');

    useEffect(() => {
        dispatch(fetchBlogHistory({ page: 1, pageSize: 12, search, topicCategory: selectedCategory }));
    }, [dispatch, search, selectedCategory]);

    const handlePageChange = (newPage: number) => {
        dispatch(fetchBlogHistory({ page: newPage, pageSize: 12, search, topicCategory: selectedCategory }));
    };

    const handleDelete = async (blogId: string) => {
        if (window.confirm('Are you sure you want to delete this blog?')) {
            await dispatch(deleteBlog(blogId));
        }
    };

    return (
        <div className="min-h-screen bg-gray-50">
            <nav className="bg-white shadow-sm">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between h-16 items-center">
                        <Link to="/dashboard" className="text-2xl font-bold text-primary-600">
                            Blog Generation AI
                        </Link>
                        <div className="flex gap-4">
                            <Link to="/dashboard" className="text-gray-700 hover:text-primary-600">Dashboard</Link>
                            <Link to="/generate" className="text-gray-700 hover:text-primary-600">Generate</Link>
                            <Link to="/history" className="text-primary-600 font-medium">History</Link>
                        </div>
                    </div>
                </div>
            </nav>

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                <h2 className="text-3xl font-bold text-gray-900 mb-8">Blog History</h2>

                <div className="mb-6 flex gap-4">
                    <input
                        type="text"
                        placeholder="Search blogs..."
                        className="input flex-1"
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                    />
                    <select
                        className="input w-48"
                        value={selectedCategory}
                        onChange={(e) => setSelectedCategory(e.target.value)}
                    >
                        <option value="">All Categories</option>
                        <option value="technology">Technology</option>
                        <option value="health">Health</option>
                        <option value="finance">Finance</option>
                        <option value="education">Education</option>
                        <option value="science">Science</option>
                    </select>
                </div>

                {loading ? (
                    <div className="text-center py-12">
                        <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
                    </div>
                ) : history.length === 0 ? (
                    <div className="card text-center py-12">
                        <p className="text-gray-500 mb-4">No blogs found</p>
                        <Link to="/generate" className="btn btn-primary">Generate New Blog</Link>
                    </div>
                ) : (
                    <>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                            {history.map((blog) => (
                                <div key={blog.id} className={`card blog-${blog.topic_category}`}>
                                    <Link to={`/blog/${blog.id}`}>
                                        <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2 hover:text-primary-600">
                                            {blog.title}
                                        </h3>
                                    </Link>
                                    <p className="text-sm text-gray-600 mb-3 line-clamp-3">
                                        {blog.content?.substring(0, 150)}...
                                    </p>
                                    <div className="flex items-center justify-between">
                                        <span className="text-xs px-2 py-1 bg-white rounded">{blog.topic_category}</span>
                                        <button
                                            onClick={() => handleDelete(blog.id)}
                                            className="text-red-600 hover:text-red-700 text-sm"
                                        >
                                            Delete
                                        </button>
                                    </div>
                                </div>
                            ))}
                        </div>

                        {totalPages > 1 && (
                            <div className="mt-8 flex justify-center gap-2">
                                {Array.from({ length: totalPages }, (_, i) => i + 1).map((p) => (
                                    <button
                                        key={p}
                                        onClick={() => handlePageChange(p)}
                                        className={`px-4 py-2 rounded ${p === page ? 'bg-primary-600 text-white' : 'bg-white text-gray-700 hover:bg-gray-100'
                                            }`}
                                    >
                                        {p}
                                    </button>
                                ))}
                            </div>
                        )}
                    </>
                )}
            </div>
        </div>
    );
};

export default HistoryPage;
