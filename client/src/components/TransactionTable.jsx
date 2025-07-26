import { useState, useRef } from 'react';
import { mockTransactions, getTransactionColumns } from '../data/mockTransactions';
import useTransactionStore from '../store/transactionStore';

const TransactionTable = () => {
  const [transactions] = useState(mockTransactions);
  const columns = getTransactionColumns();
  const tableRef = useRef(null);
  
  const { toggleTransaction, isSelected } = useTransactionStore();

  const formatCurrency = (amount) => {
    if (amount === null || amount === undefined) return '-';
    return `₹${amount.toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  };

  const formatTags = (tags) => {
    return tags.map((tag, index) => (
      <span
        key={index}
        className="tag-chip inline-block px-2 py-1 rounded-full text-xs mr-1 mb-1"
      >
        {tag}
      </span>
    ));
  };

  const ScrollableCell = ({ content, maxHeight = '60px' }) => {
    return (
      <div 
        className="scrollable-cell max-w-full overflow-auto text-sm leading-relaxed pr-2"
        style={{ maxHeight }}
      >
        <div className="whitespace-pre-wrap">
          {content}
        </div>
      </div>
    );
  };

  const renderCellContent = (column, row) => {
    const value = row[column.key];
    
    switch (column.key) {
      case 'date':
        return <span className="table-cell">{formatDate(value)}</span>;
      case 'withdrawn':
      case 'deposited':
      case 'closingBalance':
        return (
          <span className={`font-medium ${
            column.key === 'withdrawn' && value ? 'debit-text' :
            column.key === 'deposited' && value ? 'credit-text' :
            'table-cell'
          }`}>
            {formatCurrency(value)}
          </span>
        );
      case 'type':
        return (
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${
            value === 'Credit' ? 'credit-badge' : 'debit-badge'
          }`}>
            {value}
          </span>
        );
      case 'tags':
        return (
          <div className="flex flex-wrap gap-1">
            {formatTags(value)}
          </div>
        );
      case 'remarks':
      case 'settlements':
        return <ScrollableCell content={value} maxHeight="80px" />;
      default:
        return <span className="table-cell">{value}</span>;
    }
  };

  return (
    <div className="h-full overflow-hidden transaction-table rounded-2xl">
      <div 
        ref={tableRef}
        className="h-full overflow-auto rounded-2xl"
        style={{ padding: '8px 0' }}
      >
        <table className="w-full border-collapse" style={{ tableLayout: 'fixed' }}>
          {/* Table Header */}
          <thead className="sticky top-0 z-20">
            <tr className="table-header">
              {columns.map((column) => (
                <th
                  key={column.key}
                  className="px-4 py-3 text-left text-sm font-semibold border-b table-cell border-r"
                  style={{ width: column.width, minWidth: column.width, maxWidth: column.width }}
                >
                  {column.label}
                </th>
              ))}
            </tr>
          </thead>

          {/* Table Body */}
          <tbody>
            {transactions.map((transaction, index) => (
              <tr
                key={transaction.id}
                className={`table-row border-b ${
                  isSelected(transaction.srNo) ? 'selected' : ''
                }`}
                onClick={() => toggleTransaction(transaction.srNo)}
              >
                {columns.map((column) => (
                  <td
                    key={`${transaction.id}-${column.key}`}
                    className="table-cell px-4 py-3 border-r align-top"
                    style={{ 
                      width: column.width,
                      minWidth: column.width,
                      maxWidth: column.width,
                      height: '80px',
                      overflow: 'hidden'
                    }}
                  >
                    <div className="h-full flex items-start w-full">
                      {renderCellContent(column, transaction)}
                    </div>
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default TransactionTable;