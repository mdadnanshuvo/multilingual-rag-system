rag-multilingual-bangla/
├── app/                            # 💡 Core RAG system logic
│   ├── __init__.py
│   ├── config.py                   # Configuration settings
│   ├── loader.py                   # PDF loading & text extraction
│   ├── cleaner.py                  # Text cleaning & normalization
│   ├── chunker.py                  # Text chunking strategy
│   ├── embedder.py                 # Embedding logic
│   ├── retriever.py                # Vector DB indexing & retrieval
│   ├── generator.py                # Query + context → answer using LLM
│   ├── memory.py                   # Short-term memory handling
│   ├── pipeline.py                 # High-level RAG pipeline (load → embed → retrieve → generate)
│   └── api.py                      # FastAPI app (Bonus task)
│
├── data/                           # 📚 Raw data files
│   └── HSC26_Bangla_1st_Paper.pdf
│
├── outputs/                        # 📤 Intermediate & final outputs
│   ├── raw_text.txt
│   ├── cleaned_text.txt
│   ├── chunks.json
│   └── chroma/                     # Vector database files
│
├── notebooks/                      # 🧪 Jupyter notebooks for testing
│   └── exploration.ipynb
│
├── tests/                          # ✅ Unit tests
│   └── test_pipeline.py
│
├── README.md                       # ✅ Setup guide, usage, answers to evaluation questions
├── requirements.txt                # 📦 All dependencies
├── .gitignore
└── main.py                         # Entry point to run the app or start API
