import React, { useState, useEffect } from 'react';
import { Layers, X, Trash2, ArrowRight, Scale, Plus } from 'lucide-react';

// Utility to manage comparison basket in localStorage
export const addToCompareBasket = (product) => {
    let basket = JSON.parse(localStorage.getItem('compareBasket') || '[]');
    // Prevent duplicates
    if (!basket.find(p => p.product_url === product.product_url && p.store === product.store)) {
        if (basket.length >= 4) {
            basket.shift(); // keep max 4 items
        }
        basket.push(product);
        localStorage.setItem('compareBasket', JSON.stringify(basket));
        window.dispatchEvent(new Event('compareBasketUpdated'));
        return true;
    }
    return false;
};

export const getCompareBasket = () => {
    return JSON.parse(localStorage.getItem('compareBasket') || '[]');
};

export const removeFromCompareBasket = (url, store) => {
    let basket = JSON.parse(localStorage.getItem('compareBasket') || '[]');
    basket = basket.filter(p => p.product_url !== url || p.store !== store);
    localStorage.setItem('compareBasket', JSON.stringify(basket));
    window.dispatchEvent(new Event('compareBasketUpdated'));
};

const ComparisonBasket = () => {
    const [basket, setBasket] = useState(getCompareBasket());
    const [isOpen, setIsOpen] = useState(false);

    useEffect(() => {
        const handleUpdate = () => setBasket(getCompareBasket());
        window.addEventListener('compareBasketUpdated', handleUpdate);
        return () => window.removeEventListener('compareBasketUpdated', handleUpdate);
    }, []);

    if (basket.length === 0) return null;

    return (
        <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end">

            {/* Floating Panel */}
            <div
                className={`
                    mb-4 w-80 md:w-96 bg-white rounded-2xl shadow-[0_8px_30px_rgb(0,0,0,0.12)] border border-gray-100 overflow-hidden
                    transform origin-bottom-right transition-all duration-300 ease-[cubic-bezier(0.23,1,0.32,1)]
                    ${isOpen ? 'scale-100 opacity-100 translate-y-0' : 'scale-95 opacity-0 translate-y-4 pointer-events-none'}
                `}
            >
                {/* Header */}
                <div className="px-5 py-4 bg-gray-50/80 backdrop-blur-sm border-b border-gray-100 flex justify-between items-center">
                    <div className="flex items-center gap-2">
                        <Scale className="w-4 h-4 text-blue-600" />
                        <h4 className="font-semibold text-gray-900 text-sm tracking-wide">Compare Products</h4>
                    </div>
                    <button
                        onClick={() => {
                            localStorage.removeItem('compareBasket');
                            setBasket([]);
                            setIsOpen(false);
                        }}
                        className="flex items-center gap-1 text-xs text-gray-400 hover:text-red-500 font-medium transition-colors px-2 py-1 rounded-md hover:bg-red-50"
                    >
                        <Trash2 className="w-3.5 h-3.5" />
                        Clear All
                    </button>
                </div>

                {/* Body / Items List */}
                <div className="max-h-[60vh] overflow-y-auto p-2 scrollbar-thin scrollbar-thumb-gray-200">
                    {basket.map((item, idx) => (
                        <div key={idx} className="group relative flex items-center p-3 mb-1 bg-white hover:bg-gray-50 rounded-xl transition-colors">

                            {/* Product Image */}
                            <div className="w-14 h-14 flex-shrink-0 bg-white border border-gray-100 shadow-sm rounded-lg mr-4 flex items-center justify-center p-1.5 overflow-hidden">
                                <img
                                    src={item.image_url || 'https://via.placeholder.com/150?text=No+Image'}
                                    alt={item.product_name || 'product'}
                                    className="max-h-full max-w-full object-contain hover:scale-105 transition-transform duration-300"
                                />
                            </div>

                            {/* Product Info */}
                            <div className="flex-1 min-w-0 pr-8">
                                <h5 className="text-sm font-semibold text-gray-800 truncate" title={item.product_name || item.name || 'Product'}>
                                    {item.product_name || item.name || item.title || 'Product'}
                                </h5>
                                <div className="text-xs mt-1.5 flex items-center justify-between">
                                    <span className="text-gray-500 font-medium px-2 py-0.5 bg-gray-100 rounded-md">
                                        {item.store || item.platform}
                                    </span>
                                    <span className="font-bold text-gray-900 tracking-tight">
                                        ${parseFloat(item.price || item.final_price || 0).toFixed(2)}
                                    </span>
                                </div>
                            </div>

                            {/* Remove Button (Appears on hover) */}
                            <button
                                onClick={() => removeFromCompareBasket(item.product_url, item.store || item.platform)}
                                className="absolute right-3 top-1/2 -translate-y-1/2 p-1.5 bg-white border border-gray-100 text-gray-400 hover:text-red-500 hover:bg-red-50 hover:border-red-100 rounded-full shadow-sm opacity-0 group-hover:opacity-100 focus:opacity-100 transition-all"
                                aria-label="Remove item"
                            >
                                <X className="w-4 h-4" />
                            </button>
                        </div>
                    ))}
                </div>

                {/* Footer / Call to Action */}
                <div className="p-4 bg-white border-t border-gray-100">
                    {basket.length > 1 ? (
                        <a
                            href="/compare-view"
                            onClick={(e) => {
                                e.preventDefault();
                                window.dispatchEvent(new Event('openCompareOverlay'));
                            }}
                            className="flex items-center justify-center w-full gap-2 bg-gray-900 hover:bg-blue-600 text-white py-3 rounded-xl text-sm font-semibold shadow-md hover:shadow-lg hover:shadow-blue-600/20 transition-all duration-200 active:scale-[0.98]"
                        >
                            Compare Details
                            <ArrowRight className="w-4 h-4" />
                        </a>
                    ) : (
                        <div className="flex items-center justify-center w-full gap-2 py-3 rounded-xl border border-dashed border-gray-300 bg-gray-50 text-gray-500 text-sm font-medium">
                            <Plus className="w-4 h-4" />
                            Add another item to compare
                        </div>
                    )}
                </div>
            </div>

            {/* Floating Action Button (Toggle) */}
            <button
                onClick={() => setIsOpen(!isOpen)}
                className={`
                    flex items-center gap-2 px-5 py-3.5 rounded-full shadow-xl font-semibold text-sm transition-all duration-300 active:scale-95
                    ${isOpen
                        ? 'bg-white text-gray-900 hover:bg-gray-50'
                        : 'bg-gray-900 text-white hover:bg-gray-800 hover:-translate-y-1'}
                `}
            >
                <Layers className="w-5 h-5" />
                <span>Compare</span>
                <span className={`
                    flex items-center justify-center w-5 h-5 rounded-full text-xs
                    ${isOpen ? 'bg-gray-100 text-gray-900' : 'bg-blue-600 text-white'}
                `}>
                    {basket.length}
                </span>
            </button>
        </div>
    );
};

export default ComparisonBasket;