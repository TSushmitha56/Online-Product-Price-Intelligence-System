import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams, Link } from 'react-router-dom';
import api from '../api/axios';
import { KeyRound, AlertCircle, CheckCircle } from 'lucide-react';

const ResetPassword = () => {
    const [searchParams] = useSearchParams();
    const token = searchParams.get('token');
    
    const [password, setPassword] = useState('');
    const [passwordConfirm, setPasswordConfirm] = useState('');
    const [status, setStatus] = useState({ type: '', message: '' });
    const [isSubmitting, setIsSubmitting] = useState(false);
    
    const navigate = useNavigate();

    useEffect(() => {
        if (!token) {
            setStatus({ type: 'error', message: 'Invalid or missing reset token.' });
        }
    }, [token]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setStatus({ type: '', message: '' });
        
        if (password !== passwordConfirm) {
            return setStatus({ type: 'error', message: 'Passwords do not match.' });
        }

        setIsSubmitting(true);

        try {
            const res = await api.post('/auth/reset-password/', { 
                token,
                new_password: password,
                new_password2: passwordConfirm
            });
            setStatus({ type: 'success', message: res.data.message });
            setTimeout(() => navigate('/'), 3000);
        } catch (error) {
            const errorMsg = error.response?.data?.error || error.response?.data?.new_password?.[0] || 'Reset failed.';
            setStatus({ type: 'error', message: errorMsg });
        } finally {
            setIsSubmitting(false);
        }
    };

    if (!token) {
        return (
            <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
                <div className="sm:mx-auto sm:w-full sm:max-w-md bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10 text-center">
                    <div className="text-red-500 mb-4 flex justify-center"><AlertCircle className="h-12 w-12" /></div>
                    <h2 className="text-xl font-bold text-gray-900 mb-4">Invalid Link</h2>
                    <p className="text-gray-600 mb-6">The password reset link is invalid or missing the security token.</p>
                    <Link to="/forgot-password" className="text-blue-600 hover:text-blue-500 font-medium">Request a new link</Link>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
            <div className="sm:mx-auto sm:w-full sm:max-w-md">
                <div className="flex justify-center text-blue-600">
                    <KeyRound className="h-12 w-12" />
                </div>
                <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">Choose a new password</h2>
            </div>

            <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
                <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
                    {status.message && (
                        <div className={`mb-4 border-l-4 p-4 rounded-md ${status.type === 'success' ? 'bg-green-50 border-green-400' : 'bg-red-50 border-red-400'}`}>
                            <div className="flex items-center">
                                <div className="flex-shrink-0">
                                    {status.type === 'success' ? <CheckCircle className="h-5 w-5 text-green-400" /> : <AlertCircle className="h-5 w-5 text-red-400" />}
                                </div>
                                <div className="ml-3">
                                    <p className={`text-sm ${status.type === 'success' ? 'text-green-700' : 'text-red-700'}`}>{status.message}</p>
                                </div>
                            </div>
                        </div>
                    )}

                    <form className="space-y-6" onSubmit={handleSubmit}>
                        <div>
                            <label className="block text-sm font-medium text-gray-700">New Password</label>
                            <div className="mt-1">
                                <input type="password" required value={password} onChange={(e) => setPassword(e.target.value)}
                                    className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm sm:text-sm bg-white" placeholder="••••••••" disabled={isSubmitting || status.type === 'success'} minLength={8} />
                            </div>
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Confirm New Password</label>
                            <div className="mt-1">
                                <input type="password" required value={passwordConfirm} onChange={(e) => setPasswordConfirm(e.target.value)}
                                    className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm sm:text-sm bg-white" placeholder="••••••••" disabled={isSubmitting || status.type === 'success'} minLength={8} />
                            </div>
                        </div>
                        <div>
                            <button
                                type="submit" disabled={isSubmitting || status.type === 'success'}
                                className={`w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white ${isSubmitting || status.type === 'success' ? 'bg-blue-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'} transition-colors`}
                            >
                                {isSubmitting ? 'Resetting...' : 'Reset Password'}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default ResetPassword;
