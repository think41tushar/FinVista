import React from 'react';

const TransactionSummary = ({ transactions }) => {
  if (!transactions || transactions.length === 0) return null;

  const formatCurrency = (amount) => {
    if (amount === null || amount === undefined) return '₹0.00';
    return `₹${Math.abs(amount).toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-IN', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  };

  return (
    <div className="bg-gray-50 rounded-lg p-3 mb-3 max-h-40 overflow-y-auto">
      <h4 className="text-sm font-semibold text-gray-700 mb-2">
        Selected Transactions ({transactions.length})
      </h4>
      <div className="space-y-2">
        {transactions.map((transaction) => (
          <div key={transaction.id} className="bg-white rounded p-2 border">
            <div className="flex justify-between items-start text-xs">
              <div className="flex-1">
                <p className="font-medium text-gray-800 truncate">
                  {transaction.narration.slice(0, 40)}...
                </p>
                <p className="text-gray-500">
                  {formatDate(transaction.date)} • {transaction.type}
                </p>
              </div>
              <div className="text-right ml-2">
                {transaction.withdrawn > 0 && (
                  <p className="text-red-600 font-medium">
                    -{formatCurrency(transaction.withdrawn)}
                  </p>
                )}
                {transaction.deposit > 0 && (
                  <p className="text-green-600 font-medium">
                    +{formatCurrency(transaction.deposit)}
                  </p>
                )}
                <p className="text-gray-600 text-xs">
                  Bal: {formatCurrency(transaction.closing_balance)}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TransactionSummary;