import React, { useState, useMemo, useEffect, useCallback } from 'react';
import ResultCard from './ResultCard';
import ComparisonTable from './ComparisonTable';
import { SortBar, FilterPanel } from './SortBar';

// Premium Skeleton Loader
const SkeletonCard = () => (
  <div className="bg-white rounded-3xl p-4 shadow-sm border border-gray-100 flex flex-col h-full animate-pulse">
    <div className="h-56 bg-gray-100 rounded-2xl w-full mb-6"></div>
    <div className="px-2 flex flex-col flex-grow space-y-4">
      <div className="flex justify-between items-center">
        <div className="h-4 bg-gray-100 rounded-full w-1/3"></div>
        <div className="h-4 bg-gray-100 rounded-full w-12"></div>
      </div>
      <div className="space-y-2">
        <div className="h-8 bg-gray-100 rounded-lg w-1/2"></div>
        <div className="h-3 bg-gray-100 rounded-full w-1/3"></div>
      </div>
      <div className="mt-auto pt-4">
        <div className="h-12 bg-gray-100 rounded-xl w-full"></div>
      </div>
    </div>
  </div>
);

// Stat Card Component for the Header
const StatBadge = ({ label, value, icon, colorClass }) => (
  <div className="flex items-center gap-3 px-5 py-3 bg-white rounded-2xl border border-gray-100 shadow-sm transition-transform hover:-translate-y-0.5">
    <div className={`p-2 rounded-xl ${colorClass} bg-opacity-10`}>
      {icon}
    </div>
    <div className="flex flex-col">
      <span className="text-[10px] uppercase tracking-wider font-bold text-gray-400">{label}</span>
      <span className="text-lg font-bold text-gray-900">${value}</span>
    </div>
  </div>
);

const ResultsDisplay = ({ productName }) => {
  const [viewMode, setViewMode] = useState('card');
  const [sortOption, setSortOption] = useState('price_asc');
  
  // Data States
  const [results, setResults] = useState([]);
  const [isPolling, setIsPolling] = useState(false);
  
  // Loading & Error States
  const [loading, setLoading] = useState(false);
  const [errorType, setErrorType] = useState(null); 
  
  // Fetch Function Strategy Pattern
  const fetchPrices = useCallback(async (isBackground = false) => {
    if (!productName) return;

    if (!isBackground) {
        setLoading(true);
        setErrorType(null);
    } else {
        setIsPolling(true);
    }
    
    try {
      // Note: Ensure this URL is correct for your backend
      const response = await fetch(`http://localhost:8000/api/compare-prices/?product=${encodeURIComponent(productName)}`);
      
      if (!response.ok) {
        if (response.status === 429) throw new Error('rate_limit');
        throw new Error('server');
      }

      const data = await response.json();
      const fetchedOffers = data.results || [];

      // Map API Schema to ResultCard Schema
      let mapped = fetchedOffers.map(o => ({
        store: o.platform,
        title: o.title,
        price: parseFloat(o.price),
        final_price: parseFloat(o.price),
        shipping: 0,
        currency: o.currency || 'USD',
        product_url: o.product_url,
        availability: 'In Stock',
        seller_rating: 4.8, // Mocking for aesthetic demo if null
        image_url: o.image_url || null
      }));

      // Calculate "Best Deal"
      if (mapped.length > 0) {
          const lowest = Math.min(...mapped.map(m => m.final_price));
          mapped = mapped.map(m => ({
              ...m,
              is_best_deal: m.final_price === lowest
          }));
      }

      setResults(mapped);
      setErrorType(null);
    } catch (err) {
      console.error("Comparison fetch failed:", err);
      if (err.message === 'rate_limit') setErrorType('rate_limit');
      else setErrorType('network');
    } finally {
      if (!isBackground) setLoading(false);
      setIsPolling(false);
    }
  }, [productName]);

  // Initial Fetch & 30s Polling
  useEffect(() => {
    fetchPrices(false);
    const intervalId = setInterval(() => { fetchPrices(true); }, 30000);
    return () => clearInterval(intervalId);
  }, [fetchPrices]);

  // Summary Stats
  const summary = useMemo(() => {
    if (!results || results.length === 0) return { lowest: 0, average: 0, highest: 0 };
    const prices = results.map(r => r.final_price).filter(p => !isNaN(p) && p > 0);
    if (prices.length === 0) return { lowest: 0, average: 0, highest: 0 };
    return {
      lowest: Math.min(...prices).toFixed(2),
      highest: Math.max(...prices).toFixed(2),
      average: (prices.reduce((a, b) => a + b, 0) / prices.length).toFixed(2)
    };
  }, [results]);

  // Filters
  const availableStores = useMemo(() => {
    return Array.from(new Set(results.map(r => r.store)));
  }, [results]);

  const [filters, setFilters] = useState({
    stores: availableStores,
    freeShippingOnly: false,
    inStockOnly: false
  });

  useEffect(() => {
     setFilters(prev => ({ ...prev, stores: availableStores }));
  }, [availableStores]);

  // Filter & Sort Logic
  const processedResults = useMemo(() => {
    let filtered = results.filter(item => {
      if (filters.stores.length > 0 && !filters.stores.includes(item.store)) return false;
      if (filters.freeShippingOnly && item.shipping > 0) return false;
      if (filters.inStockOnly && !item.availability.toLowerCase().includes('in stock')) return false;
      return true;
    });

    filtered.sort((a, b) => {
      if (sortOption === 'price_asc') return a.final_price - b.final_price;
      if (sortOption === 'price_desc') return b.final_price - a.final_price;
      if (sortOption === 'rating_desc') return (b.seller_rating || 0) - (a.seller_rating || 0);
      return 0;
    });

    return filtered;
  }, [results, filters, sortOption]);

  // Error State Component
  if (errorType && !results.length) {
     return (
       <div className="min-h-[50vh] flex items-center justify-center">
         <div className="bg-white p-10 rounded-3xl border border-red-100 shadow-[0_10px_40px_-10px_rgba(254,202,202,0.3)] text-center max-w-md mx-auto">
            <div className="w-16 h-16 bg-red-50 text-red-500 rounded-full flex items-center justify-center mx-auto mb-6 text-2xl">⚠️</div>
            <h3 className="text-2xl font-bold text-gray-900 mb-2">
              {errorType === 'rate_limit' ? 'Too Many Requests' : 'Connection Error'}
            </h3>
            <p className="text-gray-500 mb-8 leading-relaxed">
              {errorType === 'rate_limit' 
                ? 'We are receiving too much traffic. Please take a breather and try again in a minute.' 
                : 'We couldn\'t connect to the pricing servers. Please check your internet connection.'}
            </p>
            <button 
               onClick={() => fetchPrices(false)}
               className="px-8 py-3 bg-red-600 hover:bg-red-700 text-white font-semibold rounded-xl transition-all shadow-lg shadow-red-200 hover:-translate-y-0.5"
            >
               Retry Connection
            </button>
         </div>
       </div>
     );
  }

  return (
    <div className="min-h-screen bg-gray-50/50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 animate-fade-in">
        
        {/* --- Header Section --- */}
        <div className="mb-10 flex flex-col lg:flex-row items-end justify-between gap-8">
          <div className="flex-1 w-full">
            <div className="flex items-center gap-3 mb-2">
              <span className="px-3 py-1 rounded-full bg-indigo-50 text-indigo-600 text-[11px] font-bold uppercase tracking-wider">
                Price Comparison
              </span>
              {isPolling && (
                <span className="flex items-center gap-2 text-xs font-medium text-green-600 bg-green-50 px-3 py-1 rounded-full border border-green-100">
                  <span className="relative flex h-2 w-2">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
                  </span>
                  Live Updates
                </span>
              )}
            </div>
            
            <h1 className="text-4xl font-extrabold text-gray-900 tracking-tight mb-2">
              Results for <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-violet-600">"{productName}"</span>
            </h1>
            <p className="text-gray-500 text-lg">We found {results.length} offers from trusted stores.</p>
          </div>

          {/* Stats & Actions */}
          <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-4 w-full lg:w-auto">
            {results.length > 0 && (
              <div className="flex gap-4">
                <StatBadge 
                  label="Lowest Price" 
                  value={summary.lowest} 
                  colorClass="text-emerald-600 bg-emerald-50"
                  icon={
                    <svg className="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path></svg>
                  }
                />
                <StatBadge 
                  label="Average" 
                  value={summary.average} 
                  colorClass="text-blue-600 bg-blue-50"
                  icon={
                    <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
                  }
                />
              </div>
            )}

            <button 
              onClick={() => fetchPrices(false)}
              disabled={loading || isPolling}
              className="group flex items-center justify-center gap-2 px-6 py-3 bg-white text-gray-700 border border-gray-200 rounded-2xl hover:border-indigo-300 hover:text-indigo-600 transition-all shadow-sm hover:shadow-md disabled:opacity-50"
            >
              <svg className={`w-5 h-5 ${loading || isPolling ? 'animate-spin text-indigo-500' : 'text-gray-400 group-hover:text-indigo-500'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
              <span className="font-semibold text-sm">Refresh</span>
            </button>
          </div>
        </div>

        <div className="flex flex-col lg:flex-row gap-8 items-start">
          
          {/* Left Sidebar: Filters */}
          <div className="w-full lg:w-72 flex-shrink-0 sticky top-4">
             {/* Wrapping FilterPanel in a clean container in case the component itself isn't styled */}
             <div className="bg-white rounded-3xl shadow-sm border border-gray-100 overflow-hidden p-1">
               <FilterPanel 
                 filters={filters} 
                 setFilters={setFilters} 
                 availableStores={availableStores} 
               />
             </div>
          </div>

          {/* Right Content Area */}
          <div className="flex-1 min-w-0 w-full">
            <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-2 mb-6">
              <SortBar 
                viewMode={viewMode} 
                setViewMode={setViewMode}
                sortOption={sortOption}
                setSortOption={setSortOption}
                resultCount={processedResults.length}
              />
            </div>

            {loading ? (
               <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                  {[...Array(6)].map((_, i) => <SkeletonCard key={i} />)}
               </div>
            ) : processedResults.length === 0 ? (
              <div className="bg-white py-16 px-8 text-center rounded-3xl border border-dashed border-gray-300">
                <div className="text-6xl mb-4 grayscale opacity-50">🧐</div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">No matching deals found</h3>
                <p className="text-gray-500 max-w-sm mx-auto mb-6">We couldn't find any products matching your active filters.</p>
                <button 
                  onClick={() => setFilters({stores: availableStores, freeShippingOnly: false, inStockOnly: false})}
                  className="text-indigo-600 font-bold hover:text-indigo-800 underline decoration-2 underline-offset-4"
                >
                  Clear all filters
                </button>
              </div>
            ) : (
              <div className="relative">
                {/* Subtle overlay during background polling */}
                {isPolling && (
                    <div className="absolute inset-0 bg-white/60 backdrop-blur-[1px] z-10 rounded-3xl transition-opacity duration-500"></div>
                )}
                
                {viewMode === 'card' ? (
                  <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                    {processedResults.map((offer, idx) => (
                       <ResultCard key={`${offer.store}-${offer.price}-${idx}`} offer={offer} />
                    ))}
                  </div>
                ) : (
                  <ComparisonTable offers={processedResults} />
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultsDisplay;