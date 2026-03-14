import React, { useEffect, useState } from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import api from '../api/axios';
import { useAuth } from '../context/AuthContext';
import {
    ShoppingBag, Bell, History, Sparkles, ExternalLink,
    Search, User, Clock, Trash2, ChevronRight, Package
} from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';

// Skeleton Loader for smooth transitions
const DashboardSkeleton = () => (
    <div className="space-y-8 animate-pulse">
        <div className="flex justify-between items-end mb-8">
            <div className="space-y-3">
                <div className="h-8 bg-gray-200 rounded w-64"></div>
                <div className="h-4 bg-gray-200 rounded w-96"></div>
            </div>
            <div className="flex space-x-3">
                <div className="h-10 bg-gray-200 rounded-lg w-32"></div>
                <div className="h-10 bg-gray-200 rounded-lg w-32"></div>
            </div>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-10">
            {[1, 2, 3].map(i => (
                <div key={i} className="bg-white p-6 rounded-2xl h-32 border border-gray-100"></div>
            ))}
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2 h-96 bg-white rounded-2xl border border-gray-100"></div>
            <div className="h-96 bg-white rounded-2xl border border-gray-100"></div>
        </div>
    </div>
);

const Dashboard = () => {
    const { user } = useAuth();
    const navigate = useNavigate();

    const [wishlist, setWishlist] = useState([]);
    const [alerts, setAlerts] = useState([]);
    const [history, setHistory] = useState([]);
    const [recs, setRecs] = useState([]);
    const [loading, setLoading] = useState(true);
    const [recsLoading, setRecsLoading] = useState(true);

    useEffect(() => {
        const fetchDashboardData = async () => {
            try {
                const [wishRes, alertRes, histRes] = await Promise.all([
                    api.get('/advanced/wishlist/'),
                    api.get('/advanced/alerts/'),
                    api.get('/advanced/search-history/')
                ]);

                setWishlist(wishRes.data.results || wishRes.data || []);
                setAlerts(alertRes.data.results || alertRes.data || []);
                setHistory(histRes.data.results || histRes.data || []);
            } catch (err) {
                console.error("Dashboard data fetch failed", err);
            } finally {
                setLoading(false);
            }
        };

        const fetchRecommendations = async () => {
            try {
                setRecsLoading(true);
                const recRes = await api.get('/advanced/recommendations/');
                setRecs(recRes.data.recommendations || []);
            } catch (err) {
                console.error("Recommendation fetch failed", err);
            } finally {
                setRecsLoading(false);
            }
        };

        fetchDashboardData();
        fetchRecommendations();
    }, []);

    const statCards = [
        { title: 'Saved Products', value: wishlist.length, icon: ShoppingBag, color: 'text-indigo-600', bg: 'bg-indigo-50', border: 'border-indigo-100', link: '/wishlist' },
        { title: 'Active Alerts', value: alerts.filter(a => a.status === 'active').length, icon: Bell, color: 'text-rose-600', bg: 'bg-rose-50', border: 'border-rose-100', link: '/alerts' },
        { title: 'Recent Searches', value: history.length, icon: History, color: 'text-emerald-600', bg: 'bg-emerald-50', border: 'border-emerald-100', link: '#' },
    ];

    return (
        <div className="flex flex-col min-h-screen bg-[#F8FAFC]">
            <Header />

            <main className="flex-grow py-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
                {loading ? (
                    <DashboardSkeleton />
                ) : (
                    <>
                        {/* --- Header Section --- */}
                        <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-10">
                            <div>
                                <h2 className="text-3xl font-black text-gray-900 tracking-tight flex items-center gap-3">
                                    Welcome back, {user?.first_name || 'User'} 👋
                                </h2>
                                <p className="mt-2 text-gray-500 font-medium text-sm sm:text-base">
                                    Here's an overview of your tracked products and recent activity.
                                </p>
                            </div>
                            <div className="flex items-center gap-3">
                                <button
                                    onClick={() => navigate('/profile')}
                                    className="inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl bg-white text-sm font-bold text-gray-700 border border-gray-200 shadow-sm hover:bg-gray-50 hover:text-gray-900 transition-all active:scale-95"
                                >
                                    <User className="w-4 h-4" />
                                    Profile
                                </button>
                                <button
                                    onClick={() => navigate('/upload')}
                                    className="inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl bg-gray-900 text-sm font-bold text-white shadow-md hover:bg-indigo-600 hover:shadow-indigo-500/25 transition-all duration-300 active:scale-95"
                                >
                                    <Search className="w-4 h-4" />
                                    New Search
                                </button>
                            </div>
                        </div>

                        {/* --- Stats Grid --- */}
                        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-10">
                            {statCards.map((item) => (
                                <Link
                                    to={item.link}
                                    key={item.title}
                                    className="group relative bg-white rounded-3xl p-6 shadow-[0_2px_15px_-3px_rgba(0,0,0,0.04)] border border-gray-100 hover:shadow-[0_8px_30px_rgb(0,0,0,0.08)] transition-all duration-300 hover:-translate-y-1 flex flex-col justify-between"
                                >
                                    <div className="flex justify-between items-start mb-4">
                                        <div className={`p-3.5 rounded-2xl ${item.bg} border ${item.border}`}>
                                            <item.icon className={`h-6 w-6 ${item.color}`} strokeWidth={2.5} />
                                        </div>
                                        {item.link !== '#' && (
                                            <div className="w-8 h-8 rounded-full bg-gray-50 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                                                <ChevronRight className="w-4 h-4 text-gray-400" />
                                            </div>
                                        )}
                                    </div>
                                    <div>
                                        <p className="text-3xl font-black text-gray-900 mb-1">{item.value}</p>
                                        <p className="text-sm font-semibold text-gray-500">{item.title}</p>
                                    </div>
                                </Link>
                            ))}
                        </div>

                        {/* --- Main Dashboard Content --- */}
                        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

                            {/* Left Column: Recommendations */}
                            <div className="lg:col-span-2 flex flex-col">
                                <div className="bg-white rounded-3xl shadow-[0_2px_15px_-3px_rgba(0,0,0,0.04)] border border-gray-100 overflow-hidden flex-grow flex flex-col">
                                    <div className="px-6 py-5 border-b border-gray-100/80 bg-gray-50/50 flex items-center justify-between">
                                        <h3 className="text-base font-bold text-gray-900 flex items-center gap-2.5">
                                            <Sparkles className="h-5 w-5 text-amber-400 fill-amber-400" />
                                            Recommended For You
                                        </h3>
                                    </div>

                                    <div className="p-6 flex-grow flex flex-col">
                                        {recsLoading ? (
                                            <div className="flex flex-col justify-center items-center h-full py-12">
                                                <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-indigo-600 mb-4"></div>
                                                <span className="text-sm text-gray-500 font-medium">Curating your personalized deals...</span>
                                            </div>
                                        ) : recs.length === 0 ? (
                                            <div className="flex flex-col justify-center items-center h-full py-12 text-center">
                                                <Package className="h-12 w-12 text-gray-300 mb-3" />
                                                <h4 className="text-gray-900 font-semibold">No recommendations yet</h4>
                                                <p className="text-sm text-gray-500 max-w-xs mt-1">Perform a few searches to help us understand what you're looking for.</p>
                                            </div>
                                        ) : (
                                            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                                                {recs.slice(0, 4).map((rec, idx) => (
                                                    <div
                                                        key={idx}
                                                        onClick={() => window.open(rec.product_url, '_blank')}
                                                        className="group flex items-center p-3.5 bg-white border border-gray-100 rounded-2xl hover:border-indigo-100 hover:bg-indigo-50/30 hover:shadow-md transition-all cursor-pointer"
                                                    >
                                                        <div className="flex-shrink-0 h-20 w-20 bg-gray-50 rounded-xl flex items-center justify-center p-2 overflow-hidden mr-4">
                                                            <img
                                                                src={rec.image_url || 'https://via.placeholder.com/80?text=No+Image'}
                                                                alt={rec.product_name}
                                                                className="object-contain max-h-full mix-blend-multiply group-hover:scale-110 transition-transform duration-500"
                                                                loading="lazy"
                                                            />
                                                        </div>
                                                        <div className="flex-1 min-w-0 pr-2">
                                                            <p className="text-xs font-bold text-indigo-600 uppercase tracking-wider mb-1">
                                                                {rec.store || 'Store'}
                                                            </p>
                                                            <h4 className="text-sm font-semibold text-gray-900 truncate mb-1" title={rec.product_name}>
                                                                {rec.product_name}
                                                            </h4>
                                                            <div className="flex items-center justify-between">
                                                                <p className="text-lg font-black text-gray-900">
                                                                    ${parseFloat(rec.price).toFixed(2)}
                                                                </p>
                                                                <ExternalLink className="w-4 h-4 text-gray-300 group-hover:text-indigo-600 transition-colors" />
                                                            </div>
                                                        </div>
                                                    </div>
                                                ))}
                                            </div>
                                        )}
                                    </div>
                                </div>
                            </div>

                            {/* Right Column: Search History */}
                            <div className="flex flex-col">
                                <div className="bg-white rounded-3xl shadow-[0_2px_15px_-3px_rgba(0,0,0,0.04)] border border-gray-100 overflow-hidden flex-grow flex flex-col">
                                    <div className="px-6 py-5 border-b border-gray-100/80 bg-gray-50/50 flex items-center justify-between">
                                        <h3 className="text-base font-bold text-gray-900 flex items-center gap-2.5">
                                            <History className="h-5 w-5 text-gray-400" />
                                            Recent Searches
                                        </h3>
                                        {history.length > 0 && (
                                            <button
                                                onClick={async () => {
                                                    if (window.confirm('Clear all search history?')) {
                                                        await api.delete('/advanced/search-history/');
                                                        setHistory([]);
                                                    }
                                                }}
                                                className="p-1.5 text-gray-400 hover:text-rose-500 hover:bg-rose-50 rounded-md transition-colors"
                                                title="Clear History"
                                            >
                                                <Trash2 className="w-4 h-4" />
                                            </button>
                                        )}
                                    </div>

                                    <div className="p-6 flex-grow flex flex-col">
                                        {history.length === 0 ? (
                                            <div className="flex flex-col items-center justify-center flex-grow py-8 text-center">
                                                <Search className="h-10 w-10 text-gray-200 mb-3" />
                                                <p className="text-sm text-gray-500 font-medium">Your search history is empty.</p>
                                            </div>
                                        ) : (
                                            <ul className="space-y-4">
                                                {history.slice(0, 6).map(item => (
                                                    <li key={item.id} className="group flex items-start gap-3">
                                                        <div className="mt-0.5 p-1.5 rounded-full bg-gray-50 text-gray-400 group-hover:bg-indigo-50 group-hover:text-indigo-500 transition-colors">
                                                            <Clock className="w-3.5 h-3.5" />
                                                        </div>
                                                        <div className="flex-1 min-w-0">
                                                            <p className="text-sm font-semibold text-gray-800 truncate">
                                                                {item.query}
                                                            </p>
                                                            <p className="text-[11px] font-medium text-gray-400 mt-0.5">
                                                                {new Date(item.timestamp).toLocaleDateString(undefined, {
                                                                    month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
                                                                })}
                                                            </p>
                                                        </div>
                                                    </li>
                                                ))}
                                            </ul>
                                        )}
                                        {history.length > 6 && (
                                            <div className="mt-auto pt-6 w-full">
                                                <button className="w-full py-2.5 bg-gray-50 hover:bg-gray-100 text-xs font-bold text-gray-600 rounded-xl transition-colors">
                                                    View All History ({history.length})
                                                </button>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            </div>

                        </div>
                    </>
                )}
            </main>

            <Footer />
        </div>
    );
};

export default Dashboard;