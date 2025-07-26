import { useRef } from 'react';
import useTransactionStore from '../store/transactionStore';

const TransactionTable = () => {
  const { transactions, loading, error, toggleTransaction, isSelected } = useTransactionStore();
  const tableRef = useRef(null);

  // Define columns based on API response structure
  const columns = [
    { key: 'date', label: 'Date', width: '120px' },
    { key: 'narration', label: 'Description', width: '300px' },
    { key: 'withdrawn', label: 'Withdrawn', width: '120px' },
    { key: 'deposit', label: 'Deposit', width: '120px' },
    { key: 'closing_balance', label: 'Balance', width: '120px' },
    { key: 'type', label: 'Type', width: '80px' },
    { key: 'tags', label: 'Tags', width: '150px' },
    { key: 'remarks', label: 'Remarks', width: '200px' }
  ];

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
      case 'deposit':
      case 'closing_balance':
        return (
          <span className={`font-medium ${
            column.key === 'withdrawn' && value ? 'debit-text' :
            column.key === 'deposit' && value ? 'credit-text' :
            'table-cell'
          }`}>
            {formatCurrency(value)}
          </span>
        );
      case 'type':
        return (
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${
            value === 'BANK' ? 'bg-blue-100 text-blue-800' : 'bg-green-100 text-green-800'
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
        return <ScrollableCell content={value} maxHeight="80px" />;
      case 'narration':
        return <ScrollableCell content={value} maxHeight="80px" />;
      default:
        return <span className="table-cell">{value}</span>;
    }
  };

  if (loading) {
    return (
      <div className="h-full flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2" style={{ borderColor: 'var(--color-accent)' }}></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="h-full flex items-center justify-center">
        <div className="text-red-600">{error}</div>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col overflow-hidden transaction-table rounded-2xl">
      <div 
        ref={tableRef}
        className="flex-1 overflow-auto rounded-2xl min-h-0"
      >
        <table className="w-full border-collapse rounded-2xl" style={{ tableLayout: 'fixed' }}>
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
                  isSelected(transaction.id) ? 'selected' : ''
                }`}
                onClick={() => toggleTransaction(transaction.id)}
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