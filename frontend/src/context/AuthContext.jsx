import { createContext, useState, useEffect, useCallback } from 'react';
import toast from 'react-hot-toast';
import authApi from '../api/authApi';

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('auth_token'));
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Load user from token on mount
  useEffect(() => {
    const initAuth = async () => {
      const storedToken = localStorage.getItem('auth_token');
      if (storedToken) {
        try {
          const profile = await authApi.getProfile();
          setUser(profile.user || profile);
          setToken(storedToken);
        } catch {
          // Token invalid — clean up
          localStorage.removeItem('auth_token');
          localStorage.removeItem('user');
          setToken(null);
          setUser(null);
        }
      }
      setLoading(false);
    };
    initAuth();
  }, []);

  const login = useCallback(async (email, password) => {
    setError(null);
    try {
      const data = await authApi.login(email, password);
      const authToken = data.access_token || data.token;
      const userData = data.user || { email };

      localStorage.setItem('auth_token', authToken);
      localStorage.setItem('user', JSON.stringify(userData));
      setToken(authToken);
      setUser(userData);
      toast.success('Successfully logged in!');
      return data;
    } catch (err) {
      const message = err.response?.data?.detail || err.response?.data?.message || 'Login failed';
      toast.error(message);
      setError(message);
      throw new Error(message);
    }
  }, []);

  const register = useCallback(async (name, email, password) => {
    setError(null);
    try {
      const data = await authApi.register(name, email, password);
      const authToken = data.access_token || data.token;
      const userData = data.user || { name, email };

      if (authToken) {
        // We do not auto-login on registration based on requirements
        // localStorage.setItem('auth_token', authToken);
        // localStorage.setItem('user', JSON.stringify(userData));
        // setToken(authToken);
        // setUser(userData);
      }
      toast.success('Account created successfully!');
      return data;
    } catch (err) {
      const message = err.response?.data?.detail || err.response?.data?.message || 'Registration failed';
      toast.error(message);
      setError(message);
      throw new Error(message);
    }
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user');
    setToken(null);
    setUser(null);
    setError(null);
    toast.success('Logged out successfully');
  }, []);

  const clearError = useCallback(() => setError(null), []);

  const isAuthenticated = !!token && !!user;

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        loading,
        error,
        isAuthenticated,
        login,
        register,
        logout,
        clearError,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export default AuthContext;
