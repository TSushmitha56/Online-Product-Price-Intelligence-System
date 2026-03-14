import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import PrivateRoute from './routes/PrivateRoute';
import ComparisonBasket from './components/ComparisonBasket';
import CompareOverlay from './components/CompareOverlay';
import { Suspense, lazy } from 'react';

// Pages - Lazy Loaded
const Login = lazy(() => import('./pages/Login'));
const Register = lazy(() => import('./pages/Register'));
const ForgotPassword = lazy(() => import('./pages/ForgotPassword'));
const ResetPassword = lazy(() => import('./pages/ResetPassword'));
const Home = lazy(() => import('./pages/Home'));
const Upload = lazy(() => import('./pages/Upload'));
const Compare = lazy(() => import('./pages/Compare'));
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Wishlist = lazy(() => import('./pages/Wishlist'));
const PriceAlerts = lazy(() => import('./pages/PriceAlerts'));
const Profile = lazy(() => import('./pages/Profile'));

const PageLoader = () => (
  <div className="flex h-screen w-full items-center justify-center bg-gray-50">
    <div className="h-10 w-10 animate-spin rounded-full border-4 border-blue-600 border-t-transparent"></div>
  </div>
);

function App() {
  const [backendStatus, setBackendStatus] = useState({ loading: true, error: null, message: '' });

  // Initial Backend Health Check
  useEffect(() => {
    fetch('http://localhost:8000/api/hello/')
      .then(res => {
        if (!res.ok) throw new Error('Backend not reachable');
        return res.json();
      })
      .then(data => setBackendStatus({ loading: false, error: null, message: data.message }))
      .catch(err => setBackendStatus({ loading: false, error: err.message, message: '' }));
  }, []);

  return (
    <AuthProvider>
      <Router>
        {/* Global Error Banner for Backend Disconnect */}
        {backendStatus.error && (
          <div className="bg-red-600 px-4 py-3 text-white text-center sm:px-6 lg:px-8 z-50 fixed top-0 w-full shadow-md">
            <p className="font-medium">
              System Offline: Backend server is unreachable. Please start the Python Django server.
            </p>
          </div>
        )}

        {/* Note: Router pushes content down if banner exists */}
        <div className={`min-h-screen bg-gray-50 flex flex-col ${backendStatus.error ? 'pt-12' : ''}`}>
          <Suspense fallback={<PageLoader />}>
            <Routes>
              {/* Public Routes */}
              <Route path="/" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/forgot-password" element={<ForgotPassword />} />
              <Route path="/reset-password" element={<ResetPassword />} />

              {/* Protected Application Routes */}
              <Route element={<PrivateRoute />}>
                <Route path="/home" element={<Home />} />
                <Route path="/upload" element={<Upload />} />
                <Route path="/compare" element={<Compare />} />
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/wishlist" element={<Wishlist />} />
                <Route path="/alerts" element={<PriceAlerts />} />
                <Route path="/profile" element={<Profile />} />
              </Route>

              {/* Fallback Catch-all Route */}
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </Suspense>
          <ComparisonBasket />
          <CompareOverlay />
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
