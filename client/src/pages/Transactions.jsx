import { useEffect } from 'react';
import Navbar from '../components/common/Navbar';
import ChatInterface from '../components/common/ChatInterface';
import TransactionTable from '../components/TransactionTable';
import useAuthStore from '../store/authStore';
import useTransactionStore from '../store/transactionStore';

const Transactions = () => {
  const { user, isAuthenticated } = useAuthStore();
  const { fetchUserData, loading, error } = useTransactionStore();

  useEffect(() => {
    if (isAuthenticated && user?.id) {
      // Fetch both transactions and relations when component mounts
      fetchUserData(user.id);
    }
  }, [user?.id, isAuthenticated, fetchUserData]);

  return (
    <div className="h-screen flex flex-col text-white relative overflow-hidden" style={{ backgroundColor: 'var(--color-bg-primary)' }}>
      {/* Light Grid Texture */}
      <div className="pointer-events-none absolute inset-0 bg-[url('/grid.svg')] bg-repeat opacity-10" />
      
      {/* Aurora Accent */}
      <div className="pointer-events-none absolute left-1/3 top-1/3 -z-10 h-[500px] w-[500px] -translate-x-1/2 -translate-y-1/2 rounded-full blur-3xl" style={{ backgroundColor: 'rgba(27, 156, 133, 0.15)' }} />
      
      <div className="flex flex-1 p-4 gap-4 min-h-0">
        <div className="w-2/3 rounded-xl backdrop-blur-sm shadow-2xl p-4 flex flex-col min-h-0" style={{ backgroundColor: 'var(--color-bg-secondary)', border: '1px solid var(--color-grey-dark)' }}>
          <TransactionTable />
        </div>
        
        <div className="w-1/3 rounded-xl backdrop-blur-sm shadow-2xl flex flex-col min-h-0" style={{ backgroundColor: 'var(--color-bg-secondary)', border: '1px solid var(--color-grey-dark)' }}>
          <ChatInterface />
        </div>
      </div>
    </div>
  );
};

export default Transactions;