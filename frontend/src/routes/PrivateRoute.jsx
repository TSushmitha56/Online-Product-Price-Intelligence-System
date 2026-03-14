import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const PrivateRoute = () => {
    const { isAuthenticated } = useAuth();

    // If unauthorized, return to login page
    if (!isAuthenticated) {
        return <Navigate to="/" replace />;
    }

    // If authorized, render child routes
    return <Outlet />;
};

export default PrivateRoute;
