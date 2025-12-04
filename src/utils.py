from typing import Any, Dict, List, Tuple
import pandas as pd  # Import pandas for DataFrame type hint


def _coerce_float(value: Any) -> float:
    """
    Converte um valor para float de forma segura. Retorna 0.0 se a conversão falhar.
    """
    if value is None:
        return 0.0
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0


def _safe_div(numerator: float, denominator: float) -> float:
    return numerator / denominator if denominator else 0.0


def _calculate_reliability(
    raw_metrics: Dict[str, Any], expected_keys: List[str]
) -> Tuple[float, List[str]]:
    """
    Essa função é usada para dar uma nota ao conjunto de dados financeiros
    baseado na presença e validade dos valores esperadas.
    """
    available_keys_count = 0
    missing_keys = []

    for key in expected_keys:
        value = raw_metrics.get(key)
        if value is not None:
            try:
                float(value)  # tenta converter para float
                available_keys_count += 1
            except (ValueError, TypeError):
                missing_keys.append(key)
        else:
            missing_keys.append(key)

    total_keys = len(expected_keys)
    # this score is a simple reliability metric based on percentage of available keys
    score = (available_keys_count / total_keys) * 100 if total_keys > 0 else 0

    return round(score, 2), missing_keys


def get_value(data_source: pd.DataFrame | Dict, keys: List[str]) -> float:
    """
    Tries to read the first value from a set of possible keys in a DataFrame or Dict.
    Handles different data structures from yfinance.
    """
    if data_source is None:
        return 0.0

    # Handle DataFrame (balance_sheet, financials, cashflow)
    if isinstance(data_source, pd.DataFrame):
        if data_source.empty:
            return 0.0
        for name in keys:
            if name in data_source.index:
                try:
                    # Use .iloc[0] to get the first column value for that row
                    return float(data_source.loc[name].iloc[0].item())
                except (ValueError, TypeError, IndexError):
                    continue  # Try next key
        return 0.0

    # Handle Dictionary (info object)
    if isinstance(data_source, dict):
        for key in keys:
            value = data_source.get(key)
            if value is not None:
                try:
                    return float(value)
                except (ValueError, TypeError):
                    continue  # Try next key
        return 0.0

    return 0.0
