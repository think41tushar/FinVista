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
    <div className="min-h-screen min-w-screen text-white relative isolate" style={{ backgroundColor: 'var(--color-bg-primary)' }}>
      {/* Light Grid Texture */}
      <div className="pointer-events-none absolute inset-0 bg-[url('/grid.svg')] bg-repeat opacity-10" />
      
      {/* Aurora Accent */}
      <div className="pointer-events-none absolute left-1/2 top-1/3 -z-10 h-[600px] w-[600px] -translate-x-1/2 -translate-y-1/2 rounded-full blur-3xl" style={{ backgroundColor: 'rgba(27, 156, 133, 0.15)' }} />

      <main className="max-w-7xl mx-auto py-8 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="rounded-xl backdrop-blur-sm shadow-2xl p-6 min-h-[24rem]" style={{ backgroundColor: 'var(--color-bg-secondary)', border: '1px solid var(--color-grey-dark)' }}>
            <h2 className="text-3xl font-bold mb-6 flex items-center" style={{ color: 'var(--color-white)' }}>
              Welcome, <span className="ml-2" style={{ color: 'var(--color-accent)' }}>{user?.name || user?.email?.split("@")[0]}!</span>
            </h2>
            <div className="rounded-xl overflow-hidden backdrop-blur-sm shadow-lg" style={{ backgroundColor: 'var(--color-bg-tertiary)', border: '1px solid var(--color-grey-dark)' }}>
              <ConnectFiCard />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}