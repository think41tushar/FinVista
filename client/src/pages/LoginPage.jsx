import { useState, useEffect } from 'react';
import useAuthStore from '../store/authStore';
import { useNavigate } from 'react-router-dom';

export default function Login() {
  const [email, setEmail] = useState('test@example.com');
  const [password, setPassword] = useState('password123');
  const [name, setName] = useState('');
  const { login, error, loading } = useAuthStore();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const result = await login(email, password, name || 'Alex', navigate);
    
    if (result.success) {
      // Navigation is handled in the login function
      console.log('Login successful');
    }
  };

  // Background color animation effect
  useEffect(() => {
    document.body.style.backgroundColor = 'var(--color-bg-primary)';
    return () => {
      document.body.style.backgroundColor = '';
    };
  }, []);

  return (
    <div className='relative isolate flex w-full min-h-screen items-center justify-center text-white' style={{ backgroundColor: 'var(--color-bg-primary)' }}>
      {/* Light Grid Texture */}
      <div className="pointer-events-none absolute inset-0 bg-[url('/grid.svg')] bg-repeat opacity-10" />
      
      {/* Aurora Accent */}
      <div className="pointer-events-none absolute left-1/2 top-1/2 -z-10 h-[400px] w-[400px] -translate-x-1/2 -translate-y-1/2 rounded-full blur-3xl" style={{ backgroundColor: 'rgba(27, 156, 133, 0.15)' }} />
      
      <div className="w-full max-w-md px-8 py-10 mx-4 rounded-xl backdrop-blur-sm shadow-2xl" style={{ backgroundColor: 'var(--color-bg-secondary)', border: '1px solid var(--color-grey-dark)' }}>
        <div className="w-full space-y-8">
          <div className="text-center">
            <h1 className="text-4xl font-bold mb-1" style={{ color: 'var(--color-accent)' }}>FinVista</h1>
            <h2 className="text-2xl font-bold mb-3" style={{ color: 'var(--color-white)' }}>
              Sign in to your account
            </h2>
            <p className="text-sm opacity-80" style={{ color: 'var(--color-grey-light)' }}>
              Don't have an account? Just enter your details to register
            </p>
          </div>
          
          <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
            {error && (
              <div className="rounded-md p-4" style={{ backgroundColor: 'rgba(248, 113, 113, 0.1)', border: '1px solid rgba(248, 113, 113, 0.3)' }}>
                <div className="text-sm" style={{ color: '#f87171' }}>{error}</div>
              </div>
            )}
            
            <div className="space-y-4">
              <div className="relative">
                <input
                  id="name"
                  name="name"
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full pl-4 pr-3 py-3 rounded-xl border transition-all focus:ring-2 focus:outline-none"
                  style={{
                    backgroundColor: 'var(--color-bg-tertiary)',
                    color: 'var(--color-white)',
                    borderColor: 'var(--color-grey-dark)'
                  }}
                  onFocus={(e) => {
                    e.target.style.borderColor = 'var(--color-accent)';
                    e.target.style.boxShadow = '0 0 0 2px rgba(27, 156, 133, 0.2)';
                  }}
                  onBlur={(e) => {
                    e.target.style.borderColor = 'var(--color-grey-dark)';
                    e.target.style.boxShadow = 'none';
                  }}
                  placeholder="Name (optional - defaults to Alex)"
                />
              </div>
              
              <div className="relative">
                <input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full pl-4 pr-3 py-3 rounded-xl border transition-all focus:ring-2 focus:outline-none"
                  style={{
                    backgroundColor: 'var(--color-bg-tertiary)',
                    color: 'var(--color-white)',
                    borderColor: 'var(--color-grey-dark)'
                  }}
                  onFocus={(e) => {
                    e.target.style.borderColor = 'var(--color-accent)';
                    e.target.style.boxShadow = '0 0 0 2px rgba(27, 156, 133, 0.2)';
                  }}
                  onBlur={(e) => {
                    e.target.style.borderColor = 'var(--color-grey-dark)';
                    e.target.style.boxShadow = 'none';
                  }}
                  placeholder="Email address"
                />
              </div>
              
              <div className="relative">
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full pl-4 pr-3 py-3 rounded-xl border transition-all focus:ring-2 focus:outline-none"
                  style={{
                    backgroundColor: 'var(--color-bg-tertiary)',
                    color: 'var(--color-white)',
                    borderColor: 'var(--color-grey-dark)'
                  }}
                  onFocus={(e) => {
                    e.target.style.borderColor = 'var(--color-accent)';
                    e.target.style.boxShadow = '0 0 0 2px rgba(27, 156, 133, 0.2)';
                  }}
                  onBlur={(e) => {
                    e.target.style.borderColor = 'var(--color-grey-dark)';
                    e.target.style.boxShadow = 'none';
                  }}
                  placeholder="Password"
                />
              </div>
            </div>

            <div>
              <button
                type="submit"
                disabled={loading}
                className="group relative w-full flex justify-center items-center py-3 px-4 border border-transparent text-sm font-medium rounded-xl shadow transition-all hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed"
                style={{
                  backgroundColor: 'var(--color-accent)',
                  color: 'var(--color-white)'
                }}
                onMouseEnter={(e) => e.target.style.backgroundColor = 'var(--color-accent-light)'}
                onMouseLeave={(e) => e.target.style.backgroundColor = 'var(--color-accent)'}
                onFocus={(e) => {
                  e.target.style.outline = '2px solid var(--color-accent)';
                  e.target.style.outlineOffset = '2px';
                }}
                onBlur={(e) => {
                  e.target.style.outline = 'none';
                  e.target.style.outlineOffset = '0';
                }}
              >
                {loading ? 'Processing...' : 'Sign in / Register'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}