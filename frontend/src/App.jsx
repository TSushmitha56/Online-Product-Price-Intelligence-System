import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import PrivateRoute from './routes/PrivateRoute';

// Pages
import Login from './pages/Login';
import Home from './pages/Home';
import Upload from './pages/Upload';
import Compare from './pages/Compare';

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
          <Routes>
            {/* Public Login Route */}
            <Route path="/" element={<Login />} />

            {/* Protected Application Routes */}
            <Route element={<PrivateRoute />}>
              <Route path="/home" element={<Home />} />
              <Route path="/upload" element={<Upload />} />
              <Route path="/compare" element={<Compare />} />
            </Route>

            {/* Fallback Catch-all Route */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
