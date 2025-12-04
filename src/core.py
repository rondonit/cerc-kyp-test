import json
from pathlib import Path

from .data_fetcher import fetch_company_data
from .data_normalization import normalize_company_data
from .ratios import compute_ratios
from .risk_analyst import get_risk_agent


def run_complete_analysis(ticker: str, model_provider: str) -> str:
    """
    1. Fetch os dados brutos da empresa.
    2. Transforma os dados e calcula os índices financeiros (ratios).
    3. Manda os dados padronizados e os ratios para o agente LLM de risco gerar o relatório.
    """
    data_dir = Path("data")
    input_path = data_dir / f"{ticker}.json"

    # extract
    if not input_path.exists():
        raw_company_data = fetch_company_data(ticker)
        with open(input_path, "w", encoding="utf-8") as f:
            json.dump(raw_company_data, f, indent=4)
    else:
        with open(input_path, "r", encoding="utf-8") as f:
            raw_company_data = json.load(f)

    # transform
    company_data, reliability_metadata = normalize_company_data(raw_company_data)
    if reliability_metadata["missing_metrics"]:
        print(
            f"Aviso: Dados faltando para {ticker}: "
            f"{', '.join(reliability_metadata['missing_metrics'])}"
        )

    company_ratios = compute_ratios(company_data)
    model_runner = get_risk_agent(model_provider)
    risk_report = model_runner(company_data, company_ratios, reliability_metadata)

    # chama o do agente de risco
    return risk_report
