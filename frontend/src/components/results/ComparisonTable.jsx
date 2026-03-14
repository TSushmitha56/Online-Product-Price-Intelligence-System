import React from 'react';
import { ExternalLink, Star, Truck, CheckCircle, AlertCircle, Award, Store } from 'lucide-react';

const ComparisonTable = ({ offers }) => {
  if (!offers || offers.length === 0) return null;

  return (
    <div className="w-full bg-white rounded-2xl shadow-[0_2px_20px_-4px_rgba(0,0,0,0.05)] border border-gray-100 overflow-hidden">
      <div className="overflow-x-auto scrollbar-thin scrollbar-thumb-gray-200">
        <table className="min-w-full border-collapse">
          <thead>
            <tr className="bg-gray-50/80 border-b border-gray-100">
              <th scope="col" className="px-8 py-4 text-left text-[11px] font-bold text-gray-400 uppercase tracking-widest">Store</th>
              <th scope="col" className="px-6 py-4 text-left text-[11px] font-bold text-gray-400 uppercase tracking-widest">Price Details</th>
              <th scope="col" className="px-6 py-4 text-left text-[11px] font-bold text-gray-400 uppercase tracking-widest">Rating</th>
              <th scope="col" className="px-6 py-4 text-left text-[11px] font-bold text-gray-400 uppercase tracking-widest">Status</th>
              <th scope="col" className="px-8 py-4 text-right text-[11px] font-bold text-gray-400 uppercase tracking-widest">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-50">
            {offers.map((offer, idx) => {
              const inStock = offer.availability?.toLowerCase().includes('stock');

              return (
                <tr
                  key={idx}
                  className={`group relative transition-colors duration-200 hover:bg-gray-50/50 ${offer.is_best_deal ? 'bg-indigo-50/20' : 'bg-white'
                    }`}
                >
                  {/* Left Accent Border for Best Deal */}
                  {offer.is_best_deal && (
                    <td className="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b from-indigo-500 to-violet-500 rounded-l-2xl"></td>
                  )}

                  {/* Store & Best Deal Tag */}
                  <td className="px-8 py-5 whitespace-nowrap">
                    <div className="flex flex-col items-start gap-2">
                      <div className="flex items-center gap-2">
                        <div className={`p-1.5 rounded-md ${offer.is_best_deal ? 'bg-indigo-100 text-indigo-600' : 'bg-gray-100 text-gray-500'}`}>
                          <Store className="w-4 h-4" />
                        </div>
                        <span className="text-base font-bold text-gray-900 tracking-tight">
                          {offer.store}
                        </span>
                      </div>

                      {offer.is_best_deal && (
                        <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-[10px] font-bold bg-gradient-to-r from-indigo-500 to-violet-500 text-white shadow-sm shadow-indigo-200/50 uppercase tracking-wider">
                          <Award className="w-3 h-3" />
                          Top Pick
                        </span>
                      )}
                    </div>
                  </td>

                  {/* Pricing */}
                  <td className="px-6 py-5 whitespace-nowrap">
                    <div className="flex flex-col">
                      <div className="flex items-baseline text-gray-900">
                        <span className="text-sm font-semibold text-gray-400 mr-1">$</span>
                        <span className="text-2xl font-black tracking-tight">{parseFloat(offer.final_price || 0).toFixed(2)}</span>
                      </div>
                      <div className="flex items-center mt-1.5 text-xs font-medium">
                        {offer.shipping > 0 ? (
                          <span className="text-gray-500 flex items-center gap-1.5">
                            <Truck className="w-3.5 h-3.5 text-gray-400" />
                            +${parseFloat(offer.shipping).toFixed(2)} delivery
                          </span>
                        ) : (
                          <span className="text-emerald-600 flex items-center gap-1.5">
                            <Truck className="w-3.5 h-3.5" />
                            Free shipping
                          </span>
                        )}
                      </div>
                    </div>
                  </td>

                  {/* Rating */}
                  <td className="px-6 py-5 whitespace-nowrap">
                    {offer.seller_rating ? (
                      <div className="flex items-center gap-1.5 bg-amber-50/80 px-2.5 py-1.5 rounded-lg border border-amber-100/50 w-fit">
                        <Star className="w-4 h-4 text-amber-500 fill-amber-500" />
                        <span className="text-sm font-bold text-amber-900">{offer.seller_rating}</span>
                        {/* Optional: Add review count if available */}
                        {offer.reviews_count && <span className="text-xs text-amber-700/60 ml-1 font-medium">({offer.reviews_count})</span>}
                      </div>
                    ) : (
                      <span className="text-sm text-gray-300 font-medium italic">No reviews</span>
                    )}
                  </td>

                  {/* Availability */}
                  <td className="px-6 py-5 whitespace-nowrap">
                    <span className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold border ${inStock
                        ? 'bg-emerald-50 text-emerald-700 border-emerald-200/60'
                        : 'bg-rose-50 text-rose-700 border-rose-200/60'
                      }`}>
                      {inStock ? (
                        <CheckCircle className="w-3.5 h-3.5 text-emerald-500" />
                      ) : (
                        <AlertCircle className="w-3.5 h-3.5 text-rose-500" />
                      )}
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
                        inline-flex items-center justify-center px-6 py-2.5 text-sm font-bold rounded-xl transition-all duration-300 ease-out active:scale-95
                        ${offer.is_best_deal
                          ? 'bg-gray-900 text-white hover:bg-indigo-600 hover:shadow-[0_8px_20px_rgb(79,70,229,0.25)] hover:-translate-y-0.5'
                          : 'bg-white text-gray-700 border border-gray-200 hover:border-gray-300 hover:bg-gray-50 hover:text-gray-900'
                        }
                      `}
                    >
                      View Deal
                      <ExternalLink className={`ml-2 w-4 h-4 ${offer.is_best_deal ? 'text-indigo-200 group-hover:text-white' : 'text-gray-400 group-hover:text-gray-600'} transition-colors`} />
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