import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import ResultsDisplay from '../components/results/ResultsDisplay';
import { ArrowLeft } from 'lucide-react';
import PriceTrendChart from '../components/PriceTrendChart';
import SocialShare from '../components/SocialShare';
import { useAuth } from '../context/AuthContext';
import api from '../api/axios';

const Compare = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const { isAuthenticated } = useAuth();
    const [productQuery, setProductQuery] = useState(null);

    useEffect(() => {
        const params = new URLSearchParams(location.search);
        const product = params.get('product');

        // If someone manually hits /compare without a product, kick them back to /upload
        if (!product) {
            navigate('/upload', { replace: true });
        } else {
            setProductQuery(product);
            // Save search history
            if (isAuthenticated) {
                api.post('/advanced/search-history/', { query: product })
                   .catch(err => console.error('Failed to log search history', err));
            }
        }
    }, [location, navigate, isAuthenticated]);

    return (
        <div className="flex flex-col min-h-screen bg-gray-50">
            <Header />

            <main className="flex-grow">
                <div className="max-w-7xl mx-auto px-4 py-8">

                    <div className="mb-6 flex justify-between items-center">
                        <button
                            onClick={() => navigate('/upload')}
                            className="inline-flex items-center text-sm font-medium text-gray-600 hover:text-blue-600 transition-colors"
                        >
                            <ArrowLeft className="h-4 w-4 mr-2" />
                            New Search
                        </button>
                    </div>

                    {productQuery && (
                        <div className="flex flex-col gap-8 mb-12">
                            {/* Full Width Results */}
                            <section className="bg-white rounded-xl shadow-sm border border-gray-100 p-2 sm:p-6 w-full">
                                <ResultsDisplay productName={productQuery} />
                            </section>
                            
                            {/* Bottom Section: Graph & Share */}
                            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                                <div className="lg:col-span-2">
                                    <PriceTrendChart productName={productQuery} />
                                </div>
                                <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex flex-col items-center justify-center">
                                    <h3 className="text-lg font-bold text-gray-800 mb-4 text-center">Share these deals</h3>
                                    <SocialShare title={`Amazing deals on ${productQuery}`} />
                                </div>
                            </div>
                        </div>
                    )}

                </div>
            </main>

            <Footer />
        </div>
    );
};

export default Compare;
