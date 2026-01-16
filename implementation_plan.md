# Document Classification and Extraction System Plan

This project aims to automate the identification and data extraction from various document types (IDs, invoices, receipts, tax payments, property records) in JPG, PNG, and PDF formats.

## Recommendations

Based on your requirements, I recommend a **Multi-modal LLM approach (using Gemini 1.5 Flash)** with a **few-shot classification** strategy.

### Why Gemini 1.5 Flash?
- **Speed & Cost**: Fast and efficient for processing directories of images.
- **Vision Native**: Interprets visual cues in local documents (seals, logos, specific layouts).
- **Few-Shot Learning**: We will provide a few "Reference Examples" (previously classified documents) in the prompt to ensure the model recognizes the specific formats of your country.

---

## Proposed Architecture

1.  **Input Layer**:
    - **Folder Scanner**: Recursively reads images from a specified local directory.
    - **ZIP Handler**: Automatically extracts and processes files from compressed archives.
2.  **Reference Store**:
    - A directory (e.g., `examples/`) containing sample documents for each category (ID, Invoice, etc.) to guide the AI.
3.  **Classification Agent**:
    - Uses the reference documents to build a "context" for the AI, improving accuracy for specific local formats.
4.  **Output Layer**:
    - Organized output folder (e.g., `output/{category}/`) or a `results.json` log.

---

## Proposed Changes

### [Common]
- [x] Initialize Git repository.
- [x] Create `.gitignore` to exclude large image files and sensitive `.env`.
- [x] Create `README.md`.

### [Backend - Python]
The system will be a CLI-based tool or a simple script that processes batches of files.

#### [NEW] [main.py](file:///home/albert1t0/Documentos/GitHub/lector-dj/main.py)
Logic for scanning folders/extracting ZIPs and calling the Gemini API.

#### [NEW] [examples/](file:///home/albert1t0/Documentos/GitHub/lector-dj/examples/)
Folder to store the "guide" documents (one or two samples per type).

#### [NEW] [requirements.txt](file:///home/albert1t0/Documentos/GitHub/lector-dj/requirements.txt)
Dependencies:
- `google-generativeai` (for Gemini)
- `pdf2image`
- `pillow` (for image handling)
- `python-dotenv`

---

## Verification Plan

### Automated Tests
- Create a test suite that passes sample (anonymized) documents and verifies the classification accuracy.
- `pytest` for unit testing the extraction logic.

### Manual Verification
- Upload 5 different document types and verify that the system correctly identifies them.
