#!/bin/bash

TICKERS=(
  "AAPL"
  "MSFT"
  "GOOGL"
  "NVDA"
  "AMZN"
  "WMT"
  "JPM"
  "V"
  "JNJ"
  "PFE"
  "XOM"
  "BA"
  "KO"
  "PETR4.SA"
  "VALE3.SA"
  "ITUB4.SA"
  "MGLU3.SA"
)

MODEL_TO_USE="gemini"

echo "Fetching data for ${#TICKERS[@]} companies."

for ticker in "${TICKERS[@]}"; do
  echo "Processing $ticker with $MODEL_TO_USE LLM model."
  
  uv run -m src.cli --ticket "$ticker" --model "$MODEL_TO_USE" --pdf
  
  sleep 1
done

echo "DONE! The data are saved in the 'data/' folder and the reports in the 'reports/' folder."