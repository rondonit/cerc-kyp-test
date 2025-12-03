from typing import Any, Dict

"""
Helpers to normalize raw company payloads into the structure expected by the
Jinja report template.
"""

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


def _coerce_float(value: Any) -> float:
    try:
        return float(value)
    except Exception:
        return 0.0


def normalize_company_data(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Flatten and sanitize the company payload so the template always receives
    the expected keys.
    """
    business = raw.get("business") or {}
    metrics_raw = raw.get("metrics") or {}

    metrics = {key: _coerce_float(metrics_raw.get(key, 0.0)) for key in METRIC_KEYS}

    company = {
        "company_name": raw.get("company_name") or raw.get("name") or raw.get("ticker"),
        "company_ticker": raw.get("company_ticker") or raw.get("ticker"),
        "currency": raw.get("currency"),
        "sector": raw.get("sector") or business.get("sector"),
        "industry": raw.get("industry") or business.get("industry"),
        "website": raw.get("website") or business.get("website"),
        "description": raw.get("description") or business.get("description"),
        "metrics": metrics,
    }

    return company
