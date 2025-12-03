import json
import logging
from pathlib import Path
from typing import Any, Dict, List

import yfinance as yf

logger = logging.getLogger(__name__)


def get_value(df: Any, row_names: List[str]) -> float:
    """
    Safely read the first matching row from the dataframe's first column.
    Returns 0.0 when the row does not exist or the dataframe is empty.
    """
    if df is None or getattr(df, "empty", True):
        return 0.0

    for name in row_names:
        if name in df.index:
            try:
                return float(df.loc[name].iloc[0].item())
            except Exception:
                logger.debug(
                    "Failed to parse value for row '%s'; trying next alias", name
                )
                continue  # try next alias

    logger.debug("Rows %s not found; returning 0.0", row_names)

    return 0.0


def build_company_payload(symbol: str) -> Dict[str, Any]:
    ticker = yf.Ticker(symbol)
    logger.info("Fetching data for %s", symbol)
    info: Dict[str, Any] = ticker.info  # type: ignore[assignment]

    # --- location ---
    location = {
        "address": info.get("address1"),
        "city": info.get("city"),
        "state": info.get("state"),
        "zip": info.get("zip"),
        "country": info.get("country"),
    }

    # --- business ---
    business = {
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "website": info.get("website"),
        "description": info.get("longBusinessSummary"),
    }

    balance_sheet = ticker.balance_sheet
    income_statement = ticker.financials
    cash_flow = ticker.cashflow
    logger.debug(
        "Balance sheet empty: %s | Financials empty: %s | Cashflow empty: %s",
        getattr(balance_sheet, "empty", True),
        getattr(income_statement, "empty", True),
        getattr(cash_flow, "empty", True),
    )

    metrics = {
        "total_assets": get_value(balance_sheet, ["Total Assets", "Total assets"]),
        "total_liabilities": get_value(
            balance_sheet, ["Total Liab", "Total Liabilities Net Minority Interest"]
        ),
        "total_equity": get_value(
            balance_sheet,
            ["Total Stockholder Equity", "Total Equity Gross Minority Interest"],
        ),
        "current_assets": get_value(
            balance_sheet, ["Total Current Assets", "Current Assets"]
        ),
        "current_liabilities": get_value(
            balance_sheet, ["Total Current Liabilities", "Current Liabilities"]
        ),
        "total_revenue": get_value(income_statement, ["Total Revenue"]),
        "net_income": get_value(
            income_statement, ["Net Income", "Net Income Common Stockholders"]
        ),
        "operating_cash_flow": get_value(
            cash_flow, ["Total Cash From Operating Activities", "Operating Cash Flow"]
        ),
    }

    payload: Dict[str, Any] = {
        "company_ticker": symbol,
        "company_name": info.get("longName", symbol),
        "currency": info.get("financialCurrency") or info.get("currency"),
        "location": location,
        "business": business,
        "metrics": metrics,
    }

    return payload


def main() -> None:
    symbol = "AAPL"
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
    data = build_company_payload(symbol)
    out_path = Path("aapl_kyp_minimal.json")
    out_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"Saved {out_path}")


if __name__ == "__main__":
    main()
