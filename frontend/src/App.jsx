/**
 * Main App Component
 * 
 * Integrates:
 * - Header with navigation
 * - Main content area with Image Upload component
 * - Backend status indicator
 * - Footer
 * 
 * Uses Tailwind CSS for responsive, modern styling
 */
import { useState, useEffect } from 'react';
import Header from './components/Header';
import Footer from './components/Footer';
import ImageUpload from './components/ImageUpload';
import ResultsDisplay from './components/results/ResultsDisplay';

function App() {
  const [backendMessage, setBackendMessage] = useState('');
  const [backendStatus, setBackendStatus] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Track the recognized product query from URL for deep linking
  const [productQuery, setProductQuery] = useState(() => {
    const params = new URLSearchParams(window.location.search);
    return params.get('product') || null;
  });

  // Automatically clean the URL on mount to remove the query parameter
  // This allows the query param to temporarily exist but cleans it up after refresh.
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    if (params.has('product')) {
      const newUrl = new URL(window.location);
      newUrl.searchParams.delete('product');
      window.history.replaceState({}, '', newUrl);
    }
  }, []);

  // Listen for browser back/forward navigation affecting the URL
  useEffect(() => {
    const handlePopState = () => {
      const params = new URLSearchParams(window.location.search);
      setProductQuery(params.get('product') || null);
    };
    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, []);

  const handleProductRecognized = (query) => {
    setProductQuery(query);
    const newUrl = new URL(window.location);
    newUrl.searchParams.set('product', query);
    window.history.pushState({}, '', newUrl);

    // Smooth scroll to results
    setTimeout(() => {
      document.getElementById('results')?.scrollIntoView({ behavior: 'smooth' });
    }, 100);
  };

  // Check backend connectivity on component mount
  useEffect(() => {
    fetch('http://localhost:8000/api/hello/')
      .then(response => {
        if (!response.ok) throw new Error('Backend not reachable');
        return response.json();
      })
      .then(data => {
        setBackendMessage(data.message);
        setBackendStatus(data.status);
        setError('');
      })
      .catch(err => {
        setError(`Backend Error: ${err.message}`);
        setBackendMessage('Backend not available');
        setBackendStatus('offline');
      })
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="flex flex-col min-h-screen bg-gray-100">
      {/* Header Component */}
      <Header />

      {/* Main Content Area */}
      <main className="flex-grow">
        <div className="max-w-7xl mx-auto px-4 py-12">
          {/* Backend Status Section */}
          <section className="mb-12">
            <div className="bg-white rounded-lg shadow p-6 max-w-6xl mx-auto">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">System Status</h2>

              {/* Backend Status Check */}
              {loading && (
                <div className="flex items-center space-x-2 text-blue-600">
                  <span className="text-xl">⏳</span>
                  <p>Checking backend connection...</p>
                </div>
              )}

              {!loading && !error && (
                <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                  <div className="flex items-start space-x-3">
                    <span className="text-2xl">✅</span>
                    <div>
                      <p className="text-green-800 font-semibold">{backendMessage}</p>
                      <p className="text-green-700 text-sm mt-1">Status: {backendStatus}</p>
                    </div>
                  </div>
                </div>
              )}

              {error && (
                <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                  <div className="flex items-start space-x-3">
                    <span className="text-2xl">❌</span>
                    <div>
                      <p className="text-red-800 font-semibold">{error}</p>
                      <p className="text-red-700 text-sm mt-2">
                        Make sure to run the backend:
                        <code className="bg-red-100 px-2 py-1 rounded block mt-1 font-mono">
                          python manage.py runserver
                        </code>
                      </p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </section>

          {/* Image Upload Section */}
          <section id="upload" className="bg-white rounded-lg shadow p-12 mb-12 max-w-6xl mx-auto">
            <ImageUpload onProductRecognized={handleProductRecognized} />
          </section>

          {/* Price Comparison Preview */}
          {productQuery && (
            <section id="results" className="bg-white rounded-lg shadow p-4 sm:p-8">
              <ResultsDisplay productName={productQuery} />
            </section>
          )}

        </div>
      </main>

      {/* Footer Component */}
      <Footer />
    </div>
  );
}

export default App;
