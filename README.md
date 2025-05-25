# SOP–Regulatory Compliance Checker

A Python tool and web interface that automatically compares your Standard Operating Procedure (SOP) documents against a set of regulatory documents. Highlights discrepancies and suggests  edits.

---

## Features

- **Bulk Document Ingestion**  
  - Load one or more SOP files (`.pdf`/`.docx`)  
  - Load 10+ regulatory documents (`.pdf`/`.docx`)  

- **Clause Extraction**  
  - Splits text by Section 
  - Filters out noise and breaks each split into shorter clauses

- **TF–IDF Embeddings & FAISS**  
  - Vectorizes each clause into a 4,096-d TF–IDF embedding space  
  - Uses FAISS's extremely fast nearest-neighbor search

- **Relevance & Summaries**  
  - Uses Claude to find the most relevant clauses  
  - Generates a summary of  differences between SOP and regulations 
  - Provides 2–3 actionable bullet-point edits per clause  

- **Markdown Report**  
  - `compliance_report.md` grouping by SOP section  
  - Includes section & clause ID, source filename, regulatory text & SOP excerpt, sentence highlighting discrepancy, suggestions for edits to SOP.

- **FastAPI Web UI**  
  - Browser-based file upload for SOP & regulatory docs  
  - Renders the compliance report after running the analysis

---

## Installation

1. **Clone** the repo  
   ```bash
   git clone https://github.com/Rohan-dev-C/SafetyRegulationVerifier.git
   cd SafetyRegulationVerifier
2. Python virtual environment
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
3. Install dependencies
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt

## Configuring `.env`

- **Claude API Key**  
  Create a file named `.env` in the project root containing:  
  ```ini
  ANTHROPIC_API_KEY="your-claude-API-key"

## Running the Program
1. Add Files
  - Put your SOP file(s) in data/sop/
  - Put your regulatory document(s) in data/regulatory_docs/
2. Run in Terminal
  ```bash
  bash scripts/run_full_pipeline.sh
  ```
3. Check Results in `compliance_report.md`

## Using Web UI
1. Launch the Webapp server
   ```bash
   uvicorn src.webapp.main:app --reload
2. Open Your Browser and Open `http://localhost:8000`


