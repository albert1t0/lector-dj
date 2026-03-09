# Document Classification and Extraction System Plan (v2)

This project aims to automate the identification and data extraction from various document types (IDs, invoices, receipts, tax payments, property records) in JPG, PNG, and PDF formats.

## Recommendations

Based on recent adjustments, we have transitioned from a cloud-only LLM setup to a **Local Multi-modal LLM approach**. We use an **OpenAI-compatible server** (e.g., LM Studio, vLLM, or Ollama) to process documents locally, ensuring data privacy and reducing costs.

### Why Local OpenAI-Compatible Server?
- **Privacy & Security**: Documents never leave your local infrastructure, which is crucial for sensitive data like IDs and Invoices.
- **Cost**: No per-API-call billing. Processing costs are limited to the hardware running the local model.
- **Portability**: The code leverages the standard `openai` Python library, making it easy to swap between local models or switch back to cloud OpenAI/Gemini (via proxies) just by changing the `OPENAI_BASE_URL`.
- **Few-Shot Learning**: We continue to provide "Reference Examples" (previously classified documents) in the prompt to ensure the model recognizes the specific formats of your country. These examples are processed natively via Base64 encoded images in Vision messages.

---

## Proposed Architecture

1.  **Input Layer**:
    - **Folder Scanner**: Recursively reads images from a specified local directory.
    - **ZIP Handler**: Automatically extracts and processes files from compressed archives.
    - **PDF Converter**: Automatically converts PDF documents into high-resolution JPG images for the LLM to process page by page.
2.  **Reference Store**:
    - A directory (e.g., `examples/`) containing sample documents for each category to guide the AI with image/text pairs.
3.  **Classification Agent**:
    - Uses the `openai` client to send Vision messages containing Base64 images directly to your local LLM inference server.
4.  **Output Layer**:
    - Generates a **JSON file** (`results.json`) with the raw extraction metadata for developers.
    - Generates a **CSV Manifest** (`manifest.csv`) for easy ingestion into spreadsheets (Excel/Sheets), databases, or quick human review.

---

## Implemented Changes

### [Backend - Python] [DONE]
The system is now a robust CLI tool that processes batches of files with high security and reliability using local models.

#### [x] [main.py](file:///home/albert1t0/Documentos/GitHub/lector-dj/main.py)
Logic for scanning folders, extracting ZIPs, encoding images natively in Base64, and calling the OpenAI-compatible API with few-shot learning. Includes dual-output generation (JSON + CSV).

#### [x] [examples/](file:///home/albert1t0/Documentos/GitHub/lector-dj/examples/)
Folder-based category system for "guide" documents used in the Vision context windows.

#### [x] [requirements.txt](file:///home/albert1t0/Documentos/GitHub/lector-dj/requirements.txt)
Dependencies streamlined: replaced `google-generativeai` with `openai` and kept standard vision processing libraries (`pdf2image`, `Pillow`).

#### [x] [.env configurations](file:///home/albert1t0/Documentos/GitHub/lector-dj/.env.example)
Variables updated to reflect local server endpoints (`OPENAI_BASE_URL`, `OPENAI_MODEL_NAME`).

---

## Phase 2: Detailed Data Extraction (Next Steps)

1.  **Field Extraction**: Move beyond simple classification to extract specific text and fields (e.g., Invoice numbers, dates, Tax IDs, names). This requires updating the system prompt and expecting structured JSON outputs from the selected local model.
2.  **Database Integration**: Ingest the generated `manifest.csv` and `results.json` directly into a structured database (SQL or NoSQL).
3.  **UI/Dashboard**: Develop a simple web interface to visualize results, review the manifest dynamically, and manually correct classification errors.

---

## Verification Plan

### Automated Tests [PASSED]
- [x] Unit tests for file handling and secure ZIP extraction (`tests/test_file_handler.py`).
- [x] Unit tests for `openai` integration, Base64 conversion, and few-shot classification using an OpenAI API mock (`tests/test_classification.py`). Tests have been updated and validated.

### Manual Verification [PENDING USER DATA]
- [ ] Spin up a local server (e.g., LM Studio) at `http://localhost:1234/v1` with a Vision-capable model.
- [ ] Run `python main.py --input <path>` with real sample documents.
- [ ] Verify the formatting of `results.json` and review the `manifest.csv` in Excel.
