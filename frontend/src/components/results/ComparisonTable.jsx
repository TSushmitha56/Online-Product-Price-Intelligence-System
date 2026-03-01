import React from 'react';
import { ExternalLink, Star, Truck, CheckCircle, AlertCircle } from 'lucide-react'; // Optional: If you don't have lucide-react, you can remove icons or use SVGs.

const ComparisonTable = ({ offers }) => {
  return (
    <div className="w-full overflow-hidden bg-white rounded-2xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-gray-100">
      <div className="overflow-x-auto">
        <table className="min-w-full">
          <thead>
            <tr className="border-b border-gray-100 bg-white">
              <th scope="col" className="px-8 py-5 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider">Store</th>
              <th scope="col" className="px-6 py-5 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider">Price Details</th>
              <th scope="col" className="px-6 py-5 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider">Rating</th>
              <th scope="col" className="px-6 py-5 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider">Status</th>
              <th scope="col" className="px-8 py-5 text-right text-xs font-semibold text-gray-400 uppercase tracking-wider"></th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-50">
            {offers.map((offer, idx) => {
              const inStock = offer.availability.toLowerCase().includes('stock');
              
              return (
                <tr 
                  key={idx} 
                  className={`group transition-all duration-200 hover:bg-gray-50/50 ${
                    offer.is_best_deal ? 'bg-indigo-50/30' : 'bg-white'
                  }`}
                >
                  {/* Store & Best Deal Tag */}
                  <td className="px-8 py-5 whitespace-nowrap">
                    <div className="flex flex-col items-start gap-1.5">
                      <span className="text-base font-bold text-gray-900 tracking-tight">
                        {offer.store}
                      </span>
                      {offer.is_best_deal && (
                        <span className="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold bg-gradient-to-r from-indigo-500 to-violet-500 text-white shadow-sm shadow-indigo-200">
                          BEST PRICE
                        </span>
                      )}
                    </div>
                  </td>
                  
                  {/* Pricing */}
                  <td className="px-6 py-5 whitespace-nowrap">
                    <div className="flex flex-col">
                      <div className="flex items-baseline text-gray-900">
                        <span className="text-sm font-medium mr-0.5">$</span>
                        <span className="text-xl font-bold">{offer.final_price.toFixed(2)}</span>
                      </div>
                      <div className="flex items-center mt-1 text-xs text-gray-500 font-medium">
                        {offer.shipping > 0 ? (
                          <>
                            <span>+${offer.shipping.toFixed(2)} delivery</span>
                          </>
                        ) : (
                          <span className="text-emerald-600 flex items-center">
                            Free shipping
                          </span>
                        )}
                      </div>
                    </div>
                  </td>
                  
                  {/* Rating */}
                  <td className="px-6 py-5 whitespace-nowrap">
                    {offer.seller_rating ? (
                      <div className="flex items-center bg-gray-50 w-fit px-2.5 py-1 rounded-lg border border-gray-100">
                        {/* Inline SVG for Star if no icon library */}
                        <svg className="w-3.5 h-3.5 text-amber-400 fill-current" viewBox="0 0 20 20">
                          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                        </svg>
                        <span className="ml-1.5 text-sm font-semibold text-gray-700">{offer.seller_rating}</span>
                      </div>
                    ) : (
                      <span className="text-xs text-gray-400 font-medium">—</span>
                    )}
                  </td>
                  
                  {/* Availability */}
                  <td className="px-6 py-5 whitespace-nowrap">
                    <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium border ${
                      inStock 
                        ? 'bg-emerald-50 text-emerald-700 border-emerald-100' 
                        : 'bg-rose-50 text-rose-700 border-rose-100'
                    }`}>
                      <span className={`w-1.5 h-1.5 rounded-full mr-2 ${inStock ? 'bg-emerald-500' : 'bg-rose-500'}`}></span>
                      {offer.availability}
                    </span>
                  </td>
                  
                  {/* Action */}
                  <td className="px-8 py-5 whitespace-nowrap text-right">
                    <a 
                      href={offer.product_url || "#"} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className={`
                        inline-flex items-center justify-center px-5 py-2.5 text-sm font-semibold rounded-full transition-all duration-200 ease-in-out
                        ${offer.is_best_deal 
                          ? 'bg-indigo-600 text-white hover:bg-indigo-700 hover:shadow-lg hover:shadow-indigo-200 hover:-translate-y-0.5' 
                          : 'bg-white text-gray-700 border border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                        }
                      `}
                    >
                      View Deal
                      {/* Inline SVG for Arrow */}
                      <svg className={`ml-2 w-4 h-4 ${offer.is_best_deal ? 'text-indigo-200' : 'text-gray-400'}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                      </svg>
                    </a>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ComparisonTable;