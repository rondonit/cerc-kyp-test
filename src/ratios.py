from typing import Any, Dict
from .utils import _safe_div


def compute_ratios(company_data: Dict[str, Any]) -> Dict[str, float]:
    """
    Compute the ratios used by the risk template. Returns 0.0 when denominators
    are zero or missing.
    """
    # extract necessary metrics from company data for ratio calculations
    ratios_data = company_data.get("ratios", {})

    total_assets = float(ratios_data.get("total_assets", 0.0) or 0.0)  # evita None
    total_liabilities = float(ratios_data.get("total_liabilities", 0.0) or 0.0)
    total_equity = float(ratios_data.get("total_equity", 0.0) or 0.0)
    current_assets = float(ratios_data.get("current_assets", 0.0) or 0.0)
    current_liabilities = float(ratios_data.get("current_liabilities", 0.0) or 0.0)
    total_revenue = float(ratios_data.get("total_revenue", 0.0) or 0.0)
    net_income = float(ratios_data.get("net_income", 0.0) or 0.0)
    operating_cash_flow = float(ratios_data.get("operating_cash_flow", 0.0) or 0.0)

    ratios = {
        # Liquidity
        "current_ratio": _safe_div(current_assets, current_liabilities),
        # Leverage
        "debt_to_equity_ratio": _safe_div(total_liabilities, total_equity),
        "assets_to_equity_ratio": _safe_div(total_assets, total_equity),
        "equity_ratio": _safe_div(total_equity, total_assets),
        "liabilities_ratio": _safe_div(total_liabilities, total_assets),
        # Profitability
        "net_margin": _safe_div(net_income, total_revenue),
        "roe": _safe_div(net_income, total_equity),
        "roa": _safe_div(net_income, total_assets),
        # Cash generation
        "ocf_margin": _safe_div(operating_cash_flow, total_revenue),
        "ocf_to_liabilities": _safe_div(operating_cash_flow, total_liabilities),
    }

    return ratios
