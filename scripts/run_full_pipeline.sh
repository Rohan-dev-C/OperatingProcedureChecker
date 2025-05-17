
echo ""
echo "Running compliance pipeline..."

if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

export TOKENIZERS_PARALLELISM=false

python -m src.cli data/sop/ data/regulatory_docs/
