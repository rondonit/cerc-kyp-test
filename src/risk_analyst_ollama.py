import logging
import time
import ollama
from data_normalization import normalize_company_data
from template_engine import render_template

logger = logging.getLogger(__name__)


def run_risk_agent(
    company_data: dict,
    ratios: dict,
    template_name: str = "report_template.jinja",
    model: str = "gemma3:latest",
) -> str:
    company = normalize_company_data(company_data)
    variables = {
        "company": company,
        "ratios": ratios,
    }
    logger.debug("Renderizando template %s", template_name)
    prompt = render_template(template_name, variables)
    logger.info("Enviando prompt para o modelo %s (chars=%d)", model, len(prompt))

    # Simplificado: não usamos streaming. Apenas indicar que o relatório está sendo gerado.
    print(
        f"Gerando relatório de risco para {company.get('company_name')} ({company.get('company_ticker')})..."
    )

    start = time.time()
    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
    logger.info("Resposta recebida em %.2fs", time.time() - start)
    return response["message"]["content"]
