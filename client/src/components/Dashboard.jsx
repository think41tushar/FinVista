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
    <div className="min-h-screen min-w-screen bg-gray-100">

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="border-4 border-dashed border-gray-200 rounded-lg h-96 p-4">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              Welcome, {user?.name || user?.email?.split("@")[0]}!
            </h2>
            <div className="bg-white overflow-hidden shadow rounded-lg">
              <ConnectFiCard />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}