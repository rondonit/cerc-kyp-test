FROM python:3.13-slim

RUN pip install uv
WORKDIR /app
COPY requirements.txt .
RUN uv pip install --system --no-cache-dir -r requirements.txt

COPY src/ src/
COPY prompts/ prompts/
COPY fetch_all.sh .
COPY api.py .

ENTRYPOINT ["uv", "run", "-m", "src.cli"]
