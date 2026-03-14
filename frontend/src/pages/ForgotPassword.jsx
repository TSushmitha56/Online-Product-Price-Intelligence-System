import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../api/axios';
import { Mail, AlertCircle, CheckCircle } from 'lucide-react';

const ForgotPassword = () => {
    const [email, setEmail] = useState('');
    const [status, setStatus] = useState({ type: '', message: '' });
    const [isSubmitting, setIsSubmitting] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setStatus({ type: '', message: '' });
        setIsSubmitting(true);

        try {
            const res = await api.post('/auth/forgot-password/', { email });
            setStatus({ type: 'success', message: res.data.message });
        } catch (error) {
            setStatus({ 
                type: 'error', 
                message: error.response?.data?.email?.[0] || 'An error occurred. Please try again.' 
            });
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
            <div className="sm:mx-auto sm:w-full sm:max-w-md">
                <div className="flex justify-center text-blue-600">
                    <Mail className="h-12 w-12" />
                </div>
                <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
                    Reset your password
                </h2>
                <p className="mt-2 text-center text-sm text-gray-600">
                    Enter your email to receive a reset link
                </p>
            </div>

            <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
                <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
                    {status.message && (
                        <div className={`mb-4 border-l-4 p-4 rounded-md ${status.type === 'success' ? 'bg-green-50 border-green-400' : 'bg-red-50 border-red-400'}`}>
                            <div className="flex items-center">
                                <div className="flex-shrink-0">
                                    {status.type === 'success' ? (
                                        <CheckCircle className="h-5 w-5 text-green-400" />
                                    ) : (
                                        <AlertCircle className="h-5 w-5 text-red-400" />
                                    )}
                                </div>
                                <div className="ml-3">
                                    <p className={`text-sm ${status.type === 'success' ? 'text-green-700' : 'text-red-700'}`}>
                                        {status.message}
                                    </p>
                                </div>
                            </div>
                        </div>
                    )}

                    <form className="space-y-6" onSubmit={handleSubmit}>
                        <div>
                            <label htmlFor="email" className="block text-sm font-medium text-gray-700">Email address</label>
                            <div className="mt-1">
                                <input id="email" type="email" required value={email} onChange={(e) => setEmail(e.target.value)}
                                    className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm text-gray-700 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm bg-white" placeholder="your-email@example.com" disabled={isSubmitting || status.type === 'success'} />
                            </div>
                        </div>

                        <div>
                            <button
                                type="submit" disabled={isSubmitting || status.type === 'success'}
                                className={`w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white ${isSubmitting || status.type === 'success' ? 'bg-blue-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'} focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors`}
                            >
                                {isSubmitting ? 'Sending...' : 'Send reset link'}
                            </button>
                        </div>
                    </form>

                    <div className="mt-6 text-center">
                        <Link to="/" className="font-medium text-gray-600 hover:text-gray-500 text-sm flex items-center justify-center">
                            Return to sign in
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ForgotPassword;
