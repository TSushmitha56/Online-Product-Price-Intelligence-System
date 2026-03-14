import React, { useEffect, useState } from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import api from '../api/axios';
import { Bell, Trash2, Plus, Edit2 } from 'lucide-react';

const PriceAlerts = () => {
    const [alerts, setAlerts] = useState([]);
    const [loading, setLoading] = useState(true);
    
    // Modal states
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [formData, setFormData] = useState({ product_name: '', target_price: '', product_url: '', id: null });
    const [error, setError] = useState('');

    useEffect(() => {
        fetchAlerts();
    }, []);

    const fetchAlerts = async () => {
        setLoading(true);
        try {
            const res = await api.get('/advanced/alerts/');
            setAlerts(res.data.results || res.data);
        } catch (err) {
            console.error("Failed to load alerts", err);
        } finally {
            setLoading(false);
        }
    };

    const handleSaveAlert = async (e) => {
        e.preventDefault();
        setError('');
        try {
            // Strip internal id from payload to avoid serializer issues
            const { id, ...payload } = formData;
            if (id) {
                // Update existing alert
                const res = await api.put(`/advanced/alerts/${id}/`, payload);
                setAlerts(prev => prev.map(a => a.id === id ? res.data : a));
            } else {
                // Create new alert
                const res = await api.post('/advanced/alerts/', payload);
                setAlerts(prev => [res.data, ...prev]);
            }
            closeModal();
        } catch (err) {
            // Robustly extract any validation error message from the API
            const data = err.response?.data;
            let msg = 'Failed to save alert. Please try again.';
            if (data) {
                if (typeof data === 'string') {
                    msg = data;
                } else if (typeof data === 'object') {
                    // Grab the first error message from any field
                    const firstKey = Object.keys(data)[0];
                    const firstVal = data[firstKey];
                    msg = Array.isArray(firstVal) ? firstVal[0] : String(firstVal);
                }
            }
            setError(msg);
        }
    };

    const handleDelete = async (id) => {
        if (!window.confirm("Are you sure you want to delete this alert?")) return;
        try {
            await api.delete(`/advanced/alerts/${id}/`);
            setAlerts(alerts.filter(a => a.id !== id));
        } catch (err) {
            console.error("Failed to delete alert", err);
        }
    };

    const openCreateModal = () => {
        setFormData({ product_name: '', target_price: '', product_url: '', id: null });
        setError('');
        setIsModalOpen(true);
    };

    const openEditModal = (alert) => {
        setFormData({ 
            product_name: alert.product_name, 
            target_price: alert.target_price, 
            product_url: alert.product_url || '', 
            id: alert.id 
        });
        setError('');
        setIsModalOpen(true);
    };

    const closeModal = () => setIsModalOpen(false);

    return (
        <div className="flex flex-col min-h-screen bg-gray-50">
            <Header />
            <main className="flex-grow py-8 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
                <div className="mb-8 border-b border-gray-200 pb-5 sm:flex sm:items-center sm:justify-between">
                    <div>
                        <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:truncate sm:text-3xl sm:tracking-tight flex items-center">
                            <Bell className="w-8 h-8 mr-3 text-blue-600" />
                            Price Alerts
                        </h2>
                        <p className="mt-2 text-sm text-gray-500">
                            We'll email you when prices drop below your target.
                        </p>
                    </div>
                    <div className="mt-4 sm:ml-4 sm:mt-0 flex">
                        <button
                            onClick={openCreateModal}
                            className="inline-flex items-center rounded-md bg-blue-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600 transition"
                        >
                            <Plus className="-ml-0.5 mr-1.5 h-5 w-5" />
                            Create Alert
                        </button>
                    </div>
                </div>

                {loading ? (
                    <div className="flex justify-center py-12"><div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600"></div></div>
                ) : alerts.length === 0 ? (
                    <div className="text-center py-16 bg-white rounded-xl shadow-sm border border-gray-100">
                        <Bell className="mx-auto h-12 w-12 text-gray-300" />
                        <h3 className="mt-2 text-sm font-semibold text-gray-900">No active alerts</h3>
                        <p className="mt-1 text-sm text-gray-500">Create an alert to get notified when a product hits your target price.</p>
                        <div className="mt-6">
                            <button onClick={openCreateModal} className="inline-flex items-center rounded-md bg-blue-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-500">
                                <Plus className="-ml-0.5 mr-1.5 h-5 w-5" />
                                New Alert
                            </button>
                        </div>
                    </div>
                ) : (
                    <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                        <div className="overflow-x-auto">
                            <table className="min-w-full divide-y divide-gray-200">
                                <thead className="bg-gray-50 border-b border-gray-200">
                                    <tr>
                                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Product</th>
                                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Target Price</th>
                                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Current Price</th>
                                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Created</th>
                                        <th scope="col" className="relative px-6 py-3"><span className="sr-only">Actions</span></th>
                                    </tr>
                                </thead>
                                <tbody className="bg-white divide-y divide-gray-200">
                                    {alerts.map((alert) => (
                                        <tr key={alert.id} className="hover:bg-gray-50 transition">
                                            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                                                {alert.product_url ? (
                                                    <a href={alert.product_url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:text-blue-800 hover:underline inline-block w-48 truncate" title={alert.product_name}>
                                                        {alert.product_name}
                                                    </a>
                                                ) : (
                                                    <span className="inline-block w-48 truncate" title={alert.product_name}>{alert.product_name}</span>
                                                )}
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-semibold">
                                                ${parseFloat(alert.target_price || 0).toFixed(2)}
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                                {alert.current_price ? `$${parseFloat(alert.current_price).toFixed(2)}` : <span className="text-xs italic">Pending Check</span>}
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap">
                                                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                                                    alert.status === 'triggered' ? 'bg-green-100 text-green-800' :
                                                    alert.status === 'active' ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'
                                                }`}>
                                                    {alert.status ? alert.status.charAt(0).toUpperCase() + alert.status.slice(1) : 'Unknown'}
                                                </span>
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                                {new Date(alert.created_at).toLocaleDateString()}
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-3">
                                                <button onClick={() => openEditModal(alert)} className="text-indigo-600 hover:text-indigo-900" title="Edit">
                                                    <Edit2 className="w-5 h-5 inline" />
                                                </button>
                                                <button onClick={() => handleDelete(alert.id)} className="text-red-600 hover:text-red-900" title="Delete">
                                                    <Trash2 className="w-5 h-5 inline" />
                                                </button>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                )}
            </main>
            <Footer />

            {/* Create/Edit Modal overlay */}
            {isModalOpen && (
                <div className="fixed inset-0 z-50 flex items-center justify-center p-4" aria-modal="true" role="dialog">
                    {/* Backdrop */}
                    <div className="absolute inset-0 bg-gray-900/60" onClick={closeModal}></div>

                    {/* Modal Panel */}
                    <div className="relative z-10 w-full max-w-lg bg-white rounded-2xl shadow-2xl p-6 sm:p-8">
                        <h3 className="text-xl font-bold text-gray-900 mb-5">
                            {formData.id ? 'Edit Price Alert' : 'Create Price Alert'}
                        </h3>
                        <form onSubmit={handleSaveAlert} className="space-y-5">
                            {error && (
                                <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
                                    <p className="text-sm text-red-700 font-medium">{error}</p>
                                </div>
                            )}
                            <div>
                                <label className="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">
                                    Product Name / Search Term
                                </label>
                                <input
                                    type="text"
                                    required
                                    value={formData.product_name}
                                    onChange={e => setFormData({...formData, product_name: e.target.value})}
                                    className="w-full rounded-xl border border-gray-200 bg-gray-50 px-4 py-3 text-sm text-gray-900 focus:bg-white focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 outline-none transition-all"
                                    placeholder="e.g. Sony WH-1000XM5"
                                />
                            </div>
                            <div>
                                <label className="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">
                                    Target Price ($)
                                </label>
                                <input
                                    type="number"
                                    step="0.01"
                                    min="0"
                                    required
                                    value={formData.target_price}
                                    onChange={e => setFormData({...formData, target_price: e.target.value})}
                                    className="w-full rounded-xl border border-gray-200 bg-gray-50 px-4 py-3 text-sm text-gray-900 focus:bg-white focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 outline-none transition-all"
                                    placeholder="299.99"
                                />
                            </div>
                            <div>
                                <label className="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">
                                    Product URL <span className="text-gray-400 normal-case font-normal">(Optional)</span>
                                </label>
                                <input
                                    type="url"
                                    value={formData.product_url}
                                    onChange={e => setFormData({...formData, product_url: e.target.value})}
                                    className="w-full rounded-xl border border-gray-200 bg-gray-50 px-4 py-3 text-sm text-gray-900 focus:bg-white focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 outline-none transition-all"
                                    placeholder="https://..."
                                />
                            </div>
                            <div className="flex justify-end gap-3 pt-2">
                                <button
                                    type="button"
                                    onClick={closeModal}
                                    className="px-5 py-2.5 rounded-xl border border-gray-200 text-sm font-semibold text-gray-600 hover:bg-gray-50 transition-colors"
                                >
                                    Cancel
                                </button>
                                <button
                                    type="submit"
                                    className="px-6 py-2.5 rounded-xl bg-blue-600 text-sm font-bold text-white hover:bg-blue-700 shadow-md hover:shadow-blue-500/25 transition-all active:scale-95"
                                >
                                    Save Alert
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default PriceAlerts;
