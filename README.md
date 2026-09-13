# 🩺 AI Medical Assistant (Bedrock + Llama 3 + RAG)

A Retrieval-Augmented Generation (RAG) medical Q&A assistant. Upload a medical PDF,
it gets chunked and embedded into a FAISS vector store, and you can then ask
natural-language questions that are answered strictly from the uploaded
document's content using an AWS Bedrock LLM (Llama 3).

## Architecture

```
frontend/app.py          Streamlit UI (upload PDF, chat interface)
backend/app/
  main.py                FastAPI app entrypoint
  routes.py              /upload and /ask endpoints
  document_loader.py     Loads and splits PDF into LangChain documents
  embeddings.py          Bedrock embedding model wrapper
  vector_store.py        FAISS vector store (create / load)
  rag_pipeline.py        Retrieval + prompt construction + answer generation
  llm.py                 Bedrock LLM (Llama 3) wrapper
  config.py              Environment variable loading
backend/data/            Uploaded PDFs (includes a sample Medical_data.pdf)
backend/db/faiss_index/  Pre-built FAISS index (from the sample PDF)
```

**How it works:**
1. A PDF is uploaded through the Streamlit sidebar (or directly via the `/upload` API).
2. `document_loader.py` splits it into pages/chunks using `PyPDFLoader`.
3. `embeddings.py` calls AWS Bedrock to embed each chunk, and `vector_store.py`
   stores them in a local FAISS index.
4. When a question is asked, `rag_pipeline.py` retrieves the top 5 most
   relevant chunks, builds a strict "answer only from context" prompt, and
   sends it to Bedrock's Llama 3 model via `llm.py`.
5. The answer and source chunks are returned to the Streamlit chat UI.

## Requirements

- Python 3.11 (matches the included compiled bytecode)
- An AWS account with **Bedrock access enabled** for:
  - A text generation model (e.g. Llama 3 on Bedrock)
  - A text embedding model (e.g. Amazon Titan Embeddings)

## Setup

1. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # macOS/Linux
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file inside `backend/`** with your AWS credentials and
   model IDs (this file is NOT included in the zip and must be created manually):
   ```env
   AWS_ACCESS_KEY_ID=your_access_key_here
   AWS_SECRET_ACCESS_KEY=your_secret_key_here
   AWS_REGION=us-east-1
   BEDROCK_MODEL_ID=meta.llama3-8b-instruct-v1:0
   EMBEDDING_MODEL_ID=amazon.titan-embed-text-v1
   ```
   > ⚠️ Never commit `.env` to version control — add it to `.gitignore`.

## Running the app

Open two terminals from the project's main folder:

**Terminal 1 — Backend (FastAPI):**
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

**Terminal 2 — Frontend (Streamlit):**
```bash
cd frontend
streamlit run app.py
```

Then open the Streamlit URL shown in the terminal (usually `http://localhost:8501`).

## Usage

1. In the sidebar, upload a PDF and click **Upload** — this re-indexes the
   vector store using that document (replacing the existing index).
2. Type a question in the main panel and click **Ask**.
3. The assistant answers using only the content of the uploaded PDF, and will
   say "I don't know" if the answer isn't found in the document.

A sample PDF (`Medical_data.pdf`) and its pre-built FAISS index are already
included, so you can ask questions immediately without uploading anything first —
as long as `EMBEDDING_MODEL_ID` matches the model originally used to build it.

## Notes & things to double-check

- **Embedding model consistency:** if you switch `EMBEDDING_MODEL_ID` after the
  index was built, dimensions will mismatch. Re-upload a PDF to rebuild the index
  whenever you change the embedding model.
- **`/ask` takes `query` as a query parameter**, not a JSON body — this matches
  how the frontend calls it, but keep it in mind if you test the API directly
  (e.g. via `/docs`).
- **This is not a medical device** and should not be used for real diagnosis or
  treatment decisions — it's a document Q&A tool, and its answers are only as
  good as the source PDF and the LLM's summarization of it.
- Consider adding a `.gitignore` for `venv/`, `__pycache__/`, and `.env` before
  pushing this to GitHub.

## Author

**Gayathri** ([@Gayathri-Reddy874](https://github.com/Gayathri-Reddy874))

## License

This project is licensed under the [MIT License](LICENSE) — free to use, modify,
and distribute with attribution.
