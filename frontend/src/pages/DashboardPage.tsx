import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAppSelector, useAppDispatch } from '../hooks/redux';
import { fetchBlogHistory } from '../features/blogs/blogsSlice';
import { logout } from '../features/auth/authSlice';

const DashboardPage: React.FC = () => {
    const dispatch = useAppDispatch();
    const { user } = useAppSelector((state) => state.auth);
    const { history, total, loading } = useAppSelector((state) => state.blogs);

    useEffect(() => {
        dispatch(fetchBlogHistory({ page: 1, pageSize: 5 }));
    }, [dispatch]);

    const handleLogout = () => {
        dispatch(logout());
    };

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Navbar */}
            <nav className="bg-white shadow-sm">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between h-16 items-center">
                        <div className="flex items-center">
                            <h1 className="text-2xl font-bold text-primary-600">Blog Generation AI</h1>
                        </div>
                        <div className="flex items-center gap-4">
                            <Link to="/generate" className="text-gray-700 hover:text-primary-600">
                                Generate
                            </Link>
                            <Link to="/history" className="text-gray-700 hover:text-primary-600">
                                History
                            </Link>
                            <div className="flex items-center gap-3">
                                <span className="text-sm text-gray-700">{user?.username}</span>
                                <button
                                    onClick={handleLogout}
                                    className="btn btn-secondary text-sm"
                                >
                                    Logout
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </nav>

            {/* Main Content */}
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                {/* Welcome Section */}
                <div className="mb-12">
                    <h2 className="text-4xl font-bold text-gray-900 mb-2">
                        Welcome back, {user?.full_name || user?.username}! 👋
                    </h2>
                    <p className="text-lg text-gray-600">
                        Ready to create amazing content with AI?
                    </p>
                </div>

                {/* Stats Cards */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
                    <div className="card bg-gradient-to-br from-blue-50 to-indigo-50">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm font-medium text-gray-600">Total Blogs</p>
                                <p className="text-3xl font-bold text-gray-900 mt-1">{total}</p>
                            </div>
                            <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center">
                                <svg className="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                </svg>
                            </div>
                        </div>
                    </div>

                    <div className="card bg-gradient-to-br from-green-50 to-emerald-50">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm font-medium text-gray-600">Recent Blogs</p>
                                <p className="text-3xl font-bold text-gray-900 mt-1">{history.length}</p>
                            </div>
                            <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
                                <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                            </div>
                        </div>
                    </div>

                    <div className="card bg-gradient-to-br from-purple-50 to-pink-50">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm font-medium text-gray-600">AI Powered</p>
                                <p className="text-xl font-bold text-gray-900 mt-1">GroqAI</p>
                            </div>
                            <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center">
                                <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                                </svg>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Quick Actions */}
                <div className="mb-12">
                    <h3 className="text-2xl font-bold text-gray-900 mb-6">Quick Actions</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <Link
                            to="/generate"
                            className="card hover:shadow-lg transition-shadow cursor-pointer group"
                        >
                            <div className="flex items-center gap-4">
                                <div className="w-16 h-16 bg-primary-100 rounded-lg flex items-center justify-center group-hover:bg-primary-200 transition-colors">
                                    <svg className="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                                    </svg>
                                </div>
                                <div>
                                    <h4 className="text-lg font-semibold text-gray-900">Generate New Blog</h4>
                                    <p className="text-sm text-gray-600">Create AI-powered content instantly</p>
                                </div>
                            </div>
                        </Link>

                        <Link
                            to="/history"
                            className="card hover:shadow-lg transition-shadow cursor-pointer group"
                        >
                            <div className="flex items-center gap-4">
                                <div className="w-16 h-16 bg-indigo-100 rounded-lg flex items-center justify-center group-hover:bg-indigo-200 transition-colors">
                                    <svg className="w-8 h-8 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                </div>
                                <div>
                                    <h4 className="text-lg font-semibold text-gray-900">View History</h4>
                                    <p className="text-sm text-gray-600">Browse your generated blogs</p>
                                </div>
                            </div>
                        </Link>
                    </div>
                </div>

                {/* Recent Blogs */}
                <div>
                    <div className="flex justify-between items-center mb-6">
                        <h3 className="text-2xl font-bold text-gray-900">Recent Blogs</h3>
                        <Link to="/history" className="text-primary-600 hover:text-primary-700 font-medium">
                            View All →
                        </Link>
                    </div>

                    {loading ? (
                        <div className="text-center py-12">
                            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
                        </div>
                    ) : history.length === 0 ? (
                        <div className="card text-center py-12">
                            <p className="text-gray-500 mb-4">No blogs yet. Start creating!</p>
                            <Link to="/generate" className="btn btn-primary">
                                Generate Your First Blog
                            </Link>
                        </div>
                    ) : (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                            {history.slice(0, 6).map((blog) => (
                                <Link
                                    key={blog.id}
                                    to={`/blog/${blog.id}`}
                                    className={`card hover:shadow-lg transition-shadow cursor-pointer blog-${blog.topic_category}`}
                                >
                                    <h4 className="font-semibold text-gray-900 mb-2 line-clamp-2">
                                        {blog.title}
                                    </h4>
                                    <p className="text-sm text-gray-600 mb-3 line-clamp-3">
                                        {blog.content?.substring(0, 100)}...
                                    </p>
                                    <div className="flex items-center justify-between text-xs text-gray-500">
                                        <span className="px-2 py-1 bg-gray-100 rounded">
                                            {blog.topic_category}
                                        </span>
                                        <span>{new Date(blog.created_at).toLocaleDateString()}</span>
                                    </div>
                                </Link>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default DashboardPage;
