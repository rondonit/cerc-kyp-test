import os
from dotenv import load_dotenv
import google.genai as genai
import ollama
from .template_engine import render_template
import requests

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
report_language = os.getenv("REPORT_LANGUAGE", "en")
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")


def _run_gemini_agent(
    company_data: dict,
    ratios: dict,
    reliability_metadata: dict,
    template_name: str = "report_template.jinja",
    model: str = "gemini-2.5-flash-lite",  # do not cghange the model here
) -> str:
    variables = {
        "company": company_data,
        "ratios": ratios,
        "metrics": company_data.get("metrics", {}),
        "reliability": reliability_metadata,
        "language": report_language,
    }
    prompt = render_template(template_name, variables)
    client = genai.Client(api_key=gemini_api_key)
    response = client.models.generate_content(model=model, contents=prompt)
    return str(response.text)


def _run_ollama_agent(
    company_data: dict,
    ratios: dict,
    reliability_metadata: dict,
    template_name: str = "report_template.jinja",
    model: str = "gemma3:latest",
) -> str:
    variables = {
        "company": company_data,
        "ratios": ratios,
        "metrics": company_data.get("metrics", {}),
        "reliability": reliability_metadata,
    }
    prompt = render_template(template_name, variables)
    print(f"Gerando relatório de risco para {company_data.get('company_name')}")
    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]


def _run_openrouter_agent(
    company_data: dict,
    ratios: dict,
    reliability_metadata: dict,
    template_name: str = "report_template.jinja",
    model: str = "amazon/nova-2-lite-v1:free",
) -> str:
    if not model:
        model = os.getenv("OPENROUTER_MODEL", "amazon/nova-2-lite-v1:free")

    variables = {
        "company": company_data,
        "ratios": ratios,
        "metrics": company_data.get("metrics", {}),
        "reliability": reliability_metadata,
        "language": report_language,
    }

    prompt = render_template(template_name, variables)

    headers = {"Authorization": f"Bearer {openrouter_api_key}", "Content-Type": "application/json"}

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload
    )

    data = response.json()
    raw_content = data["choices"][0]["message"]["content"]
    print(raw_content)
    return raw_content


def get_risk_agent(provider: str):
    if provider == "gemini":
        return _run_gemini_agent
    elif provider == "openrouter":
        return _run_openrouter_agent
    else:
        return _run_ollama_agent
