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
- [x] Create `README.md` and basic project documentation.
- [x] Publish to GitHub.

### [Backend - Python] [DONE]
The system is now a robust CLI tool that processes batches of files with high security and reliability.

#### [x] [main.py](file:///home/albert1t0/Documentos/GitHub/lector-dj/main.py)
Logic for scanning folders/extracting ZIPs and calling the Gemini API with few-shot learning.

#### [x] [examples/](file:///home/albert1t0/Documentos/GitHub/lector-dj/examples/)
Folder-based category system for "guide" documents.

#### [x] [requirements.txt](file:///home/albert1t0/Documentos/GitHub/lector-dj/requirements.txt)
All dependencies managed and tested.

---

## Phase 2: Detailed Data Extraction (Next Steps)

1.  **Field Extraction**: Move beyond classification to extract specific data (e.g., Invoice numbers, dates, Tax IDs, names).
2.  **Database Integration**: Store extracted metadata in a structured database (SQL or NoSQL).
3.  **UI/Dashboard**: Develop a simple web interface to visualize results and review classification errors.

---

## Verification Plan

### Automated Tests [PASSED]
- [x] Unit tests for file handling and secure ZIP extraction (`tests/test_file_handler.py`).
- [x] Unit tests for Gemini integration and few-shot classification with API mocking (`tests/test_classification.py`).

### Manual Verification [PENDING USER DATA]
- [ ] Upload real sample documents from your country into `input/` and verify accuracy.
