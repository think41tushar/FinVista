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
  getRelatedTransactionsRecursively: (transactionId, visited = new Set()) => {
    const { relations } = get();
    
    // Avoid infinite loops
    if (visited.has(transactionId)) {
      return new Set();
    }
    visited.add(transactionId);
    
    const relatedIds = new Set([transactionId]);
    
    // Find the relation for this transaction
    const relation = relations.find(rel => 
      rel.primary_transaction === transactionId || 
      rel.related_transactions.includes(transactionId)
    );
    
    if (relation) {
      // Add all related transactions
      relation.related_transactions.forEach(relId => {
        relatedIds.add(relId);
        // Recursively get related transactions
        const nestedRelated = get().getRelatedTransactionsRecursively(relId, visited);
        nestedRelated.forEach(id => relatedIds.add(id));
      });
    }
    
    return relatedIds;
  },

  isTransactionRelated: (transactionId) => {
    const { relations } = get();
    
    // Check if this transaction appears in any relation's related_transactions
    return relations.some(relation => 
      relation.related_transactions.includes(transactionId)
    );
  },

  // Create a map of transaction types for better performance
  getTransactionTypesMap: () => {
    const { relations, transactions } = get();
    const typesMap = new Map();
    
    // First, set all transactions as direct
    transactions.forEach(transaction => {
      typesMap.set(transaction.id, 'direct');
    });
    
    // Then mark all related transactions
    relations.forEach(relation => {
      relation.related_transactions.forEach(transId => {
        typesMap.set(transId, 'related');
      });
    });
    
    return typesMap;
  },

  // Get settlement notes map
  getSettlementNotesMap: () => {
    const { relations } = get();
    const notesMap = new Map();
    
    relations.forEach(relation => {
      if (relation.settlement_notes) {
        // Add settlement note for all related transactions
        relation.related_transactions.forEach(transId => {
          notesMap.set(transId, relation.settlement_notes);
        });
      }
    });
    
    return notesMap;
  },

  // Add a transaction and all its related transactions to selection
  selectTransaction: (transactionId) => set((state) => {
    const { getRelatedTransactionsRecursively } = get();
    const newSelected = new Set(state.selectedTransactions);
    
    // Get all related transactions recursively
    const relatedIds = getRelatedTransactionsRecursively(transactionId);
    
    // Add all related transactions to selection
    relatedIds.forEach(id => newSelected.add(id));
    
    return { selectedTransactions: newSelected };
  }),
  
  deselectTransaction: (transactionId) => set((state) => {
    const { getRelatedTransactionsRecursively } = get();
    const newSelected = new Set(state.selectedTransactions);
    
    // Get all related transactions recursively
    const relatedIds = getRelatedTransactionsRecursively(transactionId);
    
    // Remove all related transactions from selection
    relatedIds.forEach(id => newSelected.delete(id));
    
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
  queryAI: async (query, selectedTransactionIds = [], userId = null) => {
    // Don't set loading for AI queries - this prevents UI crashes
    set({ error: null });
    
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

      const requestBody = {
        query: contextualQuery
      };
      
      // Only add user_id if it's provided
      if (userId) {
        requestBody.user_id = userId;
      }

      const response = await axios.post(`${BASE_URL}/ai/query`, requestBody);

      // Log the response for debugging
      console.log('AI Query Response:', response.data);

      // Handle different response structures and extract actual text content
      let aiResponse;
      
      // Check if response.data has the structure {status: 'success', response: {...}}
      if (response.data.status === 'success' && response.data.response) {
        if (typeof response.data.response === 'object') {
          // Extract the actual text from the response object
          if (response.data.response.response) {
            // Structure: {status: 'success', response: {response: "actual text"}}
            aiResponse = response.data.response.response;
          } else if (response.data.response.text) {
            // Structure: {status: 'success', response: {text: "actual text"}}
            aiResponse = response.data.response.text;
          } else if (response.data.response.message) {
            // Structure: {status: 'success', response: {message: "actual text"}}
            aiResponse = response.data.response.message;
          } else {
            // If no known text field, show the first string value found
            const values = Object.values(response.data.response);
            const textValue = values.find(val => typeof val === 'string');
            aiResponse = textValue || JSON.stringify(response.data.response, null, 2);
          }
        } else {
          aiResponse = response.data.response;
        }
      } else if (response.data.response) {
        // Handle case where response is directly in response.data.response
        if (typeof response.data.response === 'object') {
          // Extract text from nested structure
          if (response.data.response.response) {
            aiResponse = response.data.response.response;
          } else if (response.data.response.text) {
            aiResponse = response.data.response.text;
          } else {
            const values = Object.values(response.data.response);
            const textValue = values.find(val => typeof val === 'string');
            aiResponse = textValue || JSON.stringify(response.data.response, null, 2);
          }
        } else {
          aiResponse = response.data.response;
        }
      } else {
        // Fallback - show the entire response
        aiResponse = JSON.stringify(response.data, null, 2);
      }
      
      // Clean up the response text (remove extra quotes and escape characters)
      if (typeof aiResponse === 'string') {
        aiResponse = aiResponse.replace(/\\n/g, '\n').replace(/\\"/g, '"');
      }

      return { 
        success: true, 
        response: aiResponse,
        selectedTransactions 
      };
    } catch (err) {
      const message = err.response?.data?.detail || 'AI query failed';
      set({ error: message });
      return { success: false, error: message };
    }
  }
}),
{ name: 'transaction-store' } // devtools name
));

export default useTransactionStore;