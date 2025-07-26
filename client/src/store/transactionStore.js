import { create } from 'zustand';

const useTransactionStore = create((set, get) => ({
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
  
  // Check if a transaction is selected
  isSelected: (srNo) => {
    const { selectedTransactions } = get();
    return selectedTransactions.has(srNo);
  },
  
  // Get count of selected transactions
  getSelectedCount: () => {
    const { selectedTransactions } = get();
    return selectedTransactions.size;
  }
}));

export default useTransactionStore;