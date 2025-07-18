# Safey Compliance Suite

A toolkit for automated industrial compliance checks:

1. Operating Procedure Verification `SafetyRegulationSuite/SOP-Regulation-Verifier`
   – Extracts clauses from a directory of regulatory PDFs/DOCXs, indexes them via TF-IDF, and flags any required regulations missing from your Standard Operating Procedure.
2. Piping & Instrumentation Diagram (P&ID) Verification `SafetyRegulationSuite/PID-Regulation-Verifier`
   - Detects components (valves, pumps, sensors) in engineering diagrams (P&IDs), builds a process graph, and ensures your SOP steps reference every diagram component.

---

## Features

- **Clause Extraction**: Heuristically pulls “shall/must/should” statements from hundreds of regulatory files.  
- **TF-IDF Indexing**: Builds a lightweight text index for fast similarity search, stores embeddings in a FAISS vector database.  
- **Graph Construction**: Uses YOLOv8 + OpenCV to detect P&ID symbols and infer connections with NetworkX.  
- **SOP Parsing**: Reads DOCX SOPs (paragraphs & tables) to extract component references.  
- **Discrepancy Logging**: Generates Human-readable Markdown reports viewable through a FastAPI web interface. 

---

## Installation

```bash
git clone https://github.com/Rohan-dev-C/SafetyRegulationSuite.git
cd SafetyRegulationSuite

# Python 3.12+
pip install -r requirements.txt
```
---
## Configuring `.env`

- **Claude API Key**  
  Create a file named `.env` in the project root containing:  
  ```ini
  ANTHROPIC_API_KEY="your-claude-API-key"

--- 
## Running the Pipeline - 

### Custom Configurations

Environment variables can be set to customize the program, but all variables will be set in `run_pipeline.sh` otherwise.
```bash
export PID_PATH=data/pid/diagram.pdf
export SOP_PATH=data/sop/sop.docx
export OUTPUT_DIR=output/
export YOLO_MODEL=yolov8n.pt
```

### Add Files
  - Put your SOP file(s) in data/sop/
  - Put your regulatory document(s) in data/regulatory_docs/
  - Put your P&ID(s) in data/pid/

Before you run anything - `cd ~/Your Path for This File/SafetyRegulationVerifier`

Run PID Compliance 

```bash
bash PID-Regulation-Verifier/scripts/run_pipeline.sh
```

Run SOP Compliance
```bash
bash SOP-Regulation-Verifier/scripts/run_full_pipeline.sh
```

# Testing/Output

1. Includes Unit Tests in `tests/` for all main Python scripts
2. Can Check Output in `output/graphs` and `output/logs`



