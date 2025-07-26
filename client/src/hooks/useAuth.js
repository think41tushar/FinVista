import useAuthStore from '../store/authStore';

// Custom hook for using auth store directly
export const useAuth = () => {
  return useAuthStore();
};

export default useAuth;