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
    <div className="h-screen flex flex-col" style={{ backgroundColor: 'var(--color-bg-primary)' }}>
      
      <div className="flex flex-1 p-4 gap-4 h-[calc(100vh-88px)]">
        <div className="w-2/3 floating-container">
          <TransactionTable />
        </div>
        
        <div className="w-1/3 floating-container">
          <ChatInterface />
        </div>
      </div>
    </div>
  );
};

export default Transactions;