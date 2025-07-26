import useAuthStore from '../store/authStore';
import { useNavigate } from 'react-router-dom';
import ConnectFiCard from './dashboard/ConnectFiCard';

export default function Dashboard() {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen min-w-screen bg-gradient-to-br from-[#0e1238] via-[#172057] to-[#1e2d73] text-white relative isolate">
      {/* Light Grid Texture */}
      <div className="pointer-events-none absolute inset-0 bg-[url('/grid.svg')] bg-repeat opacity-10" />
      
      {/* Aurora Accent */}
      <div className="pointer-events-none absolute left-1/2 top-1/3 -z-10 h-[600px] w-[600px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-lime-400/20 blur-3xl" />

      <main className="max-w-7xl mx-auto py-8 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="rounded-xl backdrop-blur-sm bg-white/5 border border-slate-700/50 shadow-2xl p-6 min-h-[24rem]">
            <h2 className="text-3xl font-bold text-slate-100 mb-6 flex items-center">
              Welcome, <span className="text-lime-400 ml-2">{user?.name || user?.email?.split("@")[0]}!</span>
            </h2>
            <div className="rounded-xl overflow-hidden backdrop-blur-sm bg-white/5 border border-slate-700/50 shadow-lg">
              <ConnectFiCard />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}