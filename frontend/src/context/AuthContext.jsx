import { createContext, useContext, useState, useEffect } from 'react';
import api from '../api/axios';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadUser = async () => {
            const token = localStorage.getItem('access');
            if (token) {
                try {
                    const res = await api.get('/auth/profile/');
                    setUser(res.data);
                    setIsAuthenticated(true);
                } catch (error) {
                    console.error('Failed to load user profile.', error);
                    setIsAuthenticated(false);
                    setUser(null);
                    localStorage.removeItem('access');
                    localStorage.removeItem('refresh');
                }
            }
            setLoading(false);
        };

        loadUser();
    }, []);

    const login = async (email, password) => {
        try {
            const res = await api.post('/auth/login/', { email, password });
            localStorage.setItem('access', res.data.access);
            localStorage.setItem('refresh', res.data.refresh);
            
            // Fetch profile after login
            const profileRes = await api.get('/auth/profile/');
            setUser(profileRes.data);
            setIsAuthenticated(true);
            return { success: true };
        } catch (error) {
            return { 
                success: false, 
                message: error.response?.data?.detail || 'Invalid login credentials.',
            };
        }
    };

    const register = async (name, email, password, passwordConfirm) => {
        try {
            const res = await api.post('/auth/register/', { 
                name, 
                email, 
                password,
                password2: passwordConfirm
            });
            return { success: true };
        } catch (error) {
            let errorMsg = 'Failed to register.';
            const errors = error.response?.data;
            if (errors) {
                if (typeof errors === 'object') {
                    errorMsg = Object.values(errors).flat().join(' ');
                } else if (typeof errors === 'string') {
                    errorMsg = errors;
                }
            }
            return { success: false, message: errorMsg };
        }
    };

    const logout = () => {
        localStorage.removeItem('access');
        localStorage.removeItem('refresh');
        setUser(null);
        setIsAuthenticated(false);
    };

    return (
        <AuthContext.Provider value={{ user, setUser, isAuthenticated, login, register, logout, loading }}>
            {!loading && children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
