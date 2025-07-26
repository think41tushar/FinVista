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
    <div className='relative isolate flex w-full min-h-screen items-center justify-center bg-gradient-to-br from-[#0e1238] via-[#172057] to-[#1e2d73] text-white'>
      {/* Light Grid Texture */}
      <div className="pointer-events-none absolute inset-0 bg-[url('/grid.svg')] bg-repeat opacity-10" />
      
      {/* Aurora Accent */}
      <div className="pointer-events-none absolute left-1/2 top-1/2 -z-10 h-[400px] w-[400px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-lime-400/20 blur-3xl" />
      
      <div className="w-full max-w-md px-8 py-10 mx-4 rounded-xl backdrop-blur-sm bg-white/5 border border-slate-700/50 shadow-2xl">
        <div className="w-full space-y-8">
          <div className="text-center">
            <h1 className="text-4xl font-bold mb-1 text-lime-400">FinVista</h1>
            <h2 className="text-2xl font-bold mb-3 text-slate-100">
              Sign in to your account
            </h2>
            <p className="text-sm opacity-80 text-slate-300">
              Don't have an account? Just enter your details to register
            </p>
          </div>
          
          <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
            {error && (
              <div className="rounded-md p-4 bg-red-400/10 border border-red-400/30">
                <div className="text-sm text-red-300">{error}</div>
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
                  className="w-full pl-4 pr-3 py-3 rounded-xl border bg-slate-800/40 text-slate-100 border-slate-700/50 transition-all focus:ring-2 focus:ring-lime-400/30 focus:border-lime-400 focus:outline-none"
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
                  className="w-full pl-4 pr-3 py-3 rounded-xl border bg-slate-800/40 text-slate-100 border-slate-700/50 transition-all focus:ring-2 focus:ring-lime-400/30 focus:border-lime-400 focus:outline-none"
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
                  className="w-full pl-4 pr-3 py-3 rounded-xl border bg-slate-800/40 text-slate-100 border-slate-700/50 transition-all focus:ring-2 focus:ring-lime-400/30 focus:border-lime-400 focus:outline-none"
                  placeholder="Password"
                />
              </div>
            </div>

            <div>
              <button
                type="submit"
                disabled={loading}
                className="group relative w-full flex justify-center items-center py-3 px-4 border border-transparent text-sm font-medium rounded-xl bg-lime-400 text-slate-900 shadow hover:bg-lime-300 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-lime-400 transition-all hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed"
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