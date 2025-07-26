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
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-[#0e1238] via-[#172057] to-[#1e2d73] text-white relative isolate">
      {/* Light Grid Texture */}
      <div className="pointer-events-none absolute inset-0 bg-[url('/grid.svg')] bg-repeat opacity-10" />
      
      {/* Aurora Accent */}
      <div className="pointer-events-none absolute left-1/3 top-1/3 -z-10 h-[500px] w-[500px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-lime-400/20 blur-3xl" />
      
      <div className="flex flex-1 p-4 gap-4 h-[calc(100vh-64px)]">
        <div className="w-2/3 rounded-xl backdrop-blur-sm bg-white/5 border border-slate-700/50 shadow-2xl p-4 overflow-hidden">
          <TransactionTable />
        </div>
        
        <div className="w-1/3 rounded-xl backdrop-blur-sm bg-white/5 border border-slate-700/50 shadow-2xl">
          <ChatInterface />
        </div>
      </div>
    </div>
  );
};

export default Transactions;