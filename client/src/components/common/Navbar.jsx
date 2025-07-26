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
    <nav 
      className="text-white shadow-lg border-b" 
      style={{ 
        backgroundColor: 'var(--color-bg-primary)', 
        borderColor: 'var(--color-grey-dark)' 
      }}
    >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold cursor-pointer" style={{ color: 'var(--color-accent)' }} onClick={() => navigate('/')}>FinVista</h1>
            </div>
            <div className="flex items-center space-x-4">
              {isAuthenticated && user && (
                <>
                  <span style={{ color: 'var(--color-cream)' }}>{user.name || user.email}</span>
                  <button
                    onClick={handleLogout}
                    className="px-3 py-2 rounded-md font-medium cursor-pointer transition-colors"
                    style={{ 
                      color: 'var(--color-grey-light)',
                      ':hover': { color: 'var(--color-accent)' }
                    }}
                    onMouseEnter={(e) => e.target.style.color = 'var(--color-accent)'}
                    onMouseLeave={(e) => e.target.style.color = 'var(--color-grey-light)'}
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