import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from '../../hooks/redux';
import { logout } from '../../features/auth/authSlice';

const Navbar: React.FC = () => {
    const navigate = useNavigate();
    const dispatch = useAppDispatch();
    const { user } = useAppSelector((state) => state.auth);

    const handleLogout = () => {
        dispatch(logout());
        navigate('/login');
    };

    return (
        <nav className="bg-white shadow-sm sticky top-0 z-50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between h-16 items-center">
                    <div className="flex items-center gap-8">
                        <Link to="/dashboard" className="text-2xl font-bold text-primary-600 hover:text-primary-700 transition-colors">
                            Blog Generation AI
                        </Link>
                        <div className="hidden md:flex gap-6">
                            <Link
                                to="/dashboard"
                                className="text-gray-700 hover:text-primary-600 font-medium transition-colors"
                            >
                                Dashboard
                            </Link>
                            <Link
                                to="/generate"
                                className="text-gray-700 hover:text-primary-600 font-medium transition-colors"
                            >
                                Generate
                            </Link>
                            <Link
                                to="/history"
                                className="text-gray-700 hover:text-primary-600 font-medium transition-colors"
                            >
                                History
                            </Link>
                        </div>
                    </div>

                    <div className="flex items-center gap-4">
                        <div className="hidden sm:flex items-center gap-3">
                            <div className="text-right">
                                <p className="text-sm font-medium text-gray-900">{user?.full_name || user?.username}</p>
                                <p className="text-xs text-gray-500">{user?.email}</p>
                            </div>
                            <div className="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
                                <span className="text-primary-700 font-semibold text-sm">
                                    {user?.username?.charAt(0).toUpperCase()}
                                </span>
                            </div>
                        </div>
                        <button
                            onClick={handleLogout}
                            className="btn btn-secondary text-sm"
                        >
                            Logout
                        </button>
                    </div>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
