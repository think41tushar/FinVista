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
    <div className="min-h-screen min-w-screen relative" style={{ backgroundColor: 'var(--color-bg-primary)' }}>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="border-4 border-dashed border-gray-200 rounded-lg h-96 p-4" style={{ backgroundColor: 'var(--color-bg-secondary)' }}>
            <h2 className="text-2xl font-bold text-gray-900 mb-4" style={{ color: 'var(--color-white)' }}>
              Welcome, {user?.name || user?.email?.split("@")[0]}!
            </h2>
            <div className="bg-white overflow-hidden shadow rounded-lg"  style={{ backgroundColor: 'var(--color-bg-tertiary)', border: '1px solid var(--color-grey-dark)' }}>
              <ConnectFiCard />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}