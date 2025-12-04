import argparse
from pathlib import Path
import requests

from .core import run_complete_analysis


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Pipeline de geração de relatório de risco.")
    parser.add_argument(
        "--model",
        choices=["ollama", "gemini"],
        default="gemini",
        help="Escolhe qual provider de modelo de IA usar.",
    )
    parser.add_argument(
        "--ticket",
        type=str,
        required=True,
        help="O ticker da empresa para a qual gerar o relatório (ex: AAPL, MSFT).",
    )
    parser.add_argument(
        "--pdf",
        action="store_true",
        help="Gera o Risk Report em PDF junto com o Markdown.",
    )
    return parser.parse_args()


def main() -> None:
    """
    Entrypoint para a execução do pipeline via CLI.
    """
    args = parse_args()

    try:
        report_content = run_complete_analysis(ticker=args.ticket, model_provider=args.model)

        out_dir = Path("reports")
        out_dir.mkdir(parents=True, exist_ok=True)
        output_path_md = out_dir / f"{args.ticket}_risk_report_{args.model}.md"

        with open(output_path_md, "w", encoding="utf-8") as f:
            f.write(report_content)
        print(f"Relatório Markdown salvo em {output_path_md}")

        if args.pdf:
            pdf_path = out_dir / f"{args.ticket}_risk_report_{args.model}.pdf"
            style = (
                "h1, h2 { color: MidnightBlue; font-size: 0.9em; } "
                "body { font-size: 0.85em; } "
                "table { border-collapse: collapse; } "
                "table, th, td { border: 1px solid DimGray; } "
                "th, td { text-align: left; padding: 0.5em; }"
            )
            payload = {
                "markdown": report_content,
                "css": style,
            }
            response = requests.post("https://md-to-pdf.fly.dev", data=payload, stream=True)
            with open(pdf_path, "wb") as f:
                f.write(response.content)
            print(f"Relatório PDF salvo em {pdf_path}")

    except Exception as e:
        print(f"Erro ao gerar o relatório para {args.ticket} com o modelo {args.model}: {e}")


if __name__ == "__main__":
    main()
