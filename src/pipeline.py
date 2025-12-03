import argparse
import json
import logging

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
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
    logger = logging.getLogger("pipeline")

    logger.info("Lendo dados da empresa")
    with open("data/aapl_kyp_minimal.json", encoding="utf-8") as f:
        company_data = json.load(f)

    logger.info("Calculando rácios financeiros")
    company_ratios = compute_ratios(company_data)
    logger.debug("Rácios calculados: %s", company_ratios)

    model_runner = (
        run_risk_agent_gemini if args.model == "gemini" else run_risk_agent_ollama
    )
    logger.info("Chamando o modelo (%s) para gerar o relatório", args.model)

    risk_report = model_runner(company_data, company_ratios)
    logger.info("Relatório pronto")

    output_path = "data/aapl_risk_report.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(risk_report)
    logger.info("Relatório salvo em %s", output_path)


if __name__ == "__main__":
    main()
