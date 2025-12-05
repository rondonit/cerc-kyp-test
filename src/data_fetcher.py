import yfinance as yf

# import pandas as pd
from typing import Any, Dict
from .utils import get_value


def fetch_company_data(company: str) -> Dict[str, Any]:
    """
    Fetches financial data for a company from Yahoo Finance and
    returns it as a dictionary in the new specified nested format.
    """
    ticker = yf.Ticker(company)

    balance_sheet = ticker.balance_sheet
    income_statement = ticker.financials
    cash_flow = ticker.cashflow
    info = ticker.info

    ratios = {
        "total_assets": get_value(balance_sheet, ["Total Assets", "Total assets"]),
        "total_liabilities": get_value(
            balance_sheet, ["Total Liab", "Total Liabilities Net Minority Interest"]
        ),
        "total_equity": get_value(
            balance_sheet, ["Total Stockholder Equity", "Total Equity Gross Minority Interest"]
        ),
        "current_assets": get_value(balance_sheet, ["Total Current Assets", "Current Assets"]),
        "current_liabilities": get_value(
            balance_sheet, ["Total Current Liabilities", "Current Liabilities"]
        ),
        "total_revenue": get_value(income_statement, ["Total Revenue"]),
        "net_income": get_value(income_statement, ["Net Income", "Net Income Common Stockholders"]),
        "operating_cash_flow": get_value(
            cash_flow, ["Total Cash From Operating Activities", "Operating Cash Flow"]
        ),
    }

    location = {
        "address": info.get("address1", ""),
        "city": info.get("city", ""),
        "state": info.get("state", ""),
        "zip": info.get("zip", ""),
        "country": info.get("country", ""),
    }

    business = {
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "website": info.get("website"),
        "description": info.get("longBusinessSummary"),
    }

    metrics = {
        "market_cap": info.get("marketCap"),
        "enterprise_value": info.get("enterpriseValue"),
        "trailing_pe": info.get("trailingPE"),
        "forward_pe": info.get("forwardPE"),
        "dividend_yield": info.get("dividendYield"),
        "beta": info.get("beta"),
        "52_week_high": info.get("fiftyTwoWeekHigh"),
        "52_week_low": info.get("fiftyTwoWeekLow"),
    }

    company_data: Dict[str, Any] = {
        "company_ticker": company,
        "company_name": info.get("longName", company),
        "currency": info.get("financialCurrency", info.get("currency")),
        "location": location,
        "business": business,
        "ratios": ratios,
        "metrics": metrics,
    }

    return company_data
