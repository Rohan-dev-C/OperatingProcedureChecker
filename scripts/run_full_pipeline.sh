#!/bin/bash

echo ""
echo "Running compliance pipeline..."

# Activate environment variables (e.g., Claude API key)
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Set tokenizers warning suppression (optional cleanup if ever using HF again)
export TOKENIZERS_PARALLELISM=false

# Run the pipeline with SOP and regulatory document paths
python -m src.cli data/sop/ data/regulatory_docs/
