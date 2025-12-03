from typing import Any, Dict


def compute_ratios(company_data_json: Dict[str, Any]) -> Dict[str, float]:
    metrics = company_data_json["metrics"]

    # depois preciso achar um jeito melhor de lidar com divisões por zero que seja menos
    # verboso!
    ratios = {
        "current_ratio": metrics["current_assets"] / metrics["current_liabilities"]
        if metrics["current_liabilities"] > 0
        else 0.0,
        "debt_to_equity_ratio": metrics["total_liabilities"] / metrics["total_equity"]
        if metrics["total_equity"] > 0
        else 0.0,
        "net_margin": metrics["net_income"] / metrics["total_revenue"]
        if metrics["total_revenue"] > 0
        else 0.0,
        "roe": metrics["net_income"] / metrics["total_equity"]
        if metrics["total_equity"] > 0
        else 0.0,
    }

    return ratios
