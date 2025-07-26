from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import sys
import os

# Add the parent directory to the path to import from integrations
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from integrations.llm.mutual_fund_pipeline import MutualFundPipeline
from integrations.llm.stocks_pipeline import StockPipeline 

router = APIRouter(prefix="/api/mutual-funds", tags=["mutual-funds"])

@router.get("/analysis")
async def get_mutual_fund_analysis():
    """
    Get comprehensive mutual fund portfolio analysis
    """
    try:
        pipeline = MutualFundPipeline()
        analysis_data = await pipeline.get_portfolio_analysis()

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": analysis_data,
                "message": "Mutual fund portfolio analysis retrieved successfully"
            }
        )
    except Exception as e:
        print(f"Error in mutual fund analysis endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve mutual fund portfolio analysis: {str(e)}"
        )

@router.get("/holdings")
async def get_mutual_fund_holdings():
    """
    Get basic mutual fund holdings data
    """
    try:
        pipeline = MutualFundPipeline()
        analysis_data = await pipeline.get_portfolio_analysis()

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": {
                    "holdings": analysis_data.get("holdings", []),
                    "summary": analysis_data.get("summary", {})
                },
                "message": "Holdings retrieved successfully"
            }
        )
    except Exception as e:
        print(f"Error in holdings endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve holdings: {str(e)}"
        )

@router.get("/performance")
async def get_performance_metrics():
    """
    Get performance metrics including top performers and underperformers
    """
    try:
        pipeline = MutualFundPipeline()
        analysis_data = await pipeline.get_portfolio_analysis()

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": {
                    "topPerformers": analysis_data.get("topPerformers", []),
                    "underperformers": analysis_data.get("underperformers", []),
                    "portfolioTimeline": analysis_data.get("portfolioTimeline", []),
                    "summary": analysis_data.get("summary", {})
                },
                "message": "Performance metrics retrieved successfully"
            }
        )
    except Exception as e:
        print(f"Error in performance endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve performance metrics: {str(e)}"
        )

@router.get("/classification")
async def get_fund_classification():
    """
    Get fund classification data
    """
    try:
        pipeline = MutualFundPipeline()
        analysis_data = await pipeline.get_portfolio_analysis()

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": {
                    "classification": analysis_data.get("classification", {}),
                    "summary": analysis_data.get("summary", {})
                },
                "message": "Fund classification retrieved successfully"
            }
        )
    except Exception as e:
        print(f"Error in classification endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve fund classification: {str(e)}"
        )

@router.get("/stock-analysis")
async def get_stock_analysis_from_mutual_fund_route():
    """
    Get comprehensive stock portfolio analysis (from /api/mutual-funds route)
    """
    try:
        pipeline = StockPipeline()
        analysis_data = await pipeline.get_portfolio_analysis()

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": analysis_data,
                "message": "Stock portfolio analysis retrieved successfully"
            }
        )
    except Exception as e:
        print(f"Error in stock analysis endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve stock portfolio analysis: {str(e)}"
        )
