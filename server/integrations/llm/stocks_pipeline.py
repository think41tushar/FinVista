import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging

# Configure logging
logger = logging.getLogger(__name__)

@dataclass
class StockHolding:
    """Represents a stock holding with calculated metrics"""
    symbol: str
    company_name: str
    exchange: str
    total_shares: float
    current_value: float
    total_invested: float
    returns: float
    returns_percent: float
    latest_price: float
    average_buy_price: float
    transactions: List[List[Any]]
    sector: str
    market_cap_category: str

@dataclass
class StockPortfolioAnalysis:
    """Complete stock portfolio analysis data structure"""
    holdings: List[StockHolding]
    portfolio_timeline: List[Dict[str, Any]]
    sector_classification: Dict[str, List[StockHolding]]
    market_cap_classification: Dict[str, List[StockHolding]]
    total_value: float
    total_invested: float
    total_returns: float
    total_returns_percent: float
    top_performers: List[StockHolding]
    underperformers: List[StockHolding]
    dividend_income: float

class StockDataAgent:
    """Agent responsible for providing stock mock data"""
    
    def __init__(self):
        pass
    
    def get_stock_sample_data(self) -> Dict[str, Any]:
        """Return sample stock data with various transaction types"""
        return {
            "stocks": [
                {
                    "symbol": "RELIANCE",
                    "companyName": "Reliance Industries Limited",
                    "exchange": "NSE",
                    "sector": "Oil & Gas",
                    "marketCap": "Large Cap",
                    "txns": [
                        [1, "2023-10-15", 2450.0, 50, 122500.0],  # Buy
                        [1, "2023-11-20", 2380.0, 25, 59500.0],   # Buy
                        [2, "2024-01-10", 2650.0, 15, 39750.0],   # Sell
                        [4, "2024-03-15", 0.0, 0, 800.0],         # Dividend
                        [1, "2024-05-20", 2720.0, 20, 54400.0],   # Buy
                    ]
                },
                {
                    "symbol": "TCS",
                    "companyName": "Tata Consultancy Services Limited",
                    "exchange": "NSE",
                    "sector": "Information Technology",
                    "marketCap": "Large Cap",
                    "txns": [
                        [1, "2023-12-01", 3600.0, 30, 108000.0],  # Buy
                        [1, "2024-02-15", 3450.0, 20, 69000.0],   # Buy
                        [4, "2024-04-10", 0.0, 0, 1500.0],        # Dividend
                        [2, "2024-06-25", 3850.0, 10, 38500.0],   # Sell
                        [1, "2024-07-15", 3900.0, 15, 58500.0],   # Buy
                    ]
                },
                {
                    "symbol": "HDFCBANK",
                    "companyName": "HDFC Bank Limited",
                    "exchange": "NSE",
                    "sector": "Banking & Financial Services",
                    "marketCap": "Large Cap",
                    "txns": [
                        [1, "2024-01-05", 1650.0, 60, 99000.0],   # Buy
                        [1, "2024-03-10", 1580.0, 40, 63200.0],   # Buy
                        [4, "2024-05-20", 0.0, 0, 1200.0],        # Dividend
                        [2, "2024-07-08", 1720.0, 20, 34400.0],   # Sell
                    ]
                },
                {
                    "symbol": "INFY",
                    "companyName": "Infosys Limited",
                    "exchange": "NSE",
                    "sector": "Information Technology",
                    "marketCap": "Large Cap",
                    "txns": [
                        [1, "2024-02-12", 1450.0, 40, 58000.0],   # Buy
                        [1, "2024-04-18", 1380.0, 30, 41400.0],   # Buy
                        [4, "2024-06-15", 0.0, 0, 900.0],         # Dividend
                        [1, "2024-08-05", 1520.0, 25, 38000.0],   # Buy
                    ]
                },
                {
                    "symbol": "TATAMOTORS",
                    "companyName": "Tata Motors Limited",
                    "exchange": "NSE",
                    "sector": "Automobile",
                    "marketCap": "Large Cap",
                    "txns": [
                        [1, "2023-11-10", 650.0, 100, 65000.0],   # Buy
                        [1, "2024-01-22", 720.0, 50, 36000.0],    # Buy
                        [2, "2024-04-15", 850.0, 30, 25500.0],    # Sell
                        [1, "2024-07-20", 890.0, 40, 35600.0],    # Buy
                    ]
                },
                {
                    "symbol": "BHARTIARTL",
                    "companyName": "Bharti Airtel Limited",
                    "exchange": "NSE",
                    "sector": "Telecom",
                    "marketCap": "Large Cap",
                    "txns": [
                        [1, "2024-03-05", 850.0, 80, 68000.0],    # Buy
                        [1, "2024-05-12", 920.0, 50, 46000.0],    # Buy
                        [4, "2024-07-10", 0.0, 0, 650.0],         # Dividend
                        [2, "2024-08-15", 1050.0, 25, 26250.0],   # Sell
                    ]
                },
                {
                    "symbol": "ASIANPAINT",
                    "companyName": "Asian Paints Limited",
                    "exchange": "NSE",
                    "sector": "Consumer Goods",
                    "marketCap": "Large Cap",
                    "txns": [
                        [1, "2024-01-15", 3200.0, 20, 64000.0],   # Buy
                        [1, "2024-04-08", 3050.0, 15, 45750.0],   # Buy
                        [4, "2024-06-25", 0.0, 0, 700.0],         # Dividend
                    ]
                },
                {
                    "symbol": "ADANIPORTS",
                    "companyName": "Adani Ports and Special Economic Zone Limited",
                    "exchange": "NSE",
                    "sector": "Infrastructure",
                    "marketCap": "Large Cap",
                    "txns": [
                        [1, "2024-02-20", 720.0, 70, 50400.0],    # Buy
                        [2, "2024-06-10", 850.0, 20, 17000.0],    # Sell
                        [1, "2024-08-12", 780.0, 30, 23400.0],    # Buy
                    ]
                },
                {
                    "symbol": "WIPRO",
                    "companyName": "Wipro Limited",
                    "exchange": "NSE",
                    "sector": "Information Technology",
                    "marketCap": "Large Cap",
                    "txns": [
                        [1, "2024-04-01", 420.0, 120, 50400.0],   # Buy
                        [4, "2024-07-05", 0.0, 0, 480.0],         # Dividend
                        [1, "2024-08-20", 450.0, 80, 36000.0],    # Buy
                    ]
                },
                {
                    "symbol": "MARUTI",
                    "companyName": "Maruti Suzuki India Limited",
                    "exchange": "NSE",
                    "sector": "Automobile",
                    "marketCap": "Large Cap",
                    "txns": [
                        [1, "2024-03-12", 10500.0, 8, 84000.0],   # Buy
                        [1, "2024-06-18", 11200.0, 5, 56000.0],   # Buy
                        [4, "2024-08-10", 0.0, 0, 520.0],         # Dividend
                    ]
                }
            ]
        }
    
    async def fetch_stock_transactions(self) -> Dict[str, Any]:
        """Return mock stock data"""
        logger.info("Using mock stock data")
        return self.get_stock_sample_data()

class StockAnalysisAgent:
    """Agent responsible for processing and analyzing stock data"""
    
    def __init__(self):
        self.sector_mapping = {
            'oil & gas': 'Energy',
            'information technology': 'Technology',
            'banking & financial services': 'Financial Services',
            'automobile': 'Automobile',
            'telecom': 'Telecom',
            'consumer goods': 'Consumer Goods',
            'infrastructure': 'Infrastructure',
            'pharmaceuticals': 'Healthcare',
            'metals & mining': 'Materials',
            'real estate': 'Real Estate'
        }
        
        self.market_cap_categories = {
            'large cap': 'Large Cap',
            'mid cap': 'Mid Cap',
            'small cap': 'Small Cap'
        }
    
    def normalize_sector(self, sector: str) -> str:
        """Normalize sector name"""
        sector_lower = sector.lower()
        return self.sector_mapping.get(sector_lower, sector)
    
    def normalize_market_cap(self, market_cap: str) -> str:
        """Normalize market cap category"""
        market_cap_lower = market_cap.lower()
        return self.market_cap_categories.get(market_cap_lower, market_cap)
    
    def calculate_stock_metrics(self, stock_data: Dict[str, Any]) -> StockHolding:
        """Calculate metrics for a single stock"""
        transactions = stock_data.get('txns', [])
        
        if not transactions:
            return None
        
        # Calculate total shares, invested amount, and dividend income
        total_shares = 0
        total_invested = 0
        dividend_income = 0
        buy_transactions = []
        
        for txn in transactions:
            txn_type, date, price, quantity, amount = txn
            
            if txn_type == 1:  # Buy
                total_shares += quantity
                total_invested += amount
                buy_transactions.append((price, quantity, amount))
            elif txn_type == 2:  # Sell
                total_shares -= quantity
                total_invested -= amount
            elif txn_type == 4:  # Dividend
                dividend_income += amount
        
        if total_shares <= 0:
            return None
        
        # Calculate average buy price
        total_buy_amount = sum(txn[2] for txn in buy_transactions)
        total_buy_shares = sum(txn[1] for txn in buy_transactions)
        average_buy_price = total_buy_amount / total_buy_shares if total_buy_shares > 0 else 0
        
        # Get latest price (most recent transaction with price > 0)
        latest_price = 0
        for txn in reversed(transactions):
            if txn[2] > 0:  # Price > 0 (exclude dividend transactions)
                latest_price = txn[2]
                break
        
        # Calculate current value and returns
        current_value = total_shares * latest_price
        returns = current_value - total_invested + dividend_income
        returns_percent = (returns / total_invested * 100) if total_invested > 0 else 0
        
        return StockHolding(
            symbol=stock_data.get('symbol', ''),
            company_name=stock_data.get('companyName', ''),
            exchange=stock_data.get('exchange', ''),
            total_shares=total_shares,
            current_value=current_value,
            total_invested=total_invested,
            returns=returns,
            returns_percent=returns_percent,
            latest_price=latest_price,
            average_buy_price=average_buy_price,
            transactions=transactions,
            sector=self.normalize_sector(stock_data.get('sector', '')),
            market_cap_category=self.normalize_market_cap(stock_data.get('marketCap', ''))
        )
    
    def calculate_portfolio_timeline(self, holdings: List[StockHolding]) -> List[Dict[str, Any]]:
        """Calculate portfolio value over time"""
        # Get all unique dates from all transactions
        all_dates = set()
        for holding in holdings:
            for txn in holding.transactions:
                all_dates.add(txn[1])  # Transaction date
        
        sorted_dates = sorted(list(all_dates))
        timeline = []
        
        for date in sorted_dates:
            total_value = 0
            total_invested = 0
            total_dividend = 0
            
            for holding in holdings:
                # Get transactions up to this date
                relevant_txns = [txn for txn in holding.transactions if txn[1] <= date]
                
                if relevant_txns:
                    # Calculate shares and invested amount up to this date
                    shares = 0
                    invested = 0
                    dividends = 0
                    latest_price = 0
                    
                    for txn in relevant_txns:
                        txn_type, txn_date, price, quantity, amount = txn
                        
                        if txn_type == 1:  # Buy
                            shares += quantity
                            invested += amount
                            latest_price = price
                        elif txn_type == 2:  # Sell
                            shares -= quantity
                            invested -= amount
                            latest_price = price
                        elif txn_type == 4:  # Dividend
                            dividends += amount
                    
                    if shares > 0:
                        total_value += shares * latest_price
                        total_invested += invested
                        total_dividend += dividends
            
            timeline.append({
                'date': date,
                'value': total_value,
                'invested': total_invested,
                'dividends': total_dividend,
                'returns': total_value - total_invested + total_dividend
            })
        
        return timeline
    
    def classify_by_sector(self, holdings: List[StockHolding]) -> Dict[str, List[StockHolding]]:
        """Classify holdings by sector"""
        classification = {}
        
        for holding in holdings:
            sector = holding.sector
            if sector not in classification:
                classification[sector] = []
            classification[sector].append(holding)
        
        return classification
    
    def classify_by_market_cap(self, holdings: List[StockHolding]) -> Dict[str, List[StockHolding]]:
        """Classify holdings by market cap"""
        classification = {}
        
        for holding in holdings:
            market_cap = holding.market_cap_category
            if market_cap not in classification:
                classification[market_cap] = []
            classification[market_cap].append(holding)
        
        return classification
    
    def get_top_performers_and_losers(self, holdings: List[StockHolding], count: int = 3) -> tuple:
        """Get top performers and underperformers"""
        sorted_holdings = sorted(holdings, key=lambda h: h.returns_percent, reverse=True)
        
        top_performers = sorted_holdings[:count]
        underperformers = sorted_holdings[-count:] if len(sorted_holdings) >= count else []
        underperformers.reverse()  # Show worst first
        
        return top_performers, underperformers
    
    async def analyze_portfolio(self, stock_data: Dict[str, Any]) -> StockPortfolioAnalysis:
        """Perform complete stock portfolio analysis"""
        try:
            stock_transactions = stock_data.get('stocks', [])
            
            if not stock_transactions:
                raise Exception("No stock transactions found")
            
            # Calculate metrics for each stock
            holdings = []
            total_dividend_income = 0
            
            for stock_data in stock_transactions:
                holding = self.calculate_stock_metrics(stock_data)
                if holding and holding.total_shares > 0:  # Only include stocks with positive holdings
                    holdings.append(holding)
                    # Calculate dividend income from transactions
                    dividend_income = sum(txn[4] for txn in holding.transactions if txn[0] == 4)
                    total_dividend_income += dividend_income
            
            if not holdings:
                raise Exception("No valid holdings found")
            
            # Calculate portfolio-level metrics
            total_value = sum(h.current_value for h in holdings)
            total_invested = sum(h.total_invested for h in holdings)
            total_returns = total_value - total_invested + total_dividend_income
            total_returns_percent = (total_returns / total_invested * 100) if total_invested > 0 else 0
            
            # Generate timeline
            portfolio_timeline = self.calculate_portfolio_timeline(holdings)
            
            # Classify holdings
            sector_classification = self.classify_by_sector(holdings)
            market_cap_classification = self.classify_by_market_cap(holdings)
            
            # Get top performers and underperformers
            top_performers, underperformers = self.get_top_performers_and_losers(holdings)
            
            return StockPortfolioAnalysis(
                holdings=holdings,
                portfolio_timeline=portfolio_timeline,
                sector_classification=sector_classification,
                market_cap_classification=market_cap_classification,
                total_value=total_value,
                total_invested=total_invested,
                total_returns=total_returns,
                total_returns_percent=total_returns_percent,
                top_performers=top_performers,
                underperformers=underperformers,
                dividend_income=total_dividend_income
            )
            
        except Exception as e:
            logger.error(f"Error analyzing stock portfolio: {e}")
            raise

class StockPipeline:
    """Main pipeline orchestrating stock data fetching and analysis"""
    
    def __init__(self):
        self.data_agent = StockDataAgent()
        self.analysis_agent = StockAnalysisAgent()
    
    async def get_portfolio_analysis(self) -> Dict[str, Any]:
        """Get complete stock portfolio analysis"""
        try:
            # Step 1: Fetch data using data agent
            logger.info("Fetching stock data...")
            stock_data = await self.data_agent.fetch_stock_transactions()
            
            if not stock_data:
                raise Exception("Failed to fetch stock data")
            
            # Step 2: Analyze data using analysis agent
            logger.info("Analyzing stock portfolio...")
            analysis = await self.analysis_agent.analyze_portfolio(stock_data)
            
            # Step 3: Format for frontend consumption
            return self._format_for_frontend(analysis)
            
        except Exception as e:
            logger.error(f"Stock pipeline error: {e}")
            raise
    
    def _format_for_frontend(self, analysis: StockPortfolioAnalysis) -> Dict[str, Any]:
        """Format analysis data for frontend consumption"""
        return {
            'holdings': [
                {
                    'symbol': h.symbol,
                    'companyName': h.company_name,
                    'exchange': h.exchange,
                    'totalShares': h.total_shares,
                    'currentValue': h.current_value,
                    'totalInvested': h.total_invested,
                    'returns': h.returns,
                    'returnsPercent': h.returns_percent,
                    'latestPrice': h.latest_price,
                    'averageBuyPrice': h.average_buy_price,
                    'sector': h.sector,
                    'marketCapCategory': h.market_cap_category,
                    'transactions': h.transactions
                }
                for h in analysis.holdings
            ],
            'portfolioTimeline': analysis.portfolio_timeline,
            'sectorClassification': {
                sector: [
                    {
                        'symbol': h.symbol,
                        'companyName': h.company_name,
                        'currentValue': h.current_value,
                        'returnsPercent': h.returns_percent
                    }
                    for h in holdings
                ]
                for sector, holdings in analysis.sector_classification.items()
            },
            'marketCapClassification': {
                category: [
                    {
                        'symbol': h.symbol,
                        'companyName': h.company_name,
                        'currentValue': h.current_value,
                        'returnsPercent': h.returns_percent
                    }
                    for h in holdings
                ]
                for category, holdings in analysis.market_cap_classification.items()
            },
            'summary': {
                'totalValue': analysis.total_value,
                'totalInvested': analysis.total_invested,
                'totalReturns': analysis.total_returns,
                'totalReturnsPercent': analysis.total_returns_percent,
                'dividendIncome': analysis.dividend_income
            },
            'topPerformers': [
                {
                    'symbol': h.symbol,
                    'companyName': h.company_name,
                    'currentValue': h.current_value,
                    'returns': h.returns,
                    'returnsPercent': h.returns_percent
                }
                for h in analysis.top_performers
            ],
            'underperformers': [
                {
                    'symbol': h.symbol,
                    'companyName': h.company_name,
                    'currentValue': h.current_value,
                    'returns': h.returns,
                    'returnsPercent': h.returns_percent
                }
                for h in analysis.underperformers
            ]
        }

# Main function for testing
async def main():
    """Test the stock pipeline"""
    pipeline = StockPipeline()
    try:
        result = await pipeline.get_portfolio_analysis()
        print(json.dumps(result, indent=2, default=str))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())