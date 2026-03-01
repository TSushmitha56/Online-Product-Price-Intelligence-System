import { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [loading, setLoading] = useState(true);

    // Check initial state from localStorage
    useEffect(() => {
        const storedAuth = localStorage.getItem('isAuthenticated');
        if (storedAuth === 'true') {
            setIsAuthenticated(true);
        }
        setLoading(false);
    }, []);

    const login = (email, password) => {
        // Hardcoded credentials as per requirements
        if (email === 'admin@example.com' && password === 'admin123') {
            setIsAuthenticated(true);
            localStorage.setItem('isAuthenticated', 'true');
            return true;
        }
        return false;
    };

    const logout = () => {
        setIsAuthenticated(false);
        localStorage.removeItem('isAuthenticated');
    };

    return (
        <AuthContext.Provider value={{ isAuthenticated, login, logout, loading }}>
            {!loading && children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
