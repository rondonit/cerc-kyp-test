import argparse
import json
import logging
from pathlib import Path

from data_normalization import normalize_company_data
from ratios import compute_ratios
from risk_analyst_gemini import run_risk_agent as run_risk_agent_gemini
from risk_analyst_ollama import run_risk_agent as run_risk_agent_ollama


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Pipeline de geração de relatório de risco."
    )
    parser.add_argument(
        "--model",
        choices=["ollama", "gemini"],
        default="ollama",
        help="Escolhe qual provider de modelo usar.",
    )
    parser.add_argument(
        "--ticket",
        type=str,
        required=True,
        help="Escolhe o ticket da empresa para a qual gerar o relatório.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
    logger = logging.getLogger("pipeline")

    # Quero gerar o relatorio para a empresa escolhida como argumento
    logger.info("Carregando dados financeiros para %s", args.ticket)
    input_path = Path("company_data") / f"{args.ticket}.json"
    with open(input_path, "r", encoding="utf-8") as f:
        raw_company_data = json.load(f)
    company_data = normalize_company_data(raw_company_data)
    logger.debug("Dados carregados e normalizados: %s", company_data)

    logger.info("Calculando ratios financeiros")
    company_ratios = compute_ratios(company_data)
    logger.debug("Ratios calculados: %s", company_ratios)

    model_runner = (
        run_risk_agent_gemini if args.model == "gemini" else run_risk_agent_ollama
    )
    logger.info("Chamando o modelo (%s) para gerar o relatório", args.model)

    risk_report = model_runner(company_data, company_ratios)
    logger.info("Relatório pronto")

    out_dir = Path("reports")
    out_dir.mkdir(parents=True, exist_ok=True)
    output_path = out_dir / f"{args.ticket}_risk_report_{args.model}.txt"
    logger.info("Salvando relatório em %s", output_path)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(risk_report)
    logger.info("Relatório salvo em %s", output_path)


if __name__ == "__main__":
    main()
