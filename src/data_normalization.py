from typing import Any, Dict, Tuple
from .utils import _coerce_float, _calculate_reliability

METRIC_KEYS = [
    "total_assets",
    "total_liabilities",
    "total_equity",
    "current_assets",
    "current_liabilities",
    "total_revenue",
    "net_income",
    "operating_cash_flow",
]


def normalize_company_data(raw: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Cleans and normalizes raw company data. Returns normalized data
    and reliability metadata.
    Returns:
        company_data: dict - Normalized company data.
        reliability_metadata: dict - Metadata about data reliability.
    """
    business = raw.get("business") or {}  # avoid None
    ratios_raw = raw.get("ratios") or {}  # evita None

    # compute reliability score before calculating ratios
    reliability_score, missing_metrics = _calculate_reliability(ratios_raw, METRIC_KEYS)
    ratios = {key: _coerce_float(ratios_raw.get(key, 0.0)) for key in METRIC_KEYS}

    company = {
        "company_name": raw.get("company_name"),
        "company_ticker": raw.get("company_ticker"),
        "currency": raw.get("currency"),
        "location": raw.get("location"),
        "business": business,
        "ratios": ratios,
        "metrics": raw.get("metrics"),  # metrics are raw financial values
    }

    metadata = {
        "data_reliability_score": reliability_score,
        "missing_metrics": missing_metrics,
        "notes": "A pontuação de confiabilidade é baseada na disponibilidade e validade das métricas financeiras esperadas.",
    }

    return company, metadata
