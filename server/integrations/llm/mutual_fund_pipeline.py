import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging

# Configure logging
logger = logging.getLogger(__name__)

@dataclass
class FundHolding:
    """Represents a mutual fund holding with calculated metrics"""
    name: str
    full_name: str
    isin: str
    folio_id: str
    total_units: float
    current_value: float
    total_invested: float
    returns: float
    returns_percent: float
    latest_price: float
    transactions: List[List[Any]]
    fund_category: str

@dataclass
class PortfolioAnalysis:
    """Complete portfolio analysis data structure"""
    holdings: List[FundHolding]
    portfolio_timeline: List[Dict[str, Any]]
    classification: Dict[str, List[FundHolding]]
    total_value: float
    total_invested: float
    total_returns: float
    total_returns_percent: float
    top_performers: List[FundHolding]
    underperformers: List[FundHolding]

class MutualFundDataAgent:
    """Agent responsible for providing mutual fund mock data"""
    
    def __init__(self):
        pass
    
    def get_mutual_fund_sample_data(self) -> Dict[str, Any]:
        """Return sample mutual fund data sorted by increasing positive performance"""
        return {
            "mutual_funds": [
            {
                "schemeName": "Parag Parikh Flexi Cap Fund - Direct Plan - Growth",
                "isin": "INF879O01027",
                "folioId": "22334455",
                "txns": [
                    [1, "2023-11-15", 130.0, 300.0, 39000.0],
                    [1, "2023-12-15", 132.0, 295.45, 39000.0],
                    [1, "2024-01-15", 135.0, 288.89, 39000.0],
                    [1, "2024-02-15", 138.0, 282.61, 39000.0],
                    [1, "2024-03-15", 140.0, 278.57, 39000.0],
                    [1, "2024-04-15", 142.0, 274.65, 39000.0],
                    [2, "2024-05-15", 145.0, -100.0, -14500.0]
                ]
            },
            {
                "schemeName": "Axis Bluechip Fund - Direct Plan - Growth",
                "isin": "INF846K01DP9",
                "folioId": "44556677",
                "txns": [
                    [1, "2023-12-05", 150.0, 200.0, 30000.0],
                    [1, "2024-01-05", 152.0, 197.37, 30000.0],
                    [1, "2024-02-05", 155.0, 193.55, 30000.0],
                    [1, "2024-03-05", 158.0, 189.87, 30000.0],
                    [1, "2024-04-05", 160.0, 187.5, 30000.0],
                    [1, "2024-05-05", 162.0, 185.19, 30000.0],
                    [2, "2024-06-05", 165.0, -50.0, -8250.0],
                    [1, "2024-07-05", 168.0, 178.57, 30000.0]
                ]
            },
            {
                "schemeName": "HDFC Equity Fund - Direct Plan - Growth",
                "isin": "INF179K01014",
                "folioId": "12345678",
                "txns": [
                    [1, "2024-01-15", 120.0, 500.0, 60000.0],
                    [1, "2024-02-15", 122.5, 491.8, 60250.0],
                    [1, "2024-03-15", 125.0, 480.0, 60000.0],
                    [1, "2024-04-15", 128.0, 468.75, 60000.0],
                    [1, "2024-05-15", 130.0, 461.54, 60000.0],
                    [1, "2024-06-15", 132.0, 454.55, 60000.0],
                    [2, "2024-07-15", 135.0, -200.0, -27000.0]
                ]
            },
            {
                "schemeName": "Kotak Flexicap Fund - Direct Plan - Growth",
                "isin": "INF174K01369",
                "folioId": "99887766",
                "txns": [
                    [1, "2024-02-20", 140.0, 250.0, 35000.0],
                    [1, "2024-03-20", 142.0, 246.48, 35000.0],
                    [1, "2024-04-20", 145.0, 241.38, 35000.0],
                    [1, "2024-05-20", 148.0, 236.49, 35000.0],
                    [1, "2024-06-20", 150.0, 233.33, 35000.0],
                    [2, "2024-07-20", 153.0, -100.0, -15300.0],
                    [1, "2024-08-20", 155.0, 225.81, 35000.0]
                ]
            },
            {
                "schemeName": "Mirae Asset Emerging Bluechip Fund - Direct Plan - Growth",
                "isin": "INF769K01DN2",
                "folioId": "66778899",
                "txns": [
                    [1, "2024-04-01", 95.0, 500.0, 47500.0],
                    [1, "2024-05-01", 97.0, 489.69, 47500.0],
                    [1, "2024-06-01", 100.0, 475.0, 47500.0],
                    [1, "2024-07-01", 102.0, 465.69, 47500.0],
                    [2, "2024-08-01", 105.0, -150.0, -15750.0],
                    [1, "2024-09-01", 108.0, 439.81, 47500.0]
                ]
            },
            {
                "schemeName": "Nippon India Large Cap Fund - Direct Plan - Growth",
                "isin": "INF204K01E10",
                "folioId": "33445566",
                "txns": [
                    [1, "2024-01-10", 110.0, 450.0, 49500.0],
                    [1, "2024-02-10", 112.0, 441.96, 49500.0],
                    [1, "2024-03-10", 115.0, 430.43, 49500.0],
                    [1, "2024-04-10", 118.0, 419.49, 49500.0],
                    [1, "2024-05-10", 120.0, 412.5, 49500.0],
                    [3, "2024-06-10", 122.0, 20.0, 2440.0],
                    [1, "2024-07-10", 125.0, 396.0, 49500.0]
                ]
            },
            {
                "schemeName": "SBI Small Cap Fund - Direct Plan - Growth",
                "isin": "INF200K01142",
                "folioId": "87654321",
                "txns": [
                    [1, "2024-01-01", 100.0, 400.0, 40000.0],
                    [1, "2024-02-01", 102.0, 392.16, 40000.0],
                    [1, "2024-03-01", 105.0, 380.95, 40000.0],
                    [1, "2024-04-01", 108.0, 370.37, 40000.0],
                    [1, "2024-05-01", 110.0, 363.64, 40000.0],
                    [1, "2024-06-01", 112.0, 357.14, 40000.0],
                    [1, "2024-07-01", 115.0, 347.83, 40000.0],
                    [2, "2024-08-01", 118.0, -100.0, -11800.0]
                ]
            },
            {
                "schemeName": "ICICI Prudential Technology Fund - Direct Plan - Growth",
                "isin": "INF109K01234",
                "folioId": "11223344",
                "txns": [
                    [1, "2024-03-10", 125.0, 300.0, 37500.0],
                    [1, "2024-04-10", 128.0, 292.97, 37500.0],
                    [1, "2024-05-10", 130.0, 288.46, 37500.0],
                    [1, "2024-06-10", 132.0, 284.09, 37500.0],
                    [1, "2024-07-10", 135.0, 277.78, 37500.0],
                    [1, "2024-08-10", 138.0, 271.74, 37500.0],
                    [3, "2024-09-10", 140.0, 10.0, 1400.0]
                ]
            }
        ]
    }

    
    async def fetch_mutual_fund_transactions(self) -> Dict[str, Any]:
        """Return mock mutual fund data"""
        logger.info("Using mock mutual fund data")
        return self.get_mutual_fund_sample_data()

class MutualFundAnalysisAgent:
    """Agent responsible for processing and analyzing mutual fund data"""
    
    def __init__(self):
        self.fund_categories = {
            'large_cap': ['large cap', 'bluechip', 'large & mid cap'],
            'mid_cap': ['mid cap', 'midcap'],
            'small_cap': ['small cap', 'smallcap'],
            'multi_cap': ['multi cap', 'multicap', 'diversified'],
            'flexi_cap': ['flexi cap', 'flexicap'],
            'balanced_hybrid': ['balanced', 'advantage', 'hybrid', 'conservative', 'aggressive'],
            'sectoral_thematic': ['gold', 'banking', 'pharma', 'it', 'auto', 'infra', 'energy', 'fmcg'],
            'index': ['index', 'nifty', 'sensex', 'etf'],
            'debt': ['debt', 'bond', 'gilt', 'liquid', 'ultra short', 'short term', 'medium term', 'long term'],
            'international': ['international', 'global', 'us', 'nasdaq', 'emerging']
        }
    
    def categorize_fund(self, fund_name: str) -> str:
        """Categorize fund based on its name"""
        fund_name_lower = fund_name.lower()
        
        for category, keywords in self.fund_categories.items():
            for keyword in keywords:
                if keyword in fund_name_lower:
                    return category.replace('_', ' ').title()

        return 'Other'
    
    def calculate_fund_metrics(self, fund_data: Dict[str, Any]) -> FundHolding:
        """Calculate metrics for a single fund"""
        transactions = fund_data.get('txns', [])
        
        if not transactions:
            return None
        
        # Calculate total units and invested amount
        total_units = sum(txn[3] for txn in transactions if txn[0] == 1)  # Buy transactions
        total_units -= sum(txn[3] for txn in transactions if txn[0] == 2)  # Subtract sell transactions
        
        total_invested = sum(txn[4] for txn in transactions if txn[0] == 1)  # Buy amounts
        total_invested -= sum(txn[4] for txn in transactions if txn[0] == 2)  # Subtract sell amounts
        
        # Get latest price (most recent transaction)
        latest_price = transactions[0][2] if transactions else 0
        
        # Calculate current value and returns
        current_value = total_units * latest_price
        returns = current_value - total_invested
        returns_percent = (returns / total_invested * 100) if total_invested > 0 else 0
        
        # Extract fund name (remove plan details)
        full_name = fund_data.get('schemeName', '')
        name = full_name.split(' - ')[0] if ' - ' in full_name else full_name
        
        return FundHolding(
            name=name,
            full_name=full_name,
            isin=fund_data.get('isin', ''),
            folio_id=fund_data.get('folioId', ''),
            total_units=total_units,
            current_value=current_value,
            total_invested=total_invested,
            returns=returns,
            returns_percent=returns_percent,
            latest_price=latest_price,
            transactions=transactions,
            fund_category=self.categorize_fund(full_name)
        )
    
    def calculate_portfolio_timeline(self, holdings: List[FundHolding]) -> List[Dict[str, Any]]:
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
            
            for holding in holdings:
                # Get transactions up to this date
                relevant_txns = [txn for txn in holding.transactions if txn[1] <= date]
                
                if relevant_txns:
                    # Calculate units and invested amount up to this date
                    units = sum(txn[3] for txn in relevant_txns if txn[0] == 1)
                    units -= sum(txn[3] for txn in relevant_txns if txn[0] == 2)
                    
                    invested = sum(txn[4] for txn in relevant_txns if txn[0] == 1)
                    invested -= sum(txn[4] for txn in relevant_txns if txn[0] == 2)
                    
                    # Use the latest price from relevant transactions
                    latest_price = relevant_txns[0][2]
                    
                    total_value += units * latest_price
                    total_invested += invested
            
            timeline.append({
                'date': date,
                'value': total_value,
                'invested': total_invested,
                'returns': total_value - total_invested
            })
        
        return timeline
    
    def classify_holdings(self, holdings: List[FundHolding]) -> Dict[str, List[FundHolding]]:
        """Classify holdings by fund category"""
        classification = {}
        
        for holding in holdings:
            category = holding.fund_category
            if category not in classification:
                classification[category] = []
            classification[category].append(holding)
        
        return classification
    
    def get_top_performers_and_losers(self, holdings: List[FundHolding], count: int = 3) -> tuple:
        """Get top performers and underperformers"""
        sorted_holdings = sorted(holdings, key=lambda h: h.returns_percent, reverse=True)
        
        top_performers = sorted_holdings[:count]
        underperformers = sorted_holdings[-count:] if len(sorted_holdings) >= count else []
        underperformers.reverse()  # Show worst first
        
        return top_performers, underperformers
    
    async def analyze_portfolio(self, mf_data: Dict[str, Any]) -> PortfolioAnalysis:
        """Perform complete portfolio analysis"""
        try:
            mf_transactions = mf_data.get('mutual_funds', [])
            
            if not mf_transactions:
                raise Exception("No mutual fund transactions found")
            
            # Calculate metrics for each fund
            holdings = []
            for fund_data in mf_transactions:
                holding = self.calculate_fund_metrics(fund_data)
                if holding and holding.total_units > 0:  # Only include funds with positive holdings
                    holdings.append(holding)
            
            if not holdings:
                raise Exception("No valid holdings found")
            
            # Calculate portfolio-level metrics
            total_value = sum(h.current_value for h in holdings)
            total_invested = sum(h.total_invested for h in holdings)
            total_returns = total_value - total_invested
            total_returns_percent = (total_returns / total_invested * 100) if total_invested > 0 else 0
            
            # Generate timeline
            portfolio_timeline = self.calculate_portfolio_timeline(holdings)
            
            # Classify holdings
            classification = self.classify_holdings(holdings)
            
            # Get top performers and underperformers
            top_performers, underperformers = self.get_top_performers_and_losers(holdings)
            
            return PortfolioAnalysis(
                holdings=holdings,
                portfolio_timeline=portfolio_timeline,
                classification=classification,
                total_value=total_value,
                total_invested=total_invested,
                total_returns=total_returns,
                total_returns_percent=total_returns_percent,
                top_performers=top_performers,
                underperformers=underperformers
            )
            
        except Exception as e:
            logger.error(f"Error analyzing portfolio: {e}")
            raise

class MutualFundPipeline:
    """Main pipeline orchestrating data fetching and analysis"""
    
    def __init__(self):
        self.data_agent = MutualFundDataAgent()
        self.analysis_agent = MutualFundAnalysisAgent()
    
    async def get_portfolio_analysis(self) -> Dict[str, Any]:
        """Get complete portfolio analysis"""
        try:
            # Step 1: Fetch data using data agent
            logger.info("Fetching mutual fund data...")
            mf_data = await self.data_agent.fetch_mutual_fund_transactions()
            
            if not mf_data:
                raise Exception("Failed to fetch mutual fund data")
            
            # Step 2: Analyze data using analysis agent
            logger.info("Analyzing portfolio...")
            analysis = await self.analysis_agent.analyze_portfolio(mf_data)
            
            # Step 3: Format for frontend consumption
            return self._format_for_frontend(analysis)
            
        except Exception as e:
            logger.error(f"Pipeline error: {e}")
            raise
    
    def _format_for_frontend(self, analysis: PortfolioAnalysis) -> Dict[str, Any]:
        """Format analysis data for frontend consumption"""
        return {
            'holdings': [
                {
                    'name': h.name,
                    'fullName': h.full_name,
                    'isin': h.isin,
                    'folioId': h.folio_id,
                    'totalUnits': h.total_units,
                    'currentValue': h.current_value,
                    'totalInvested': h.total_invested,
                    'returns': h.returns,
                    'returnsPercent': h.returns_percent,
                    'latestPrice': h.latest_price,
                    'fundCategory': h.fund_category,
                    'transactions': h.transactions
                }
                for h in analysis.holdings
            ],
            'portfolioTimeline': analysis.portfolio_timeline,
            'classification': {
                category: [
                    {
                        'name': h.name,
                        'currentValue': h.current_value,
                        'returnsPercent': h.returns_percent
                    }
                    for h in holdings
                ]
                for category, holdings in analysis.classification.items()
            },
            'summary': {
                'totalValue': analysis.total_value,
                'totalInvested': analysis.total_invested,
                'totalReturns': analysis.total_returns,
                'totalReturnsPercent': analysis.total_returns_percent
            },
            'topPerformers': [
                {
                    'name': h.name,
                    'currentValue': h.current_value,
                    'returns': h.returns,
                    'returnsPercent': h.returns_percent
                }
                for h in analysis.top_performers
            ],
            'underperformers': [
                {
                    'name': h.name,
                    'currentValue': h.current_value,
                    'returns': h.returns,
                    'returnsPercent': h.returns_percent
                }
                for h in analysis.underperformers
            ]
        }

# Main function for testing
async def main():
    """Test the pipeline"""
    pipeline = MutualFundPipeline()
    try:
        result = await pipeline.get_portfolio_analysis()
        print(json.dumps(result, indent=2, default=str))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
