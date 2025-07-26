import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import axios from 'axios';
import { BASE_URL } from '../utils/settings';

const useTransactionStore = create(
  devtools(
    (set, get) => ({
  // State
  transactions: [],
  relations: [],
  loading: false,
  error: null,
  selectedTransactions: new Set(),
  
  // Add a transaction to selection
  selectTransaction: (srNo) => set((state) => {
    const newSelected = new Set(state.selectedTransactions);
    newSelected.add(srNo);
    return { selectedTransactions: newSelected };
  }),
  
  // Remove a transaction from selection
  deselectTransaction: (srNo) => set((state) => {
    const newSelected = new Set(state.selectedTransactions);
    newSelected.delete(srNo);
    return { selectedTransactions: newSelected };
  }),
  
  // Toggle transaction selection
  toggleTransaction: (srNo) => {
    const { selectedTransactions, selectTransaction, deselectTransaction } = get();
    if (selectedTransactions.has(srNo)) {
      deselectTransaction(srNo);
    } else {
      selectTransaction(srNo);
    }
  },
  
  // Clear all selections
  clearSelection: () => set({ selectedTransactions: new Set() }),
  
  // Get selected transaction numbers as sorted array
  getSelectedArray: () => {
    const { selectedTransactions } = get();
    return Array.from(selectedTransactions).sort((a, b) => a - b);
  },

  // Get full selected transaction objects
  getSelectedTransactions: () => {
    const { selectedTransactions, transactions } = get();
    return transactions.filter(transaction => 
      selectedTransactions.has(transaction.id)
    );
  },
  
  // Check if a transaction is selected
  isSelected: (srNo) => {
    const { selectedTransactions } = get();
    return selectedTransactions.has(srNo);
  },
  
  // Get count of selected transactions
  getSelectedCount: () => {
    const { selectedTransactions } = get();
    return selectedTransactions.size;
  },

  // API Actions
  setLoading: (loading) => set({ loading }),
  
  setError: (error) => set({ error }),
  
  clearError: () => set({ error: null }),

  // Fetch transactions by user ID
  fetchTransactionsByUserId: async (userId) => {
    set({ loading: true, error: null });
    
    try {
      const response = await axios.get(`${BASE_URL}/transactions/user/${userId}`);
      set({ 
        transactions: response.data,
        loading: false 
      });
      return { success: true, data: response.data };
    } catch (err) {
      const message = err.response?.data?.detail || 'Failed to fetch transactions';
      set({ 
        error: message, 
        loading: false 
      });
      return { success: false, error: message };
    }
  },

  // Fetch relations by user ID
  fetchRelationsByUserId: async (userId) => {
    set({ loading: true, error: null });
    
    try {
      const response = await axios.get(`${BASE_URL}/relations/user/${userId}`);
      set({ 
        relations: response.data,
        loading: false 
      });
      return { success: true, data: response.data };
    } catch (err) {
      const message = err.response?.data?.detail || 'Failed to fetch relations';
      set({ 
        error: message, 
        loading: false 
      });
      return { success: false, error: message };
    }
  },

  // Fetch both transactions and relations
  fetchUserData: async (userId) => {
    set({ loading: true, error: null });
    
    try {
      const [transactionsResult, relationsResult] = await Promise.allSettled([
        axios.get(`${BASE_URL}/transactions/user/${userId}`),
        axios.get(`${BASE_URL}/relations/user/${userId}`)
      ]);

      const transactions = transactionsResult.status === 'fulfilled' 
        ? transactionsResult.value.data 
        : [];
      
      const relations = relationsResult.status === 'fulfilled' 
        ? relationsResult.value.data 
        : [];

      set({ 
        transactions,
        relations,
        loading: false 
      });

      return { 
        success: true, 
        data: { transactions, relations },
        errors: {
          transactions: transactionsResult.status === 'rejected' ? transactionsResult.reason : null,
          relations: relationsResult.status === 'rejected' ? relationsResult.reason : null
        }
      };
    } catch (err) {
      const message = 'Failed to fetch user data';
      set({ 
        error: message, 
        loading: false 
      });
      return { success: false, error: message };
    }
  },

  // Query AI with context and user message
  queryAI: async (query, selectedTransactionIds = []) => {
    set({ loading: true, error: null });
    
    try {
      // Get full transaction objects for the selected IDs
      const { transactions } = get();
      const selectedTransactions = transactions.filter(transaction => 
        selectedTransactionIds.includes(transaction.id)
      );

      // Prepare the query with transaction context
      let contextualQuery = query;
      if (selectedTransactions.length > 0) {
        const transactionContext = selectedTransactions.map(t => ({
          id: t.id,
          date: t.date,
          narration: t.narration,
          withdrawn: t.withdrawn,
          deposit: t.deposit,
          closing_balance: t.closing_balance,
          type: t.type,
          tags: t.tags,
          remarks: t.remarks
        }));
        
        contextualQuery = `Context - Selected Transactions: ${JSON.stringify(transactionContext)}\n\nUser Query: ${query}`;
      }

      const response = await axios.post(`${BASE_URL}/ai/query`, {
        query: contextualQuery
      });

      // Log the response for debugging
      console.log('AI Query Response:', response.data);

      set({ loading: false });
      return { 
        success: true, 
        response: response.data.response,
        selectedTransactions 
      };
    } catch (err) {
      const message = err.response?.data?.detail || 'AI query failed';
      set({ 
        error: message, 
        loading: false 
      });
      return { success: false, error: message };
    }
  }
}),
{ name: 'transaction-store' } // devtools name
));

export default useTransactionStore;