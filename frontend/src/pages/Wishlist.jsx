import React, { useEffect, useState } from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import api from '../api/axios';
import { Trash2, ExternalLink, Heart, Store, ArrowRight, PackageOpen } from 'lucide-react';

// Skeleton loader for a smooth loading experience
const WishlistSkeleton = () => (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[1, 2, 3, 4, 5, 6].map((i) => (
            <div key={i} className="bg-white rounded-3xl border border-gray-100 p-2 animate-pulse">
                <div className="h-56 bg-gray-100 rounded-t-2xl rounded-b-lg mb-4"></div>
                <div className="px-4 pb-4">
                    <div className="h-3 bg-gray-100 rounded-full w-24 mb-4"></div>
                    <div className="h-5 bg-gray-100 rounded-full w-full mb-2"></div>
                    <div className="h-5 bg-gray-100 rounded-full w-2/3 mb-6"></div>
                    <div className="h-8 bg-gray-100 rounded-full w-24 mb-6"></div>
                    <div className="h-12 bg-gray-100 rounded-xl w-full"></div>
                </div>
            </div>
        ))}
    </div>
);

const Wishlist = () => {
    const [wishlist, setWishlist] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchWishlist = async () => {
            try {
                const res = await api.get('/advanced/wishlist/');
                setWishlist(res.data.results || res.data);
            } catch (err) {
                console.error("Failed to load wishlist", err);
            } finally {
                setLoading(false);
            }
        };
        fetchWishlist();
    }, []);

    const handleRemove = async (id) => {
        try {
            await api.delete(`/advanced/wishlist/${id}/`);
            setWishlist(wishlist.filter(item => item.id !== id));
        } catch (err) {
            console.error("Failed to remove item", err);
        }
    };

    return (
        <div className="flex flex-col min-h-screen bg-gray-50/50">
            <Header />

            <main className="flex-grow py-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">

                {/* Page Header */}
                <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-10 pb-6 border-b border-gray-200/60">
                    <div>
                        <h1 className="text-3xl sm:text-4xl font-black text-gray-900 tracking-tight flex items-center gap-3.5">
                            <div className="p-2.5 bg-rose-100 text-rose-600 rounded-2xl shadow-sm border border-rose-200/50">
                                <Heart className="w-7 h-7 fill-rose-600" />
                            </div>
                            My Wishlist
                        </h1>
                        <p className="mt-3 text-sm sm:text-base text-gray-500 font-medium max-w-2xl">
                            Keep track of your favorite products and monitor price drops across different stores.
                        </p>
                    </div>
                    {!loading && (
                        <div className="inline-flex items-center px-4 py-2.5 rounded-xl bg-white border border-gray-200 shadow-sm text-sm font-bold text-gray-700 w-fit">
                            {wishlist.length} {wishlist.length === 1 ? 'Item' : 'Items'} Saved
                        </div>
                    )}
                </div>

                {/* Content Area */}
                {loading ? (
                    <WishlistSkeleton />
                ) : wishlist.length === 0 ? (

                    /* Empty State */
                    <div className="flex flex-col items-center justify-center py-24 bg-white rounded-3xl border border-dashed border-gray-300 shadow-sm">
                        <div className="w-24 h-24 bg-gray-50 rounded-full flex items-center justify-center mb-6 border border-gray-100">
                            <PackageOpen className="w-12 h-12 text-gray-300" />
                        </div>
                        <h3 className="text-2xl font-bold text-gray-900 mb-2">Your wishlist is empty</h3>
                        <p className="text-gray-500 text-center max-w-md mb-8 font-medium">
                            Looks like you haven't saved any deals yet. Start exploring to find and track the best prices!
                        </p>
                        <a
                            href="/"
                            className="inline-flex items-center justify-center px-8 py-3.5 bg-gray-900 text-white text-sm font-bold rounded-xl hover:bg-rose-600 hover:shadow-lg hover:shadow-rose-600/25 transition-all duration-300 active:scale-95"
                        >
                            Explore Deals
                            <ArrowRight className="ml-2 w-4 h-4 text-rose-300" />
                        </a>
                    </div>

                ) : (

                    /* Wishlist Grid */
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        {wishlist.map(item => (
                            <div
                                key={item.id}
                                className="group relative flex flex-col bg-white rounded-3xl border border-gray-100 shadow-[0_4px_20px_-5px_rgba(0,0,0,0.05)] hover:shadow-[0_10px_40px_-10px_rgba(0,0,0,0.08)] transition-all duration-300 ease-[cubic-bezier(0.23,1,0.32,1)] hover:-translate-y-1.5 overflow-hidden"
                            >
                                {/* Image Area */}
                                <div className="relative h-60 w-full p-6 flex items-center justify-center bg-gray-50/80 rounded-t-3xl overflow-hidden">

                                    {/* Floating Delete Button */}
                                    <button
                                        onClick={() => handleRemove(item.id)}
                                        className="absolute top-4 right-4 z-10 p-2.5 rounded-full bg-white/90 backdrop-blur-md border border-gray-100 text-gray-400 hover:text-rose-500 hover:bg-rose-50 hover:border-rose-100 shadow-sm transition-all duration-300 active:scale-90 opacity-100 md:opacity-0 group-hover:opacity-100 focus:opacity-100"
                                        title="Remove from wishlist"
                                    >
                                        <Trash2 className="w-4 h-4" />
                                    </button>

                                    <img
                                        src={item.image_url || 'https://via.placeholder.com/300?text=No+Image'}
                                        alt={item.product_name}
                                        className="relative z-0 max-h-full max-w-full object-contain mix-blend-multiply transition-transform duration-500 group-hover:scale-110"
                                        onError={(e) => { e.target.src = 'https://via.placeholder.com/300?text=No+Image'; }}
                                        loading="lazy"
                                    />
                                </div>

                                {/* Content Area */}
                                <div className="p-6 flex flex-col flex-grow bg-white rounded-b-3xl">

                                    {/* Store Tag */}
                                    <div className="flex items-center mb-3">
                                        <span className="flex items-center gap-1.5 text-xs font-black text-gray-400 uppercase tracking-widest">
                                            <Store className="w-3.5 h-3.5" />
                                            {item.store || 'Unknown Store'}
                                        </span>
                                    </div>

                                    {/* Product Title */}
                                    <h3 className="text-base font-semibold text-gray-900 leading-snug line-clamp-2 mb-4 group-hover:text-rose-600 transition-colors" title={item.product_name}>
                                        {item.product_name}
                                    </h3>

                                    {/* Price */}
                                    <div className="mt-auto mb-6">
                                        <div className="flex items-baseline text-gray-900">
                                            <span className="text-sm font-semibold text-gray-400 mr-1">$</span>
                                            <span className="text-3xl font-black tracking-tight">
                                                {parseFloat(item.price || 0).toFixed(2)}
                                            </span>
                                        </div>
                                    </div>

                                    {/* Action Button */}
                                    <a
                                        href={item.product_url || '#'}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="w-full flex items-center justify-center py-3.5 rounded-2xl text-sm font-bold tracking-wide transition-all duration-300 active:scale-[0.98] bg-gray-900 text-white hover:bg-rose-600 hover:shadow-lg hover:shadow-rose-600/25"
                                    >
                                        View Deal
                                        <ExternalLink className="ml-2 w-4 h-4 text-rose-300" />
                                    </a>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </main>

            <Footer />
        </div>
    );
};

export default Wishlist;