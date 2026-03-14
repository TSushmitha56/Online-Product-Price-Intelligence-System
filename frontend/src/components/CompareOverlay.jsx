import React, { useState, useEffect } from 'react';
import { X } from 'lucide-react';
import ComparisonTable from './results/ComparisonTable';
import { getCompareBasket } from './ComparisonBasket';

const CompareOverlay = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [basket, setBasket] = useState([]);

    useEffect(() => {
        const handleOpen = () => {
            setBasket(getCompareBasket());
            setIsOpen(true);
            document.body.style.overflow = 'hidden'; // Prevent background scrolling
        };
        
        window.addEventListener('openCompareOverlay', handleOpen);
        return () => window.removeEventListener('openCompareOverlay', handleOpen);
    }, []);

    const handleClose = () => {
        setIsOpen(false);
        document.body.style.overflow = 'auto'; // Restore scrolling
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 sm:p-6 lg:p-8 animate-fade-in">
            {/* Backdrop */}
            <div 
                className="absolute inset-0 bg-gray-900/40 backdrop-blur-sm transition-opacity"
                onClick={handleClose}
            ></div>

            {/* Modal Container */}
            <div className="relative bg-gray-50 rounded-3xl shadow-2xl w-full max-w-7xl max-h-full flex flex-col overflow-hidden animate-scale-up">
                
                {/* Header */}
                <div className="px-6 py-5 bg-white border-b border-gray-100 flex justify-between items-center z-10">
                    <div>
                        <h2 className="text-xl font-extrabold text-gray-900">Compare Products</h2>
                        <p className="text-sm text-gray-500 mt-0.5">Side-by-side spec comparison of your selected items.</p>
                    </div>
                    <button 
                        onClick={handleClose}
                        className="p-2 rounded-full text-gray-400 hover:text-gray-600 hover:bg-gray-100 transition-colors"
                        title="Close Compare"
                    >
                        <X className="w-6 h-6" />
                    </button>
                </div>

                {/* Content - The Table */}
                <div className="overflow-y-auto p-6 flex-grow scrollbar-thin scrollbar-thumb-gray-200">
                    <ComparisonTable offers={basket} />
                </div>
            </div>
        </div>
    );
};

export default CompareOverlay;
