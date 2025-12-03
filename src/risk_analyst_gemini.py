import time
import os
from dotenv import load_dotenv
from data_normalization import normalize_company_data
from template_engine import render_template
import google.genai as genai

load_dotenv()


def _get_api_key() -> str:
    api_key = (
        os.environ.get("GOOGLE_API_KEY")
        or os.environ.get("GENAI_API_KEY")
        or os.environ.get("GEMINI_API_KEY")
    )
    if not api_key:
        raise RuntimeError(
            "Informe a chave da API do Gemini em GOOGLE_API_KEY, GENAI_API_KEY ou GEMINI_API_KEY."
        )
    return api_key


def run_risk_agent(
    company_data: dict,
    ratios: dict,
    template_name: str = "report_template.jinja",
    model: str = "gemini-2.5-flash",
) -> str:
    company = normalize_company_data(company_data)

    variables = {
        "company": company,
        "ratios": ratios,
    }

    prompt = render_template(template_name, variables)

    # Apenas informar ao usuário (sem logs/streaming)
    print(
        f"Gerando relatório de risco para {company.get('company_name')} "
        f"({company.get('company_ticker')})..."
    )

    client = genai.Client(api_key=_get_api_key())
    start = time.time()
    response = client.models.generate_content(model=model, contents=prompt)

    elapsed = time.time() - start
    print(f"Relatório pronto (gerado em {elapsed:.2f}s).")

    return response.text
