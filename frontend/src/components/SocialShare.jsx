import React, { useState } from 'react';
import { Twitter, Facebook, Share2, Copy, Check } from 'lucide-react';

const SocialShare = ({ url, title }) => {
    const [copied, setCopied] = useState(false);
    
    const encodedUrl = encodeURIComponent(url || window.location.href);
    const encodedTitle = encodeURIComponent(title || "Check out this product on PriceIntel!");

    const handleCopy = () => {
        navigator.clipboard.writeText(url || window.location.href);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    // Calculate generic WhatsApp URL
    const whatsappUrl = `https://api.whatsapp.com/send?text=${encodedTitle}%20${encodedUrl}`;

    return (
        <div className="flex items-center space-x-3 mt-4">
            <span className="text-sm font-medium text-gray-500 flex items-center">
                <Share2 className="w-4 h-4 mr-2" /> Share:
            </span>
            <a 
                href={`https://twitter.com/intent/tweet?url=${encodedUrl}&text=${encodedTitle}`}
                target="_blank" rel="noopener noreferrer"
                className="p-2 bg-gray-50 hover:bg-blue-50 text-gray-500 hover:text-blue-500 rounded-full transition-colors"
                title="Share on Twitter"
            >
                <Twitter className="w-4 h-4" />
            </a>
            <a 
                href={`https://www.facebook.com/sharer/sharer.php?u=${encodedUrl}`}
                target="_blank" rel="noopener noreferrer"
                className="p-2 bg-gray-50 hover:bg-blue-600 text-gray-500 hover:text-white rounded-full transition-colors"
                title="Share on Facebook"
            >
                <Facebook className="w-4 h-4" />
            </a>
            <a 
                href={whatsappUrl}
                target="_blank" rel="noopener noreferrer"
                className="p-2 bg-gray-50 hover:bg-green-500 text-gray-500 hover:text-white rounded-full transition-colors font-bold text-xs flex items-center justify-center w-8 h-8"
                title="Share on WhatsApp"
            >
                WA
            </a>
            <button 
                onClick={handleCopy}
                className={`p-2 rounded-full transition-colors ${copied ? 'bg-green-50 text-green-500' : 'bg-gray-50 hover:bg-gray-200 text-gray-500'}`}
                title="Copy Link"
            >
                {copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
            </button>
        </div>
    );
};

export default SocialShare;
