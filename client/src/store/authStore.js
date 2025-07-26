import { create } from 'zustand';
import { persist, devtools } from 'zustand/middleware';
import axios from 'axios';
import { BASE_URL } from '../utils/settings';

const useAuthStore = create(
  devtools(
    persist(
    (set, get) => ({
      // State
      user: null,
      token: null,
      tokenType: 'bearer',
      loading: false,
      error: null,
      isAuthenticated: false,

      // Actions
      setLoading: (loading) => set({ loading }),
      
      setError: (error) => set({ error }),
      
      clearError: () => set({ error: null }),

      login: async (email, password, name = 'Alex', navigate = null) => {
        set({ loading: true, error: null });
        
        try {
          const response = await axios.post(`${BASE_URL}/auth/login`, {
            name,
            email,
            password
          });
          
          const { access_token, token_type, ...userData } = response.data.user;
          
          // Set axios default header
          axios.defaults.headers.common['Authorization'] = `${token_type} ${access_token}`;
          
          set({
            user: userData,
            token: access_token,
            tokenType: token_type,
            isAuthenticated: true,
            loading: false,
            error: null
          });
          
          // Navigate to transactions page if navigate function provided
          if (navigate) {
            navigate('/transactions');
          }
          
          return { success: true, user: userData };
        } catch (err) {
          const message = err.response?.data?.detail || 'Login failed';
          set({ 
            error: message, 
            loading: false,
            isAuthenticated: false,
            user: null,
            token: null
          });
          return { success: false, error: message };
        }
      },

      logout: () => {
        // Remove axios default header
        delete axios.defaults.headers.common['Authorization'];
        
        set({
          user: null,
          token: null,
          tokenType: 'bearer',
          isAuthenticated: false,
          error: null
        });
      },

      // Initialize auth state from persisted data
      initializeAuth: () => {
        const { token, tokenType, user, isAuthenticated } = get();
        
        if (token && user && isAuthenticated) {
          // Set axios default header
          axios.defaults.headers.common['Authorization'] = `${tokenType} ${token}`;
        }
      },

      // Update user profile
      updateUser: (userData) => {
        set({ user: { ...get().user, ...userData } });
      },

      // Refresh token if needed (for future implementation)
      refreshToken: async () => {
        // Implement token refresh logic here if your backend supports it
        console.log('Token refresh not implemented yet');
      }
    }),
    {
      name: 'auth-storage', // localStorage key
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        tokenType: state.tokenType,
        isAuthenticated: state.isAuthenticated
      }),
      onRehydrateStorage: () => (state) => {
        // This runs after the persisted state is loaded
        if (state?.token && state?.user) {
          // Restore axios header
          axios.defaults.headers.common['Authorization'] = `${state.tokenType} ${state.token}`;
        }
      }
    },
    { name: 'auth-store' } // devtools name
    )
  )
);

export default useAuthStore;