import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { 
      hasError: false, 
      error: null, 
      errorInfo: null,
      showDetails: false 
    };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("ErrorBoundary caught an error:", error, errorInfo);
    this.setState({ errorInfo });
  }

  toggleDetails = () => {
    this.setState(prevState => ({ showDetails: !prevState.showDetails }));
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-gray-50/50 flex flex-col justify-center items-center p-6 animate-fade-in">
          
          <div className="max-w-md w-full bg-white rounded-3xl shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)] border border-gray-100 overflow-hidden relative">
            
            {/* Background Decorative Blob */}
            <div className="absolute top-0 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-indigo-50 rounded-full blur-3xl opacity-60 pointer-events-none"></div>

            <div className="relative z-10 p-8 flex flex-col items-center text-center">
              
              {/* Icon */}
              <div className="w-20 h-20 bg-rose-50 rounded-full flex items-center justify-center mb-6 shadow-sm">
                <svg className="w-10 h-10 text-rose-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              </div>

              {/* Headline */}
              <h2 className="text-2xl font-extrabold text-gray-900 mb-3 tracking-tight">
                Application Glitch
              </h2>
              
              <p className="text-gray-500 mb-8 leading-relaxed">
                We've encountered an unexpected issue. Don't worry, your data is safe. We just need to refresh the page.
              </p>
              
              {/* Actions */}
              <button
                onClick={() => window.location.reload()}
                className="w-full py-3.5 px-6 rounded-xl shadow-lg shadow-indigo-200 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold transition-all duration-200 transform hover:-translate-y-0.5 mb-4"
              >
                Reload Application
              </button>

              <button 
                onClick={this.toggleDetails}
                className="text-sm font-medium text-gray-400 hover:text-gray-600 transition-colors flex items-center"
              >
                {this.state.showDetails ? 'Hide Technical Details' : 'View Technical Details'}
                <svg className={`ml-1 w-4 h-4 transition-transform ${this.state.showDetails ? 'rotate-180' : ''}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              {/* Technical Details (Collapsible) */}
              {this.state.showDetails && (
                <div className="mt-6 w-full text-left bg-gray-50 rounded-xl p-4 border border-gray-100 animate-fade-in-up">
                  <p className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Error Stack Trace</p>
                  <div className="overflow-auto max-h-40 scrollbar-thin scrollbar-thumb-gray-300">
                    <pre className="text-[10px] font-mono text-rose-800 whitespace-pre-wrap break-all">
                      {this.state.error && this.state.error.toString()}
                      <br/>
                      {this.state.errorInfo && this.state.errorInfo.componentStack}
                    </pre>
                  </div>
                </div>
              )}

            </div>
          </div>

          <div className="mt-8 text-center">
            <p className="text-xs text-gray-400">
              If this persists, please contact support.
            </p>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;