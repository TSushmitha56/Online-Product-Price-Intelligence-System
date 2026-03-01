import React, { useState, useEffect } from 'react';

/**
 * Header Component
 * Premium aesthetic with glassmorphism and sticky positioning
 */
export default function Header() {
  const [scrolled, setScrolled] = useState(false);

  // Add a subtle shadow only when scrolling
  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <header 
      className={`sticky top-0 z-50 transition-all duration-300 ${
        scrolled 
          ? 'bg-white/80 backdrop-blur-md border-b border-gray-100 shadow-sm py-3' 
          : 'bg-white/50 backdrop-blur-sm border-b border-transparent py-5'
      }`}
    >
      <nav className="max-w-7xl mx-auto px-6 flex justify-between items-center">
        
        {/* Logo Section */}
        <a href="#home" className="flex items-center group">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center text-white shadow-lg shadow-indigo-200 mr-3 transition-transform group-hover:rotate-3 group-hover:scale-105">
            <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
          <span className="text-xl font-extrabold tracking-tight text-gray-900 group-hover:text-indigo-600 transition-colors">
            ImageHub<span className="text-indigo-500">.</span>
          </span>
        </a>

        {/* Desktop Navigation */}
        <div className="flex items-center gap-1 md:gap-6">
          
          {/* Primary Action Button */}
          <a
            href="#upload"
            className="ml-2 flex items-center gap-2 bg-gray-900 hover:bg-black text-white text-sm font-semibold px-5 py-2.5 rounded-full shadow-lg shadow-gray-200 transition-all hover:-translate-y-0.5"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
            </svg>
            Upload
          </a>
        </div>
      </nav>
    </header>
  );
}