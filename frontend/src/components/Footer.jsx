import React from 'react';
import { Link } from 'react-router-dom';

export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-gradient-to-r from-blue-50 to-indigo-50 border-t border-gray-100 mt-20">
      <div className="max-w-7xl mx-auto px-6 py-12">

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-12 mb-12">

          {/* Brand & About Section (Spans 5 columns) */}
          <div className="md:col-span-5 space-y-4">
            <h2 className="text-2xl font-black tracking-tighter text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-violet-600 w-fit">
              ImageHub.
            </h2>
            <p className="text-sm text-gray-600 leading-relaxed max-w-xs">
              A modern product intelligence platform crafted for smart shoppers. Identify, compare, and track real-time prices with elegance and ease.
            </p>

            {/* Social Icons */}
            <div className="flex space-x-3 pt-2">
              <a href="#twitter" aria-label="Twitter" className="w-8 h-8 flex items-center justify-center rounded-full bg-gray-50 text-gray-400 hover:bg-indigo-100 hover:text-indigo-600 transition-all duration-200">
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z" /></svg>
              </a>
              <a href="#github" aria-label="GitHub" className="w-8 h-8 flex items-center justify-center rounded-full bg-gray-50 text-gray-400 hover:bg-gray-800 hover:text-white transition-all duration-200">
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" /></svg>
              </a>
            </div>
          </div>

          {/* Spacer */}
          <div className="md:col-span-1"></div>

          {/* Links Section 1 */}
          <div className="md:col-span-3">
            <h3 className="text-sm font-bold text-gray-900 uppercase tracking-wider mb-4">Product</h3>
            <ul className="space-y-3">
              <li><Link to="/home" className="text-sm text-gray-500 hover:text-indigo-600 transition-colors">Features</Link></li>
              <li><Link to="/home" className="text-sm text-gray-500 hover:text-indigo-600 transition-colors">Integrations</Link></li>
              <li><Link to="/home" className="text-sm text-gray-500 hover:text-indigo-600 transition-colors">Pricing</Link></li>
              <li><Link to="/home" className="text-sm text-gray-500 hover:text-indigo-600 transition-colors">Changelog</Link></li>
            </ul>
          </div>

          {/* Links Section 2 */}
          <div className="md:col-span-3">
            <h3 className="text-sm font-bold text-gray-900 uppercase tracking-wider mb-4">Legal & Help</h3>
            <ul className="space-y-3">
              <li><Link to="/home" className="text-sm text-gray-500 hover:text-indigo-600 transition-colors">Privacy Policy</Link></li>
              <li><Link to="/home" className="text-sm text-gray-500 hover:text-indigo-600 transition-colors">Terms of Service</Link></li>
              <li><Link to="/home" className="text-sm text-gray-500 hover:text-indigo-600 transition-colors">Contact Support</Link></li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-gray-100 pt-8 flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="text-xs text-gray-400">
            &copy; {currentYear} NEXORA Inc. All rights reserved.
          </p>

          <div className="flex items-center space-x-6">
            <span className="text-xs text-gray-400 flex items-center">
              Made with
              <svg className="w-3 h-3 mx-1 text-red-400 fill-current" viewBox="0 0 20 20"><path fillRule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clipRule="evenodd"></path></svg>
              in Design City
            </span>
          </div>
        </div>
      </div>
    </footer>
  );
}