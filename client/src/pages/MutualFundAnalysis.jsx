import React, { useState, useEffect } from 'react';
import axios from 'axios';
import useAuthStore from '../store/authStore';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  BarElement,
} from 'chart.js';
import { Line, Pie, Bar } from 'react-chartjs-2';
import {
  AlertTriangle
} from 'lucide-react';
import ChatInterface from '../components/common/ChatInterface';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  BarElement
);

const MutualFundAnalysis = () => {
  const [portfolioData, setPortfolioData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { user, isAuthenticated } = useAuthStore();
  // No more tabs, everything will be shown on a single page

  // Helper functions
  const formatCurrency = (amount) => {
    if (amount === null || amount === undefined) return '₹0';
    return `₹${Math.abs(amount).toLocaleString('en-IN', { maximumFractionDigits: 0 })}`;
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-IN', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);

        // Get data from API
        const response = await axios.get('http://localhost:8000/api/mutual-funds/analysis');

        if (response.data.success) {
          setPortfolioData(response.data.data);
        } else {
          throw new Error(response.data.message || 'Failed to fetch portfolio data');
        }
      } catch (err) {
        console.error('Error fetching mutual fund data:', err);
        setError(err.message || 'Failed to fetch portfolio data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-900">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-lime-400 mx-auto mb-6"></div>
          <div className="space-y-2">
            <p className="text-white text-lg font-medium">Loading portfolio analysis...</p>
            <p className="text-slate-400 text-sm">Fetching your investment data</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-900">
        <div className="text-center max-w-md">
          <AlertTriangle className="h-16 w-16 text-red-400 mx-auto mb-4" />
          <p className="text-white text-lg font-medium mb-2">Error loading portfolio data</p>
          <p className="text-red-400 text-sm">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="mt-4 px-6 py-2 bg-lime-400 text-slate-900 rounded-lg font-medium hover:bg-lime-300 transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  // Chart configurations
  const portfolioTimelineChart = {
    labels: portfolioData.portfolioTimeline.map(p => new Date(p.date).toLocaleDateString()),
    datasets: [
      {
        label: 'Portfolio Value',
        data: portfolioData.portfolioTimeline.map(p => p.value),
        borderColor: '#a3e635',
        backgroundColor: 'rgba(163, 230, 53, 0.1)',
        tension: 0.4,
        fill: true,
        pointBackgroundColor: '#a3e635',
        pointBorderColor: '#ffffff',
        pointBorderWidth: 2,
        pointRadius: 6,
        pointHoverRadius: 8,
      },
    ],
  };

  const assetDistributionChart = {
    labels: portfolioData.holdings.map(h => h.name),
    datasets: [
      {
        data: portfolioData.holdings.map(h => h.currentValue),
        backgroundColor: [
          '#a3e635',
          '#bef264',
          '#84cc16',
          '#65a30d',
          '#4d7c0f',
          '#365314',
          '#1a2e05',
        ],
        borderColor: '#ffffff',
        borderWidth: 3,
        hoverBorderWidth: 4,
      },
    ],
  };

  const classificationChart = {
    labels: Object.keys(portfolioData.classification),
    datasets: [
      {
        data: Object.values(portfolioData.classification).map(funds =>
          funds.reduce((sum, fund) => sum + fund.currentValue, 0)
        ),
        backgroundColor: [
          '#a3e635',
          '#bef264',
          '#84cc16',
          '#65a30d',
          '#4d7c0f',
          '#365314',
          '#1a2e05',
        ],
        borderColor: '#ffffff',
        borderWidth: 3,
        hoverBorderWidth: 4,
      },
    ],
  };

  const returnsChart = {
    labels: portfolioData.holdings.map(h => h.name),
    datasets: [
      {
        label: 'Returns (%)',
        data: portfolioData.holdings.map(h => h.returnsPercent),
        backgroundColor: portfolioData.holdings.map(h =>
          h.returnsPercent >= 0 ? '#a3e635' : '#ef4444'
        ),
        borderColor: '#ffffff',
        borderWidth: 2,
        borderRadius: 8,
        borderSkipped: false,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        labels: {
          color: '#ffffff',
          padding: 20,
          font: {
            size: 12,
            weight: '500'
          }
        },
      },
      title: {
        display: false,
      },
      tooltip: {
        backgroundColor: 'rgba(15, 23, 42, 0.9)',
        titleColor: '#ffffff',
        bodyColor: '#ffffff',
        borderColor: '#a3e635',
        borderWidth: 1,
        cornerRadius: 8,
        displayColors: true,
      }
    },
    scales: {
      x: {
        ticks: {
          color: '#94a3b8',
          font: {
            size: 11
          }
        },
        grid: {
          color: 'rgba(148, 163, 184, 0.1)',
          drawBorder: false,
        },
      },
      y: {
        ticks: {
          color: '#94a3b8',
          font: {
            size: 11
          }
        },
        grid: {
          color: 'rgba(148, 163, 184, 0.1)',
          drawBorder: false,
        },
      },
    },
  };

  const pieOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'right',
        labels: {
          color: '#ffffff',
          padding: 15,
          usePointStyle: true,
          pointStyle: 'circle',
          font: {
            size: 11,
            weight: '500'
          }
        },
      },
      tooltip: {
        backgroundColor: 'rgba(15, 23, 42, 0.9)',
        titleColor: '#ffffff',
        bodyColor: '#ffffff',
        borderColor: '#a3e635',
        borderWidth: 1,
        cornerRadius: 8,
        callbacks: {
          label: function (context) {
            const total = context.dataset.data.reduce((a, b) => a + b, 0);
            const percentage = ((context.parsed / total) * 100).toFixed(1);
            return `${context.label}: ₹${context.parsed.toLocaleString('en-IN')} (${percentage}%)`;
          }
        }
      }
    },
  };

  // Use top performers and underperformers directly from API
  const topMovers = portfolioData.topPerformers || [];
  const topLosers = portfolioData.underperformers || [];

  // Sort funds for display in table
  const sortedFunds = [...(portfolioData.holdings || [])].sort((a, b) => b.currentValue - a.currentValue);

  // Get summary data
  const totalReturnsPercent = portfolioData.summary ? portfolioData.summary.totalReturnsPercent : 0;

  return (
    <div className="flex h-screen overflow-hidden p-6 gap-4">
      {/* Scrollable Dashboard Section */}
      <div className="w-5/6 overflow-y-auto h-[calc(90vh-2rem)]">
        <div className="max-w-7xl mx-auto space-y-8 p-6 border border-[1px] border-[var(--color-grey-dark)] rounded-xl">
          <h1 className="text-4xl font-bold text-[var(--color-white)]">Mutual Fund Analysis</h1>

          {/* Portfolio Summary */}
          <div className="rounded-xl p-6 border shadow-lg text-white" style={{ backgroundColor: 'var(--color-bg-secondary)', borderColor: 'var(--color-grey-dark)' }}>
            <h2 className="text-2xl font-semibold mb-4">Portfolio Summary</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {['Current Value', 'Total Invested', 'Total Returns'].map((label, i) => (
                <div key={i} className="rounded-lg p-5 border shadow-sm" style={{ backgroundColor: 'var(--color-bg-tertiary)', borderColor: 'var(--color-grey-dark)' }}>
                  <h3 className="text-[var(--color-grey-light)] text-sm">{label}</h3>
                  {label === 'Total Returns' ? (
                    <div className="flex items-end space-x-2">
                      <p className="text-3xl font-bold">{formatCurrency(portfolioData.summary?.totalReturns || 0)}</p>
                      <p className="text-xl font-medium" style={{ color: totalReturnsPercent >= 0 ? 'var(--color-accent-light)' : '#f87171' }}>
                        {totalReturnsPercent >= 0 ? '+' : ''}{totalReturnsPercent.toFixed(2)}%
                      </p>
                    </div>
                  ) : (
                    <p className="text-3xl font-bold">
                      {formatCurrency(label === 'Current Value' ? portfolioData.summary?.totalValue : portfolioData.summary?.totalInvested || 0)}
                    </p>
                  )}
                </div>
              ))}
            </div>

            {/* Portfolio Growth Chart */}
            <div className="mt-6">
              <h3 className="text-lg font-medium mb-3 text-[var(--color-grey-light)]">Portfolio Growth</h3>
              <div className="h-64 w-full">
                <Line data={portfolioTimelineChart} options={chartOptions} />
              </div>
            </div>
          </div>

          {/* Holdings Table */}
          <div className="rounded-xl p-6 border shadow-lg text-white" style={{ backgroundColor: 'var(--color-bg-secondary)', borderColor: 'var(--color-grey-dark)' }}>
            <h2 className="text-2xl font-bold mb-4 text-[var(--color-white)]">Holdings</h2>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y" style={{ borderColor: 'var(--color-grey-dark)' }}>
                <thead>
                  <tr>
                    {['Fund', 'Units', 'Current Value', 'Invested', 'Returns'].map((h, i) => (
                      <th key={i} className="px-4 py-3 text-left text-sm font-medium uppercase tracking-wider text-[var(--color-grey-light)]">
                        {h}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y" style={{ borderColor: 'var(--color-grey-dark)' }}>
                  {sortedFunds.map((fund) => {
                    const returns = fund.returns || 0;
                    const percent = fund.returns_percent || fund.returnsPercent || 0;
                    return (
                      <tr key={fund.isin} className="hover:bg-opacity-20 transition-colors" style={{ backgroundColor: 'var(--color-bg-tertiary)' }}>
                        <td className="px-4 py-3 whitespace-nowrap">
                          <div>
                            <div className="font-medium">{fund.name}</div>
                            <div className="text-sm truncate max-w-[200px] text-[var(--color-grey-medium)]">{fund.full_name || fund.fullName}</div>
                          </div>
                        </td>
                        <td className="px-4 py-3 text-right text-[var(--color-grey-light)] whitespace-nowrap">{fund.total_units?.toFixed(2)}</td>
                        <td className="px-4 py-3 text-right whitespace-nowrap">{formatCurrency(fund.current_value)}</td>
                        <td className="px-4 py-3 text-right text-[var(--color-grey-light)] whitespace-nowrap">{formatCurrency(fund.total_invested)}</td>
                        <td className="px-4 py-3 text-right whitespace-nowrap">
                          <div className="flex flex-col items-end">
                            <span className="font-medium" style={{ color: returns >= 0 ? 'var(--color-accent-light)' : '#f87171' }}>
                              {returns >= 0 ? '+' : ''}{formatCurrency(Math.abs(returns))}
                            </span>
                            <span className="text-xs" style={{ color: percent >= 0 ? 'var(--color-accent-light)' : '#f87171' }}>
                              {percent >= 0 ? '+' : ''}{percent.toFixed(2)}%
                            </span>
                          </div>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>

          {/* Performance Bar Chart */}
          <div className="bg-[var(--color-bg-secondary)] rounded-xl p-6 border border-[var(--color-grey-dark)] shadow-lg text-white">
            <h2 className="text-2xl font-semibold mb-4">Performance</h2>
            <div className="h-80 w-full">
              <Bar data={returnsChart} options={chartOptions} />
            </div>
          </div>

          {/* Allocation Section */}
          <div className="bg-[var(--color-bg-secondary)] rounded-xl p-6 border border-[var(--color-grey-dark)] shadow-lg text-white">
            <h2 className="text-2xl font-semibold mb-6">Allocation</h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              {/* Top Performers */}
              <div>
                <h3 className="text-xl font-medium mb-4 text-[var(--color-grey-light)]">Top Performers</h3>
                <ul className="space-y-4">
                  {topMovers.map((fund) => (
                    <li key={fund.isin} className="bg-[var(--color-bg-tertiary)] rounded-lg p-4 border border-[var(--color-accent-light)]/20">
                      <div className="flex justify-between">
                        <div>
                          <h4 className="font-medium">{fund.name}</h4>
                          <p className="text-sm text-[var(--color-grey-light)]">{fund.full_name}</p>
                        </div>
                        <div className="text-right">
                          <p className="text-[var(--color-accent-light)] font-bold text-lg">
                            +{(fund.returns_percent || 0).toFixed(2)}%
                          </p>
                          <p className="text-[var(--color-accent-light)]/80 text-sm">
                            +{formatCurrency(fund.returns || 0)}
                          </p>
                        </div>
                      </div>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Underperformers */}
              <div>
                <h3 className="text-xl font-medium mb-4 text-[var(--color-grey-light)]">Underperformers</h3>
                <ul className="space-y-4">
                  {topLosers.map((fund) => (
                    <li key={fund.isin} className="bg-[var(--color-bg-tertiary)] rounded-lg p-4 border border-red-400/20">
                      <div className="flex justify-between">
                        <div>
                          <h4 className="font-medium">{fund.name}</h4>
                          <p className="text-sm text-[var(--color-grey-light)]">{fund.full_name}</p>
                        </div>
                        <div className="text-right">
                          <p className="text-red-400 font-bold text-lg">
                            {(fund.returns_percent || 0).toFixed(2)}%
                          </p>
                          <p className="text-red-400/80 text-sm">
                            {formatCurrency(fund.returns || 0)}
                          </p>
                        </div>
                      </div>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Category Allocation */}
            <div className="mt-8">
              <h3 className="text-xl font-medium mb-4 text-[var(--color-grey-light)]">Category Allocation</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="h-64">
                  <Pie data={classificationChart} options={pieOptions} />
                </div>
                <div className="space-y-3">
                  {Object.keys(portfolioData.classification || {}).map((category) => {
                    const funds = portfolioData.classification[category];
                    const categoryValue = funds.reduce((sum, fund) => sum + (fund.current_value || 0), 0);
                    const percent = ((categoryValue / (portfolioData.summary?.totalValue || 1)) * 100).toFixed(1);
                    return (
                      <div key={category} className="flex justify-between items-center p-3 rounded-lg bg-[var(--color-bg-tertiary)]">
                        <span className="text-[var(--color-grey-light)]">{category}</span>
                        <div className="text-right">
                          <span className="text-white font-medium">{formatCurrency(categoryValue)}</span>
                          <span className="text-[var(--color-grey-medium)] text-sm ml-2">({percent}%)</span>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div className='w-2/6 border border-[var(--color-grey-dark)] rounded-xl p-1 bg-[var(--color-bg-secondary)] h-[calc(90vh-2rem)] flex flex-col'>
      <ChatInterface />
      </div>
    </div>
  );

};

export default MutualFundAnalysis;