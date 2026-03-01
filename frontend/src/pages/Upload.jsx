import React from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import ImageUpload from '../components/ImageUpload';

const Upload = () => {
    const navigate = useNavigate();

    const handleProductRecognized = (query) => {
        // Navigate straight to compare page with query parameter
        navigate(`/compare?product=${encodeURIComponent(query)}`);
    };

    return (
        <div className="flex flex-col min-h-screen bg-gray-100">
            <Header />

            <main className="flex-grow flex items-center justify-center">
                <div className="w-full max-w-4xl mx-auto px-4 py-12">

                    <div className="text-center mb-10">
                        <h1 className="text-3xl font-bold text-gray-900 mb-4">Discover Better Prices</h1>
                        <p className="text-lg text-gray-600">
                            Upload a photo of any product to instantly compare live prices across major retailers.
                        </p>
                    </div>

                    <section className="bg-white rounded-2xl shadow-xl p-8 sm:p-12 mb-12">
                        <ImageUpload onProductRecognized={handleProductRecognized} />
                    </section>

                </div>
            </main>

            <Footer />
        </div>
    );
};

export default Upload;
