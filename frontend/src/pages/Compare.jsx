import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import ResultsDisplay from '../components/results/ResultsDisplay';
import { ArrowLeft } from 'lucide-react';

const Compare = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const [productQuery, setProductQuery] = useState(null);

    useEffect(() => {
        const params = new URLSearchParams(location.search);
        const product = params.get('product');

        // If someone manually hits /compare without a product, kick them back to /upload
        if (!product) {
            navigate('/upload', { replace: true });
        } else {
            setProductQuery(product);
        }
    }, [location, navigate]);

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
                        <section className="bg-white rounded-xl shadow-sm border border-gray-100 p-2 sm:p-6 mb-12">
                            <ResultsDisplay productName={productQuery} />
                        </section>
                    )}

                </div>
            </main>

            <Footer />
        </div>
    );
};

export default Compare;
