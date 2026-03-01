import React from 'react';

const ResultCard = ({ offer }) => {
  const { store, price, final_price, seller_rating, availability, image_url, product_url, is_best_deal } = offer;
  const shippingCost = final_price - price;
  const inStock = availability.toLowerCase().includes('stock');

  return (
    <div
      className={`group relative flex flex-col bg-white rounded-3xl transition-all duration-300 ease-out hover:-translate-y-1 hover:shadow-xl ${is_best_deal
        ? 'shadow-[0_10px_40px_-10px_rgba(79,70,229,0.2)] ring-1 ring-indigo-50'
        : 'shadow-[0_4px_20px_-5px_rgba(0,0,0,0.05)] border border-gray-100'
        }`}
    >
      {/* Image Section */}
      <div className="relative h-56 w-full p-6 flex items-center justify-center bg-gray-50/50 rounded-t-3xl overflow-hidden">

        {/* Best Deal Badge - Floating Glass Style */}
        {is_best_deal && (
          <div className="absolute top-4 left-4 z-10 px-3 py-1.5 rounded-full bg-indigo-600/90 backdrop-blur-sm text-white text-[10px] font-bold tracking-wider shadow-lg shadow-indigo-200">
            BEST PRICE
          </div>
        )}

        {/* Product Image with Zoom Effect */}
        {image_url ? (
          <img
            src={image_url}
            alt="Product"
            className="relative z-0 max-h-full max-w-full object-contain mix-blend-multiply transition-transform duration-500 group-hover:scale-110"
          />
        ) : (
          <div className="text-5xl opacity-20">📦</div>
        )}
      </div>

      {/* Content Section */}
      <div className="p-6 flex flex-col flex-grow bg-white rounded-b-3xl">

        {/* Header: Store & Rating */}
        <div className="flex justify-between items-start mb-3">
          <span className="text-sm font-bold text-gray-400 uppercase tracking-wide">
            {store}
          </span>
          {seller_rating && (
            <div className="flex items-center space-x-1">
              {/* Star Icon */}
              <svg className="w-3.5 h-3.5 text-amber-400 fill-current" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
              <span className="text-sm font-bold text-gray-700">{seller_rating}</span>
            </div>
          )}
        </div>

        {/* Pricing Block */}
        <div className="mb-6">
          <div className="flex items-baseline text-gray-900">
            <span className="text-lg font-semibold mr-0.5">$</span>
            <span className="text-4xl font-extrabold tracking-tight">{final_price.toFixed(2)}</span>
          </div>

          <div className="mt-1 flex items-center text-xs font-medium text-gray-500">
            {shippingCost > 0.01 ? (
              <>
                <span className="line-through mr-1.5 opacity-60">${price.toFixed(2)}</span>
                <span className="text-indigo-600">+ ${shippingCost.toFixed(2)} shipping</span>
              </>
            ) : (
              <span className="text-emerald-600 flex items-center bg-emerald-50 px-2 py-0.5 rounded-md">
                Free shipping
              </span>
            )}
          </div>
        </div>

        {/* Trust Indicators */}
        <div className="mt-auto space-y-3 mb-6">
          <div className="flex items-center text-sm font-medium">
            <span className={`flex h-2 w-2 rounded-full mr-2.5 ${inStock ? 'bg-emerald-500' : 'bg-rose-500'}`}></span>
            <span className={inStock ? 'text-gray-700' : 'text-rose-600'}>
              {availability}
            </span>
          </div>

          {seller_rating >= 4.5 && (
            <div className="flex items-center text-xs text-blue-600 bg-blue-50 px-2.5 py-1.5 rounded-lg w-fit">
              <svg className="w-3.5 h-3.5 mr-1.5" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"></path></svg>
              Trusted Seller
            </div>
          )}
        </div>

        {/* Action Button */}
        <a
          href={product_url || "#"}
          target="_blank"
          rel="noopener noreferrer"
          className={`
            w-full flex items-center justify-center py-3.5 rounded-2xl text-sm font-bold tracking-wide transition-all duration-200
            ${is_best_deal
              ? 'bg-gray-900 text-white hover:bg-black hover:shadow-lg hover:-translate-y-0.5'
              : 'bg-white text-gray-900 border-2 border-gray-100 hover:border-gray-200 hover:bg-gray-50'
            }
          `}
        >
          View Deal
          <svg className={`ml-2 w-4 h-4 ${is_best_deal ? 'text-gray-400' : 'text-gray-400'}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
          </svg>
        </a>
      </div>
    </div>
  );
};

export default ResultCard;