# Multilingual RAG System 

## 📄 Project Overview

This project implements a **Retrieval-Augmented Generation (RAG)** pipeline that answers questions in **both Bangla and English** based on a Bangla PDF textbook (HSC26 Bangla 1st Paper). It supports semantic search, Gemini-based answer generation, automatic translation, source-grounded evaluation, and exposes a REST API.

---

## 🛠️ Setup Guide


### 1. Install System Dependencies (Tesseract + Poppler)

These tools must be installed separately on your system and added to your PATH.

#### 🔹 Windows

- **Tesseract:**
  - Download from: https://github.com/tesseract-ocr/tesseract/wiki
  - Add the `tesseract.exe` folder (e.g., `C:\Program Files\Tesseract-OCR`) to your System PATH

- **Poppler:**
  - Download from: https://github.com/oschwartz10612/poppler-windows/releases/
  - Extract and add the `bin/` directory (e.g., `C:\poppler\bin`) to your System PATH

#### 🔹 macOS

```bash
brew install tesseract
brew install poppler
```

#### 🔹 Ubuntu / Debian

```bash
sudo apt update
sudo apt install tesseract-ocr poppler-utils
```

---


### 2. Clone the repository

```bash
git clone https://github.com/mdadnanshuvo/multilingual-rag-system.git
cd multilingual-rag-system
```

### 3. Create virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 4. Add your Gemini API key

Create a `.env` file:

```env
GEMINI_API_KEY=your-gemini-api-key
```

### 5. Run the FastAPI server

```bash
uvicorn app.main:app --reload
```

Visit: `http://localhost:8000/docs` for interactive Swagger UI.

---


## 📊 Used Tools, Libraries, and Packages

| Component           | Technology Used                                        |
| ------------------- | ------------------------------------------------------ |
| PDF Text Extraction | `PyMuPDF (fitz)` and `pytesseract` (fallback for OCR) |
| OCR Support         | `pdf2image`, `Pillow`, `pytesseract`                  |
| Text Cleaning       | Custom regex and line break logic                     |
| Chunking            | Character-based overlapping chunks                    |
| Embedding           | `sentence-transformers` with `paraphrase-multilingual-MiniLM-L12-v2` |
| Vector DB           | In-memory FAISS store                                 |
| RAG Answering       | Google Gemini Pro API (via REST)                      |
| Evaluation          | Keyword matching + Cosine similarity (semantic)       |
| Translation         | `deep-translator` (Bangla ⇄ English)                  |
| API Framework       | `FastAPI`                                             |


---

## 📝 Sample Queries and Outputs

**Sample 1**
![image1](outputs/sample_output1.png)

**Sample 2**
![image2](outputs/sample_output2.png)

**Sample 3**
![image3](outputs/sample_output3.png)

---

## 📆 API Documentation


### ⬆️ POST `/upload`

- **Purpose:** Upload and process a Bangla PDF. It extracts, cleans, chunks, embeds, and indexes the text.
- **Request:** A PDF file (`multipart/form-data`)
- **Response:**
  ```json
  {
    "message": "Text successfully extracted and indexed from PDF.",
    "total_chunks": 123
  }

### ❓ POST `/ask`

- **Purpose:** Ask a question in Bangla or English. The system retrieves relevant chunks and generates an answer using Gemini.

- **Input:**
  ```json
  {
    "question": "string"
  }
  ```

- **Response:**
  ```json
  {
    "question": "...",
    "answer": "..."
  }
  ```

  ### 📊 GET `/evaluate`

- **Purpose:** Runs evaluation over predefined queries using:
  - ✅ Keyword matching
  - ✅ Cosine similarity between answer and retrieved context

- **Response:**
  ```json
  {
    "status": "completed",
    "total": 4,
    "results": [
      {
        "question": "Who is referred to as Anupam's god of fortune?",
        "answer": "Anupam refers to his uncle as his god of fortune...",
        "expected_keywords": ["Anupam", "fortune", "god", "uncle", "mama"],
        "score": 0.8,
        "groundedness_score": 0.84
      }
      // ... further results
    ]
  }
  ```
### ✅ GET `/health`

- **Purpose:** Health check for the server.
- **Response:** `{ "status": "ok" }`

---


## 🔢 Evaluation Matrix

Implemented metrics:

| Metric                 | Description                                            |
| ---------------------- | ------------------------------------------------------ |
| **Keyword Score**      | Ratio of expected keywords found in the answer         |
| **Groundedness Score** | Cosine similarity between answer and retrieved context |

Sample output:

```json
{
  "question": "Who is referred to as Anupam's god of fortune?",
  "answer": "Anupam refers to his uncle as his god of fortune...",
  "score": 0.8,
  "groundedness_score": 0.84
}
```

---

## 👀 Q&A Section

### ✏️ What method or library did you use to extract the text, and why?

We initially used **PyMuPDF** (fitz) for text extraction due to its structured and programmatic access to PDF content. However, since the Bangla text in the HSC PDF was not selectable or well-encoded, the output was noisy and unreadable.
As a result, we switched to OCR using **pdf2image** + **pytesseract**, which rendered each PDF page as an image and then extracted text from those images. This approach gave significantly better results for the scanned Bangla content, despite requiring more preprocessing.


### ✏️ What chunking strategy did you use? Why?

We used **character-based overlapping chunking**, where each chunk is **500 characters long with a 50-character overlap**. This strategy was chosen because the text extracted from the scanned Bangla PDF (via OCR) often had broken or inconsistent sentence structures, making sentence-based chunking unreliable.

Character-based chunking ensures that:

- Important context is preserved across chunk boundaries  
- The model gets consistent input sizes for embeddings  
- It works even when the source text lacks proper punctuation or sentence formatting

This makes it a better fit for handling noisy OCR outputs typical in scanned Bangla educational PDFs.


### ✏️ What embedding model did you use and why?

We used the `paraphrase-multilingual-MiniLM-L12-v2` model from the `sentence-transformers` library. This model was chosen because:

- It supports **multiple languages**, including Bangla and English, enabling effective cross-lingual semantic understanding.
- It provides **fast and efficient embeddings** suitable for large-scale retrieval tasks.
- It achieves **high-quality semantic similarity** performance, which improves the accuracy of retrieving relevant chunks for both Bangla and English queries.
- It balances **speed and accuracy**, making it practical for use in a real-time API service.


### ✏️ How do you compare the query with the chunks?

We embed the input query using the same `paraphrase-multilingual-MiniLM-L12-v2` model as used for the text chunks. Then, we use a FAISS **IndexFlatL2** index to perform a nearest neighbor search based on the Euclidean (L2) distance between the query embedding and the stored chunk embeddings. The top-k most similar chunks (default k=3) are retrieved as the relevant context for answer generation.


### ✏️ How do you ensure meaningful comparison?

All queries and text chunks are embedded using the same `paraphrase-multilingual-MiniLM-L12-v2` model, ensuring that both reside in a shared multilingual semantic vector space. This allows meaningful similarity comparison even across Bangla and English inputs.

However, since we use fixed-size overlapping chunking based on character length (not sentence or paragraph boundaries), some chunks may split context mid-sentence, which can reduce retrieval accuracy for vague or complex queries.

To improve this, we could:
- Use **semantic-aware chunking** (e.g., sentence or paragraph-based)
- Incorporate **context windowing** during chunking
- Experiment with larger models like `LaBSE` or `multilingual-e5`


### ✏️ Do the results seem relevant? What might improve them?

The results are generally relevant, especially for well-formed queries, with cosine similarity scores often above 0.75. The use of a multilingual embedding model (`paraphrase-multilingual-MiniLM-L12-v2`) allows for effective semantic matching across Bangla and English.

However, since we use fixed-size overlapping chunks (not sentence-aware), certain results may miss context or return partial sentences. Additionally, vague or ambiguous queries may lead to suboptimal retrieval.

Potential improvements include:

- Switching to **sentence-based or paragraph-aware chunking** to preserve semantic boundaries
- Exploring **reranking** with a Gemini model or another LLM
- Trying a **stronger embedding model** (e.g., `LaBSE`, `multilingual-e5-large`)
- Expanding the top-k context window to include more potentially useful chunks


## 📊 Project Highlights

* ✅ Supports **Bangla & English** queries
* ✅ Gemini-powered answer generation
* ✅ REST API with Swagger docs
* ✅ Evaluation with keyword + cosine similarity
* ✅ Auto translation for seamless query handling

---

## 🚫 Security

* `.env` is listed in `.gitignore`, but make sure it’s not committed accidentally.
* Regenerate Gemini keys if secrets were pushed by mistake.

---


Feel free to reach out for any deployment support or enhancements!