import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Intercept requests to add the Authorization header
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Intercept responses to handle token expiration (401)
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;
        
        // If 401 Unauthorized and we haven't already retried this request
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            
            try {
                const refresh = localStorage.getItem('refresh');
                if (!refresh) throw new Error('No refresh token');

                // Try to get a new access token
                const res = await axios.post(`${API_URL}/auth/refresh/`, { refresh });
                const { access } = res.data;
                
                // Store new access token
                localStorage.setItem('access', access);
                
                // Update Authorization header and retry original request
                originalRequest.headers.Authorization = `Bearer ${access}`;
                return api(originalRequest);
                
            } catch (err) {
                // If refresh fails (e.g., refresh token expired), log out the user
                localStorage.removeItem('access');
                localStorage.removeItem('refresh');
                window.location.href = '/';
                return Promise.reject(err);
            }
        }
        
        return Promise.reject(error);
    }
);

export default api;
