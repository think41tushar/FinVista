import React from 'react'
import useAuthStore from '../../store/authStore';
import { useNavigate } from 'react-router-dom';

const Navbar = () => {

  const { user, logout, isAuthenticated } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };
  return (
    <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold cursor-pointer" onClick={() => navigate('/dashboard')}>FinVista</h1>
            </div>
            <div className="flex items-center space-x-4">
              {isAuthenticated && user && (
                <>
                  <span className="text-gray-700">{user.name || user.email}</span>
                  <button
                    onClick={handleLogout}
                    className="text-gray-500 hover:text-gray-700 px-3 py-2 rounded-md text-sm font-medium cursor-pointer"
                  >
                    Logout
                  </button>
                </>
              )}
            </div>
          </div>
        </div>
      </nav>
  )
}

export default Navbar