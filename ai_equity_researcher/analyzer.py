import yfinance as yf
import pandas as pd
from datetime import datetime
from typing import Dict, List, Tuple, Optional
class StockAnalyzer:
    """
    A comprehensive stock analysis tool that provides various types of financial and market data analysis.
    
    The class is organized into the following method groups:
    1. Basic Company Information: Core company data and overview
    2. Financial Analysis: Financial statements and performance metrics
    3. Market Analysis: Price, volume, and trading statistics (generated)
    4. Industry Analysis: Sector and industry-specific data
    5. External Analysis: Recommendations, news, and related securities
    6. Report Generation: Comprehensive analysis reports
    """

    def __init__(self, ticker_symbol: str):
        """Initialize the StockAnalyzer with a specific ticker symbol."""
        self.ticker_symbol = ticker_symbol
        self.ticker = yf.Ticker(ticker_symbol)

    def get_ticker_history(self, start_date: Optional[str] = None, 
                         end_date: Optional[str] = None, 
                         interval: str = "1d") -> pd.DataFrame:
        """Fetch historical price and volume data."""
        return self.ticker.history(start=start_date, end=end_date, interval=interval)

    # ==========================================
    # 1. Basic Company Information Methods
    # ==========================================
    
    def get_company_overview(self) -> Dict:
        """Fetch basic company information and overview data."""
        info = self.ticker.info
        return {
            # Basic Information
            "name": info.get("longName", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "market_cap": info.get("marketCap", "N/A"),

        }
    def get_ticker_info(self) -> Dict:
        """Fetch detailed ticker information."""
        return self.ticker.info

    # ==========================================
    # 2. Financial Analysis Methods
    # ==========================================

    def fetch_financial_statements(self) -> Dict:
        """Fetch financial statements and key financial metrics for a ticker."""
        try:
            financials = self.ticker.quarterly_financials
            cash_flow = self.ticker.quarterly_cashflow
            info = self.ticker.info

            # Initialize default values
            data = {
                'revenue': 'N/A',
                'net_income': 'N/A',
                'operating_cash_flow': 'N/A',
                'capital_expenditures': 'N/A',

                # Financial Ratios
                "trailing_pe_ratio": info.get("trailingPE", "N/A"),
                "forward_pe_ratio": info.get("forwardPE", "N/A"),
                "price_to_book": info.get("priceToBook", "N/A"),
                "price_to_sales_ratio": info.get("priceToSalesTrailing12Months", "N/A"),

                # Dividend Information
                "dividend_rate": info.get("dividendRate", "N/A"),
                "dividend_yield": info.get("dividendYield", "N/A"),
                "payout_ratio": info.get("payoutRatio", "N/A"),

                # Growth Metrics
                "earnings_growth": info.get("earningsGrowth", "N/A"),
                "revenue_growth": info.get("revenueGrowth", "N/A"),

                # Profitability Metrics
                "profit_margins": info.get("profitMargins", "N/A"),
                "return_on_assets": info.get("returnOnAssets", "N/A"),
                "return_on_equity": info.get("returnOnEquity", "N/A"),
                "gross_margins": info.get("grossMargins", "N/A"),
                "ebitda_margins": info.get("ebitdaMargins", "N/A"),

                # Liquidity & Leverage
                "current_ratio": info.get("currentRatio", "N/A"),
                "quick_ratio": info.get("quickRatio", "N/A"),
                "debt_to_equity": info.get("debtToEquity", "N/A"),
                "operating_cash_flow": info.get("operatingCashflow", "N/A"),
                "free_cash_flow": info.get("freeCashflow", "N/A"),
            }

            if not financials.empty:
                # Extract revenue and net income
                latest_period = financials.columns[0]  # Get the most recent column (quarter)
                if "Total Revenue" in financials.index:
                    data['revenue'] = f"${financials.loc['Total Revenue', latest_period]:,.2f}"
                if "Net Income" in financials.index:
                    data['net_income'] = f"${financials.loc['Net Income', latest_period]:,.2f}"

            if not cash_flow.empty:
                # Extract cash flow metrics
                latest_period = cash_flow.columns[0]  # Get the most recent column (quarter)
                if "Operating Cash Flow" in cash_flow.index:
                    data['operating_cash_flow'] = f"${cash_flow.loc['Operating Cash Flow', latest_period]:,.2f}"
                if "Capital Expenditure" in cash_flow.index:
                    data['capital_expenditures'] = f"${cash_flow.loc['Capital Expenditure', latest_period]:,.2f}"

            return data

        except Exception as e:
            print(f"Error fetching financial statements: {e}")
            return {
                'revenue': 'N/A',
                'net_income': 'N/A',
                'operating_cash_flow': 'N/A',
                'capital_expenditures': 'N/A',
                "trailing_pe_ratio": "N/A",
                "forward_pe_ratio": "N/A",
                "price_to_book": "N/A",
                "price_to_sales_ratio": "N/A",
                "dividend_rate": "N/A",
                "dividend_yield": "N/A",
                "payout_ratio": "N/A",
                "earnings_growth": "N/A",
                "revenue_growth": "N/A",
                "profit_margins": "N/A",
                "return_on_assets": "N/A",
                "return_on_equity": "N/A",
                "gross_margins": "N/A",
                "ebitda_margins": "N/A",
                "current_ratio": "N/A",
                "quick_ratio": "N/A",
                "debt_to_equity": "N/A",
            }


    # ==========================================
    # 3. Market Analysis Methods
    # ==========================================

    def get_market_performance_and_insight(self, start_date: str, end_date: str) -> Dict:
        """Analyze market performance metrics and provide insights for a specific period."""
        history = self.ticker.history(start=start_date, end=end_date)
        info = self.ticker.info
        if history.empty:
            return {"error": "No market data available for the specified period."}

        current_price = int(history["Close"].iloc[-1])
        average_price = int(history["Close"].mean())
        price_change = ((history["Close"].iloc[-1] - history["Close"].iloc[0]) / history["Close"].iloc[0]) * 100
        high_low_spread = ((history["High"].max() - history["Low"].min()) / history["Close"].mean()) * 100
        volatility = float(history["Close"].std())
        average_volume = int(history["Volume"].mean())
        max_volume = int(history["Volume"].max())

        return {
            "current_price": current_price,
            "average_price": average_price,
            "price_change": f"{price_change:.2f}%",
            "high_low_spread": f"{high_low_spread:.2f}%",
            "volatility": f"{volatility:.2f}%",
            "average_volume": average_volume,
            "max_volume": max_volume,
            "52_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
            "52_week_low": info.get("fiftyTwoWeekLow", "N/A"),
            "average_volume": info.get("averageVolume", "N/A"),
            "beta": info.get("beta", "N/A"),
            
        }


    # ==========================================
    # 4. Industry Analysis Methods
    # ==========================================

    def get_sector_and_industry_analysis(self) -> Dict:
        """Perform comprehensive sector and industry analysis."""
        sector_data, industry_data = self.get_sector_and_industry_data()
        return {
            "sector_data": sector_data,
            "industry_data": industry_data
        }

    def get_sector_and_industry_data(self) -> Tuple[Optional[Dict], Optional[Dict]]:
        """Fetch detailed sector and industry metrics."""
        info = self.ticker.info
        sector_key = info.get('sectorKey', None)
        industry_key = info.get('industryKey', None)

        sector_data = None
        industry_data = None

        if sector_key:
            sector = yf.Sector(sector_key)
            sector_data = {
                "key": sector.key,
                "name": sector.name,
                "symbol": sector.symbol,
                "overview": sector.overview,
                "top_companies": sector.top_companies,
                "top_etfs": sector.top_etfs,
                "top_mutual_funds": sector.top_mutual_funds,
                "industries": sector.industries,
            }

        if industry_key:
            industry = yf.Industry(industry_key)
            industry_data = {
                "key": industry.key,
                "name": industry.name,
                "sector_key": industry.sector_key,
                "sector_name": industry.sector_name,
                "top_performing_companies": industry.top_performing_companies,
                "top_growth_companies": industry.top_growth_companies,
            }

        return sector_data, industry_data

    # ==========================================
    # 5. External Analysis Methods
    # ==========================================

    def get_ticker_recommendations(self) -> Dict:
        """Fetch analyst recommendations and format them as a dictionary."""
        recommendations = self.ticker.recommendations
        info = self.ticker.info
        if recommendations is None or recommendations.empty:
            return {"error": "No recommendations data available."}

        latest_recommendation = recommendations.iloc[-1]
        return {
            "target_high_price": info.get("targetHighPrice", "N/A"),
            "target_low_price": info.get("targetLowPrice", "N/A"),
            "recommendation_mean": info.get("recommendationMean", "N/A"),
            "strong_buy": latest_recommendation.get("strongBuy", "N/A"),
            "buy": latest_recommendation.get("buy", "N/A"),
            "hold": latest_recommendation.get("hold", "N/A"),
            "sell": latest_recommendation.get("sell", "N/A"),
            "strong_sell": latest_recommendation.get("strongSell", "N/A")
        }


    def get_related_quotes(self, max_results: int = 5) -> List:
        """Find related securities and quotes."""
        search = yf.Search(self.ticker_symbol, max_results=max_results)
        return search.quotes

    def get_recent_news(self, news_count: int = 5) -> List[Dict]:
        """Fetch recent news and events."""
        search = yf.Search(self.ticker_symbol, news_count=news_count)
        return search.news

    # ==========================================
    # 6. Report Generation Methods
    # ==========================================

    def generate_report(self, year: int, quarter: str) -> Dict:
        """
        Generate a comprehensive analysis report organized by data category.
        
        The report includes sections for:
        - Company Overview
        - Financial Performance
        - Market Performance
        - Sector and Industry Analysis
        - Analyst Recommendations
        - Technical Statistics
        - Related Securities
        - Recent News
        """
        quarters = {
            "Q1": (f"{year}-01-01", f"{year}-03-31"),
            "Q2": (f"{year}-04-01", f"{year}-06-30"),
            "Q3": (f"{year}-07-01", f"{year}-09-30"),
            "Q4": (f"{year}-10-01", f"{year}-12-31"),
        }

        if quarter not in quarters:
            raise ValueError("Invalid quarter. Must be one of 'Q1', 'Q2', 'Q3', 'Q4'.")

        start_date, end_date = quarters[quarter]
        history = self.get_ticker_history(start_date, end_date)
        
        report = {
            "ticker": self.ticker_symbol,
            "report_date": datetime.now().strftime("%Y-%m-%d"),
            "sections": [
                {"name": "Company Overview", "data": self.get_company_overview()},
                {"name": "Financial Performance", "data": self.fetch_financial_statements()},
                {"name": "Market Performance", "data": self.get_market_performance_and_insight(start_date, end_date)},
                {"name": "Analyst Recommendations", "data": self.get_ticker_recommendations()},
                {"name": "Recent News", "data": self.get_recent_news()}
            ]
        }

        return report