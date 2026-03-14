import React, { useState } from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { useAuth } from '../context/AuthContext';
import api from '../api/axios';
import {
    User as UserIcon,
    LogOut,
    Lock,
    CheckCircle,
    AlertCircle,
    Mail,
    ShieldCheck,
    Save,
    KeyRound
} from 'lucide-react';

const Profile = () => {
    const { user, setUser, logout } = useAuth();

    // Profile Update State
    const [firstName, setFirstName] = useState(user?.first_name || '');
    const [lastName, setLastName] = useState(user?.last_name || '');
    const [profileStatus, setProfileStatus] = useState({ type: '', msg: '' });
    const [isUpdatingProfile, setIsUpdatingProfile] = useState(false);

    // Password Update State
    const [oldPassword, setOldPassword] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [newPassword2, setNewPassword2] = useState('');
    const [pwdStatus, setPwdStatus] = useState({ type: '', msg: '' });
    const [isUpdatingPwd, setIsUpdatingPwd] = useState(false);

    const handleProfileSubmit = async (e) => {
        e.preventDefault();
        setProfileStatus({ type: '', msg: '' });
        setIsUpdatingProfile(true);
        try {
            const res = await api.put('/auth/profile/', { first_name: firstName, last_name: lastName });
            setUser(res.data.user);
            setProfileStatus({ type: 'success', msg: 'Profile updated successfully.' });
        } catch (error) {
            setProfileStatus({ type: 'error', msg: 'Failed to update profile.' });
        } finally {
            setIsUpdatingProfile(false);
            setTimeout(() => setProfileStatus({ type: '', msg: '' }), 5000);
        }
    };

    const handlePasswordSubmit = async (e) => {
        e.preventDefault();
        setPwdStatus({ type: '', msg: '' });

        if (newPassword !== newPassword2) {
            return setPwdStatus({ type: 'error', msg: 'New passwords do not match.' });
        }

        setIsUpdatingPwd(true);
        try {
            await api.post('/auth/change-password/', {
                old_password: oldPassword,
                new_password: newPassword,
                new_password2: newPassword2
            });
            setOldPassword('');
            setNewPassword('');
            setNewPassword2('');
            setPwdStatus({ type: 'success', msg: 'Password changed successfully.' });
        } catch (error) {
            setPwdStatus({ type: 'error', msg: error.response?.data?.error || 'Failed to change password.' });
        } finally {
            setIsUpdatingPwd(false);
            setTimeout(() => setPwdStatus({ type: '', msg: '' }), 5000);
        }
    };

    const StatusMessage = ({ status }) => {
        if (!status.msg) return null;
        return (
            <div className={`mt-6 p-4 rounded-xl flex items-center border ${status.type === 'success'
                    ? 'bg-emerald-50 border-emerald-100 text-emerald-800'
                    : 'bg-rose-50 border-rose-100 text-rose-800'
                }`}>
                {status.type === 'success'
                    ? <CheckCircle className="w-5 h-5 mr-3 flex-shrink-0" />
                    : <AlertCircle className="w-5 h-5 mr-3 flex-shrink-0" />
                }
                <span className="text-sm font-semibold">{status.msg}</span>
            </div>
        );
    };

    // Shared input class for consistency
    const inputClasses = "w-full rounded-xl border border-gray-200 bg-gray-50/50 px-4 py-3 text-sm text-gray-900 focus:bg-white focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 outline-none transition-all duration-200";

    return (
        <div className="flex flex-col min-h-screen bg-[#F8FAFC]">
            <Header />

            <main className="flex-grow py-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full flex justify-center">
                <div className="w-full max-w-3xl space-y-8">

                    {/* --- Profile Header --- */}
                    <div className="bg-white rounded-3xl p-6 sm:p-8 shadow-[0_2px_15px_-3px_rgba(0,0,0,0.04)] border border-gray-100 flex flex-col md:flex-row md:items-center justify-between gap-6">
                        <div className="flex items-center gap-5">
                            <div className="relative">
                                <div className="h-20 w-20 bg-gradient-to-br from-indigo-500 to-violet-600 rounded-full flex justify-center items-center text-white shadow-lg shadow-indigo-200 ring-4 ring-white">
                                    <UserIcon className="h-9 w-9" />
                                </div>
                                {/* Status Dot */}
                                <div className="absolute bottom-1 right-1 h-4 w-4 bg-emerald-400 border-2 border-white rounded-full"></div>
                            </div>
                            <div>
                                <h2 className="text-2xl font-black text-gray-900 tracking-tight">
                                    {user?.first_name} {user?.last_name}
                                </h2>
                                <p className="text-sm font-medium text-gray-500 mt-1 flex items-center gap-1.5">
                                    <Mail className="w-4 h-4 text-gray-400" />
                                    {user?.email}
                                </p>
                            </div>
                        </div>
                        <div className="flex-shrink-0">
                            <button
                                onClick={logout}
                                className="w-full md:w-auto inline-flex items-center justify-center gap-2 rounded-xl bg-rose-50 px-5 py-2.5 text-sm font-bold text-rose-600 hover:bg-rose-100 hover:text-rose-700 transition-colors active:scale-95"
                            >
                                <LogOut className="h-4 w-4" />
                                Sign Out
                            </button>
                        </div>
                    </div>

                    {/* --- Personal Information Card --- */}
                    <div className="bg-white rounded-3xl shadow-[0_2px_15px_-3px_rgba(0,0,0,0.04)] border border-gray-100 overflow-hidden">
                        <div className="px-6 py-5 border-b border-gray-100/80 bg-gray-50/50">
                            <h3 className="text-base font-bold text-gray-900 flex items-center gap-2.5">
                                <ShieldCheck className="w-5 h-5 text-indigo-500" />
                                Personal Information
                            </h3>
                        </div>

                        <div className="p-6 sm:p-8">
                            <form onSubmit={handleProfileSubmit}>
                                <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                                    <div>
                                        <label className="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">First Name</label>
                                        <input
                                            type="text"
                                            value={firstName}
                                            onChange={e => setFirstName(e.target.value)}
                                            className={inputClasses}
                                            placeholder="Enter your first name"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">Last Name</label>
                                        <input
                                            type="text"
                                            value={lastName}
                                            onChange={e => setLastName(e.target.value)}
                                            className={inputClasses}
                                            placeholder="Enter your last name"
                                        />
                                    </div>
                                    <div className="sm:col-span-2">
                                        <label className="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">Email Address</label>
                                        <div className="relative">
                                            <input
                                                type="email"
                                                value={user?.email || ''}
                                                disabled
                                                className="w-full rounded-xl border border-gray-200 bg-gray-100/70 px-4 py-3 pl-11 text-sm text-gray-500 cursor-not-allowed"
                                            />
                                            <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                                        </div>
                                        <p className="mt-2 text-[11px] font-medium text-gray-400">Your email address is used for sign in and cannot be changed here.</p>
                                    </div>
                                </div>

                                <StatusMessage status={profileStatus} />

                                <div className="mt-8 flex justify-end pt-6 border-t border-gray-100">
                                    <button
                                        type="submit"
                                        disabled={isUpdatingProfile}
                                        className="inline-flex items-center justify-center gap-2 rounded-xl bg-indigo-600 px-6 py-3 text-sm font-bold text-white shadow-md hover:bg-indigo-700 hover:shadow-indigo-500/25 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-all active:scale-95 disabled:opacity-70 disabled:cursor-not-allowed"
                                    >
                                        <Save className="w-4 h-4" />
                                        {isUpdatingProfile ? 'Saving...' : 'Save Changes'}
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>

                    {/* --- Change Password Card --- */}
                    <div className="bg-white rounded-3xl shadow-[0_2px_15px_-3px_rgba(0,0,0,0.04)] border border-gray-100 overflow-hidden">
                        <div className="px-6 py-5 border-b border-gray-100/80 bg-gray-50/50">
                            <h3 className="text-base font-bold text-gray-900 flex items-center gap-2.5">
                                <Lock className="w-5 h-5 text-gray-500" />
                                Change Password
                            </h3>
                        </div>

                        <div className="p-6 sm:p-8">
                            <form onSubmit={handlePasswordSubmit}>
                                <div className="grid grid-cols-1 gap-6 max-w-md">
                                    <div>
                                        <label className="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">Current Password</label>
                                        <input
                                            type="password"
                                            required
                                            value={oldPassword}
                                            onChange={e => setOldPassword(e.target.value)}
                                            className={inputClasses}
                                            placeholder="••••••••"
                                        />
                                    </div>
                                    <div className="pt-2">
                                        <label className="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">New Password</label>
                                        <input
                                            type="password"
                                            required
                                            minLength={8}
                                            value={newPassword}
                                            onChange={e => setNewPassword(e.target.value)}
                                            className={inputClasses}
                                            placeholder="••••••••"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">Confirm New Password</label>
                                        <input
                                            type="password"
                                            required
                                            minLength={8}
                                            value={newPassword2}
                                            onChange={e => setNewPassword2(e.target.value)}
                                            className={inputClasses}
                                            placeholder="••••••••"
                                        />
                                    </div>
                                </div>

                                <StatusMessage status={pwdStatus} />

                                <div className="mt-8 flex justify-start pt-6 border-t border-gray-100">
                                    <button
                                        type="submit"
                                        disabled={isUpdatingPwd}
                                        className="inline-flex items-center justify-center gap-2 rounded-xl bg-gray-900 px-6 py-3 text-sm font-bold text-white shadow-md hover:bg-gray-800 hover:shadow-gray-900/25 focus:outline-none focus:ring-2 focus:ring-gray-900 focus:ring-offset-2 transition-all active:scale-95 disabled:opacity-70 disabled:cursor-not-allowed"
                                    >
                                        <KeyRound className="w-4 h-4" />
                                        {isUpdatingPwd ? 'Updating...' : 'Update Password'}
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>

                </div>
            </main>

            <Footer />
        </div>
    );
};

export default Profile;