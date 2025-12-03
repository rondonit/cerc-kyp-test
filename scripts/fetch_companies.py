import json
from pathlib import Path
import yfinance as yf
import pandas as pd
from typing import Any, Dict, List

COMPANIES = ["AAPL", "MSFT", "AMZN", "GOOGL", "NVDA"]


def get_value(df: pd.DataFrame, row_names: List[str]) -> float:
    """
    Tries to read the first value in row_names from the fisrt column of the dataframe.
    If the row does not exist or dataframe is empty, returns 0.0
    """
    if df is None or df.empty:
        return 0.0

    for name in row_names:
        if name in df.index:
            try:
                return float(df.loc[name].iloc[0].item())
            except Exception:
                continue  # try next name

    return 0.0


def fetch_company_data(company: str) -> Dict[str, Any]:
    """
    Fetches financial data for a company from Yahoo Finance and
    return as a dictionary in normalized format.
    """
    ticker = yf.Ticker(company)

    balance_sheet = ticker.balance_sheet
    income_statement = ticker.financials
    cash_flow = ticker.cashflow
    info = ticker.info

    metrics = {
        # balance sheet
        "total_assets": get_value(balance_sheet, ["Total Assets", "Total assets"]),
        "total_liabilities": get_value(
            balance_sheet, ["Total Liab", "Total Liabilities Net Minority Interest"]
        ),
        "total_equity": get_value(
            balance_sheet,
            ["Total Stockholder Equity", "Total Equity Gross Minority Interest"],
        ),
        # liquidity
        "current_assets": get_value(
            balance_sheet, ["Total Current Assets", "Current Assets"]
        ),
        "current_liabilities": get_value(
            balance_sheet, ["Total Current Liabilities", "Current Liabilities"]
        ),
        # income statement
        "total_revenue": get_value(income_statement, ["Total Revenue"]),
        "net_income": get_value(
            income_statement, ["Net Income", "Net Income Common Stockholders"]
        ),
        # cash flow
        "operating_cash_flow": get_value(
            cash_flow, ["Total Cash From Operating Activities", "Operating Cash Flow"]
        ),
    }

    company_data: Dict[str, Any] = {
        "company_ticker": company,
        "company_name": info.get("longName", company),
        "currency": info.get("financialCurrency", info.get("currency", None)),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "website": info.get("website"),
        "description": info.get("longBusinessSummary"),
        "metrics": metrics,
    }

    return company_data


def main():
    # Fetch data for all companies and save to JSON files
    output_dir = Path("company_data")
    output_dir.mkdir(exist_ok=True)
    for company in COMPANIES:
        data = fetch_company_data(company)
        output_file = output_dir / f"{company}.json"
        with open(output_file, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Saved data for {company} to {output_file}")


if __name__ == "__main__":
    main()
