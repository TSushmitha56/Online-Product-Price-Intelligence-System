import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Camera, Search, TrendingUp, ArrowRight, ShieldCheck, Zap } from 'lucide-react';
import Header from '../components/Header';
import Footer from '../components/Footer';

const Home = () => {
    const navigate = useNavigate();

    return (
        <div className="flex flex-col min-h-screen bg-gray-50">
            <Header />

            <main className="flex-grow">
                {/* Hero Section */}
                <div className="relative overflow-hidden bg-white">
                    <div className="max-w-7xl mx-auto">
                        <div className="relative z-10 pb-8 bg-white sm:pb-16 md:pb-20 lg:max-w-2xl lg:w-full lg:pb-28 xl:pb-32 px-4 sm:px-6 lg:px-8 mt-16 sm:mt-24">
                            <div className="sm:text-center lg:text-left">
                                <h1 className="text-4xl tracking-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
                                    <span className="block xl:inline">AI-Powered Product</span>{' '}
                                    <span className="block text-blue-600 xl:inline">Intelligence</span>
                                </h1>
                                <p className="mt-3 text-base text-gray-500 sm:mt-5 sm:text-lg sm:max-w-xl sm:mx-auto md:mt-5 md:text-xl lg:mx-0">
                                    Instantly identify products from any image, compare real-time prices across major retailers like Amazon, Walmart, and eBay, and track historical pricing data to secure the best deals.
                                </p>
                                <div className="mt-5 sm:mt-8 sm:flex sm:justify-center lg:justify-start">
                                    <div className="rounded-md shadow">
                                        <button
                                            onClick={() => navigate('/upload')}
                                            className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 md:py-4 md:text-lg md:px-10 transition-colors"
                                        >
                                            Try It Now
                                            <ArrowRight className="ml-2 h-5 w-5" />
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="lg:absolute lg:inset-y-0 lg:right-0 lg:w-1/2 bg-gray-100 flex items-center justify-center p-12">
                        {/* Abstract visual representation of scanning */}
                        <div className="relative w-full max-w-lg">
                            <div className="absolute top-0 -left-4 w-72 h-72 bg-blue-400 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob"></div>
                            <div className="absolute top-0 -right-4 w-72 h-72 bg-purple-400 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-2000"></div>
                            <div className="absolute -bottom-8 left-20 w-72 h-72 bg-indigo-400 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-4000"></div>
                            <div className="relative border-4 border-gray-200 bg-white rounded-2xl shadow-xl p-8 transform rotate-3 hover:rotate-0 transition-transform duration-500">
                                <div className="flex justify-between items-center border-b pb-4 mb-4">
                                    <div className="h-4 w-24 bg-gray-200 rounded"></div>
                                    <div className="h-4 w-12 bg-blue-200 rounded"></div>
                                </div>
                                <div className="space-y-3">
                                    <div className="h-2 w-full bg-gray-100 rounded"></div>
                                    <div className="h-2 w-5/6 bg-gray-100 rounded"></div>
                                    <div className="h-2 w-4/6 bg-gray-100 rounded"></div>
                                </div>
                                <div className="mt-6 flex justify-between items-end">
                                    <div className="h-10 w-10 bg-gray-200 rounded-full"></div>
                                    <div className="h-8 w-24 bg-blue-600 rounded"></div>
                                </div>
                                {/* Scanner line overlay */}
                                <div className="absolute top-0 left-0 right-0 h-1 bg-blue-500 shadow-[0_0_15px_rgba(59,130,246,0.5)] animate-scan"></div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Feature Highlights */}
                <div className="py-16 bg-gray-50">
                    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <div className="text-center">
                            <h2 className="text-base text-blue-600 font-semibold tracking-wide uppercase">Features</h2>
                            <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
                                A better way to shop smarter
                            </p>
                        </div>

                        <div className="mt-10">
                            <dl className="space-y-10 md:space-y-0 md:grid md:grid-cols-3 md:gap-x-8 md:gap-y-10">
                                {[
                                    {
                                        name: 'Image Recognition',
                                        description: 'Upload any photo and our AI instantly identifies the exact product, brand, and model.',
                                        icon: Camera,
                                    },
                                    {
                                        name: 'Live Price Comparison',
                                        description: 'We simultaneously query Amazon, Walmart, and eBay to find the absolute best current price in stock.',
                                        icon: Search,
                                    },
                                    {
                                        name: 'Historical Tracking',
                                        description: 'View 30-day price histories so you know if you are actually getting a real deal.',
                                        icon: TrendingUp,
                                    },
                                ].map((feature) => (
                                    <div key={feature.name} className="relative bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                                        <dt>
                                            <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-blue-500 text-white">
                                                <feature.icon className="h-6 w-6" aria-hidden="true" />
                                            </div>
                                            <p className="ml-16 text-lg leading-6 font-medium text-gray-900">{feature.name}</p>
                                        </dt>
                                        <dd className="mt-2 ml-16 text-base text-gray-500">{feature.description}</dd>
                                    </div>
                                ))}
                            </dl>
                        </div>
                    </div>
                </div>
            </main>

            <Footer />
        </div>
    );
};

export default Home;
