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
    <nav className="bg-gradient-to-br from-[#0e1238] via-[#172057] to-[#1e2d73] text-white shadow-lg border-b border-slate-700/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold cursor-pointer text-lime-400" onClick={() => navigate('/')}>FinVista</h1>
            </div>
            <div className="flex items-center space-x-4">
              {isAuthenticated && user && (
                <>
                  <span className="text-slate-200">{user.name || user.email}</span>
                  <button
                    onClick={handleLogout}
                    className="text-slate-300 hover:text-lime-400 px-3 py-2 rounded-md text-sm font-medium cursor-pointer transition-colors"
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