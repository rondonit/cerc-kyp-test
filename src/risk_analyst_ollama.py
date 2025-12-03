import logging
import time
import ollama
from template_engine import render_template

logger = logging.getLogger(__name__)


def run_risk_agent(
    company_data: dict,
    ratios: dict,
    template_name: str = "risk_template.jinja",
    model: str = "gemma3:latest",
) -> str:
    variables = {
        "company_name": company_data["company_name"],
        "company_ticker": company_data["company_ticker"],
        "sector": company_data.get("sector"),
        "industry": company_data.get("industry"),
        "website": company_data.get("website"),
        "description": company_data.get("description"),
        "ratios": ratios,
    }
    logger.debug("Renderizando template %s", template_name)
    prompt = render_template(template_name, variables)
    logger.info("Enviando prompt para o modelo %s (chars=%d)", model, len(prompt))

    # Simplificado: não usamos streaming. Apenas indicar que o relatório está sendo gerado.
    print(
        f"Gerando relatório de risco para {company_data.get('company_name')} ({company_data.get('company_ticker')})..."
    )

    start = time.time()
    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
    logger.info("Resposta recebida em %.2fs", time.time() - start)
    return response["message"]["content"]
