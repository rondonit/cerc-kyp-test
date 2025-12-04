from flask import Flask, request, Response, jsonify
from src.core import run_complete_analysis

app = Flask(__name__)


@app.route("/analyze/<ticker>", methods=["POST"])
def analyze_ticket_and_return_md(ticker: str) -> Response:
    model = request.args.get("model", "gemini")

    try:
        report = run_complete_analysis(ticker=ticker, model_provider=model)
        return Response(report, mimetype="text/markdown")  # return markdown content directly
    except FileNotFoundError:
        response = jsonify({"detail": f"Dados para o ticket '{ticker}' não encontrados."})
        response.status_code = 404
        return response
    except Exception as e:
        response = jsonify({"detail": f"Ocorreu um erro interno: {e}"})
        response.status_code = 500
        return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
