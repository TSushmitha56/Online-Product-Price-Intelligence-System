import React, { useState } from 'react';
import {
  Heart,
  Layers,
  Check,
  Star,
  ShieldCheck,
  Package,
  ArrowRight,
  Truck,
  CheckCircle,
  XCircle
} from 'lucide-react';
import api from '../../api/axios';
import { useAuth } from '../../context/AuthContext';
import { addToCompareBasket } from '../ComparisonBasket';

const ResultCard = ({ offer, productName }) => {
  const {
    store,
    price,
    final_price,
    seller_rating,
    availability,
    image_url,
    product_url,
    is_best_deal,
    title
  } = offer;

  // Safe math for pricing
  const safeFinalPrice = Number(final_price) || 0;
  const safeOriginalPrice = Number(price) || 0;
  const shippingCost = Math.max(0, safeFinalPrice - safeOriginalPrice);

  const inStock = availability?.toLowerCase().includes('stock');
  const displayTitle = productName || title || 'Unknown Product';

  const { isAuthenticated } = useAuth();
  const [wishlistAdded, setWishlistAdded] = useState(false);
  const [compareAdded, setCompareAdded] = useState(false);

  const handleWishlist = async (e) => {
    e.preventDefault();
    if (!isAuthenticated) return alert('Please sign in to save to wishlist');
    try {
      await api.post('/advanced/wishlist/', {
        product_name: displayTitle,
        product_url,
        image_url,
        price: safeFinalPrice,
        store
      });
      setWishlistAdded(true);
    } catch (err) {
      console.error('Failed to add to wishlist', err);
    }
  };

  const handleCompare = (e) => {
    e.preventDefault();
    const added = addToCompareBasket({
      ...offer, // Spread original offer details for the comparison table
      product_name: displayTitle,
      product_url,
      image_url,
      price: safeOriginalPrice,
      final_price: safeFinalPrice,
      store
    });
    if (added) setCompareAdded(true);
  };

  return (
    <div
      className={`group relative flex flex-col h-full bg-white rounded-3xl transition-all duration-300 ease-[cubic-bezier(0.23,1,0.32,1)] hover:-translate-y-1.5 
        ${is_best_deal
          ? 'shadow-[0_8px_30px_rgb(79,70,229,0.12)] border border-indigo-100 ring-1 ring-indigo-50'
          : 'shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-gray-100 hover:shadow-[0_20px_40px_rgb(0,0,0,0.08)]'
        }`}
    >
      {/* --- Image Section --- */}
      <div className="relative h-56 w-full p-6 flex items-center justify-center bg-gray-50/80 rounded-t-3xl overflow-hidden">

        {/* Best Deal Badge */}
        {is_best_deal && (
          <div className="absolute top-4 left-4 z-10">
            <span className="px-3 py-1.5 rounded-xl bg-gradient-to-r from-indigo-600 to-violet-600 text-white text-[10px] font-bold uppercase tracking-widest shadow-lg shadow-indigo-200/50">
              Top Pick
            </span>
          </div>
        )}

        {/* Floating Action Buttons */}
        <div className="absolute top-4 right-4 z-10 flex flex-col gap-2">
          <button
            onClick={handleWishlist}
            className={`p-2.5 rounded-full backdrop-blur-md border shadow-sm transition-all duration-300 active:scale-90 ${wishlistAdded
                ? 'bg-rose-50 border-rose-100 text-rose-500'
                : 'bg-white/90 border-gray-100 text-gray-400 hover:text-rose-500 hover:bg-white hover:shadow-md'
              }`}
            title="Save to Wishlist"
          >
            {wishlistAdded ? <Check className="w-4 h-4" /> : <Heart className="w-4 h-4" />}
          </button>
          <button
            onClick={handleCompare}
            className={`p-2.5 rounded-full backdrop-blur-md border shadow-sm transition-all duration-300 active:scale-90 ${compareAdded
                ? 'bg-blue-50 border-blue-100 text-blue-500'
                : 'bg-white/90 border-gray-100 text-gray-400 hover:text-blue-500 hover:bg-white hover:shadow-md'
              }`}
            title="Add to Compare"
          >
            {compareAdded ? <Check className="w-4 h-4" /> : <Layers className="w-4 h-4" />}
          </button>
        </div>

        {/* Product Image */}
        {image_url ? (
          <img
            src={image_url}
            alt={displayTitle}
            className="relative z-0 max-h-full max-w-full object-contain mix-blend-multiply transition-transform duration-500 group-hover:scale-110"
            loading="lazy"
          />
        ) : (
          <Package className="w-16 h-16 text-gray-200 transition-transform duration-500 group-hover:scale-110" />
        )}
      </div>

      {/* --- Content Section --- */}
      <div className="p-6 flex flex-col flex-grow bg-white rounded-b-3xl">

        {/* Store & Rating Header */}
        <div className="flex justify-between items-center mb-3">
          <span className="text-xs font-black text-gray-400 uppercase tracking-widest">
            {store}
          </span>
          {seller_rating && (
            <div className="flex items-center gap-1 bg-amber-50 px-2 py-1 rounded-md">
              <Star className="w-3.5 h-3.5 text-amber-500 fill-amber-500" />
              <span className="text-xs font-bold text-amber-700">{seller_rating}</span>
            </div>
          )}
        </div>

        {/* Product Title */}
        <h3 className="text-base font-semibold text-gray-900 leading-snug line-clamp-2 mb-4 group-hover:text-indigo-600 transition-colors">
          {displayTitle}
        </h3>

        {/* Pricing Block */}
        <div className="mt-auto mb-5">
          <div className="flex items-baseline text-gray-900">
            <span className="text-sm font-semibold text-gray-400 mr-1">$</span>
            <span className="text-3xl font-black tracking-tight">{safeFinalPrice.toFixed(2)}</span>
          </div>

          <div className="mt-1.5 flex items-center text-xs font-medium">
            {shippingCost > 0 ? (
              <div className="flex items-center text-gray-500">
                <span className="line-through opacity-70 mr-2">${safeOriginalPrice.toFixed(2)}</span>
                <span className="text-gray-600 flex items-center gap-1">
                  <Truck className="w-3.5 h-3.5" />
                  +${shippingCost.toFixed(2)} shipping
                </span>
              </div>
            ) : (
              <span className="text-emerald-600 flex items-center gap-1 bg-emerald-50/80 w-fit px-2 py-0.5 rounded-md">
                <Truck className="w-3.5 h-3.5" />
                Free shipping
              </span>
            )}
          </div>
        </div>

        {/* Trust Indicators (Badges) */}
        <div className="flex flex-wrap gap-2 mb-6">
          <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-[11px] font-semibold border ${inStock ? 'bg-emerald-50 text-emerald-700 border-emerald-100' : 'bg-rose-50 text-rose-700 border-rose-100'
            }`}>
            {inStock ? <CheckCircle className="w-3 h-3" /> : <XCircle className="w-3 h-3" />}
            {availability}
          </span>

          {seller_rating >= 4.5 && (
            <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-[11px] font-semibold bg-blue-50 text-blue-700 border border-blue-100">
              <ShieldCheck className="w-3 h-3" />
              Trusted
            </span>
          )}
        </div>

        {/* View Deal Button */}
        <a
          href={product_url || "#"}
          target="_blank"
          rel="noopener noreferrer"
          className={`
            w-full flex items-center justify-center py-3.5 rounded-2xl text-sm font-bold tracking-wide transition-all duration-300 active:scale-[0.98]
            ${is_best_deal
              ? 'bg-gray-900 text-white hover:bg-indigo-600 hover:shadow-[0_8px_20px_rgb(79,70,229,0.25)]'
              : 'bg-white text-gray-800 border-2 border-gray-100 hover:border-gray-200 hover:bg-gray-50 hover:text-gray-900'
            }
          `}
        >
          View Deal
          <ArrowRight className={`ml-2 w-4 h-4 ${is_best_deal ? 'text-indigo-300' : 'text-gray-400'}`} />
        </a>
      </div>
    </div>
  );
};

export default ResultCard;