import React from 'react';

export const SortBar = ({ viewMode, setViewMode, sortOption, setSortOption, resultCount }) => {
  return (
    <div className="flex flex-col sm:flex-row justify-between items-center mb-8 gap-4">
      {/* Result Counter - Pill Style */}
      <div className="flex items-center bg-white px-4 py-2 rounded-full shadow-sm border border-gray-100">
        <span className="flex h-2 w-2 rounded-full bg-indigo-500 mr-2.5"></span>
        <span className="text-sm font-medium text-gray-600">
          Found <span className="text-gray-900 font-bold">{resultCount}</span> offers
        </span>
      </div>
      
      <div className="flex items-center gap-3">
        {/* Custom Styled Select */}
        <div className="relative group">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <svg className="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4h13M3 8h9m-9 4h6m4 0l4-4m0 0l4 4m-4-4v12" />
            </svg>
          </div>
          <select 
            id="sort" 
            value={sortOption}
            onChange={(e) => setSortOption(e.target.value)}
            className="appearance-none bg-white border border-gray-200 text-gray-700 text-sm font-medium rounded-xl pl-10 pr-10 py-2.5 shadow-sm hover:border-indigo-300 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all cursor-pointer"
          >
            <option value="price_asc">Price: Low to High</option>
            <option value="price_desc">Price: High to Low</option>
            <option value="rating_desc">Highest Rated</option>
          </select>
          <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
            <svg className="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </div>
        </div>

        {/* View Toggle - Segmented Control */}
        <div className="bg-gray-100 p-1 rounded-xl flex items-center border border-gray-200">
          <button 
            onClick={() => setViewMode('card')}
            className={`p-2 rounded-lg transition-all duration-200 ${
              viewMode === 'card' 
                ? 'bg-white text-indigo-600 shadow-sm transform scale-100' 
                : 'text-gray-400 hover:text-gray-600'
            }`}
            title="Card View"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"></path></svg>
          </button>
          <button 
            onClick={() => setViewMode('table')}
            className={`p-2 rounded-lg transition-all duration-200 ${
              viewMode === 'table' 
                ? 'bg-white text-indigo-600 shadow-sm transform scale-100' 
                : 'text-gray-400 hover:text-gray-600'
            }`}
            title="List View"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
          </button>
        </div>
      </div>
    </div>
  );
};

export const FilterPanel = ({ filters, setFilters, availableStores }) => {
  const handleStoreToggle = (store) => {
    setFilters(prev => {
      const isSelected = prev.stores.includes(store);
      if (isSelected) {
        return { ...prev, stores: prev.stores.filter(s => s !== store) };
      } else {
        return { ...prev, stores: [...prev.stores, store] };
      }
    });
  };

  return (
    <div className="bg-white rounded-3xl shadow-[0_2px_15px_-3px_rgba(0,0,0,0.07),0_10px_20px_-2px_rgba(0,0,0,0.04)] border border-gray-100 overflow-hidden sticky top-4">
      
      {/* Header */}
      <div className="px-6 py-5 border-b border-gray-50 bg-gray-50/30 backdrop-blur-sm flex justify-between items-center">
        <h3 className="font-bold text-gray-900 flex items-center text-lg">
          <span className="p-1.5 bg-indigo-100 rounded-lg mr-3 text-indigo-600">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"></path></svg>
          </span>
          Filters
        </h3>
        {(filters.freeShippingOnly || filters.inStockOnly || filters.stores.length !== availableStores.length) && (
           <button 
             onClick={() => setFilters({stores: availableStores, freeShippingOnly: false, inStockOnly: false})}
             className="text-xs font-semibold text-indigo-600 hover:text-indigo-800 transition-colors"
           >
             Reset
           </button>
        )}
      </div>

      <div className="p-6 space-y-8">
        
        {/* Stores Section */}
        <div>
          <h4 className="text-[11px] font-bold text-gray-400 mb-4 uppercase tracking-widest">Platforms</h4>
          <div className="space-y-1">
            {availableStores.map(store => {
              const checked = filters.stores.includes(store);
              return (
                <label 
                  key={store} 
                  className={`flex items-center justify-between p-2 rounded-xl cursor-pointer transition-all duration-200 ${checked ? 'hover:bg-indigo-50/50' : 'hover:bg-gray-50 opacity-60 hover:opacity-100'}`}
                >
                  <span className={`text-sm font-medium ${checked ? 'text-gray-800' : 'text-gray-500'}`}>{store}</span>
                  <div className="relative flex items-center">
                    <input 
                      type="checkbox" 
                      checked={checked}
                      onChange={() => handleStoreToggle(store)}
                      className="peer h-5 w-5 cursor-pointer appearance-none rounded-md border border-gray-300 transition-all checked:border-indigo-500 checked:bg-indigo-500 hover:border-indigo-400"
                    />
                    <svg className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-3.5 h-3.5 pointer-events-none text-white opacity-0 peer-checked:opacity-100 transition-opacity" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="3">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                </label>
              );
            })}
          </div>
        </div>

        <div className="h-px bg-gray-100 w-full"></div>

        {/* Preferences Section using Toggles */}
        <div>
          <h4 className="text-[11px] font-bold text-gray-400 mb-4 uppercase tracking-widest">Preferences</h4>
          
          <div className="space-y-4">
            {/* Free Shipping Toggle */}
            <label className="flex items-center justify-between cursor-pointer group">
              <div className="flex flex-col">
                <span className="text-sm font-semibold text-gray-700 group-hover:text-indigo-600 transition-colors">Free Shipping</span>
                <span className="text-[10px] text-gray-400">Show only free delivery</span>
              </div>
              <div className="relative">
                <input 
                  type="checkbox" 
                  checked={filters.freeShippingOnly}
                  onChange={(e) => setFilters(prev => ({ ...prev, freeShippingOnly: e.target.checked }))}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600 shadow-inner"></div>
              </div>
            </label>

            {/* In Stock Toggle */}
            <label className="flex items-center justify-between cursor-pointer group">
              <div className="flex flex-col">
                <span className="text-sm font-semibold text-gray-700 group-hover:text-indigo-600 transition-colors">Available Only</span>
                <span className="text-[10px] text-gray-400">Hide out of stock items</span>
              </div>
              <div className="relative">
                <input 
                  type="checkbox" 
                  checked={filters.inStockOnly}
                  onChange={(e) => setFilters(prev => ({ ...prev, inStockOnly: e.target.checked }))}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600 shadow-inner"></div>
              </div>
            </label>
          </div>
        </div>
      </div>
    </div>
  );
};