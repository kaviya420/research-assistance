"""
Run this after pip install -r requirements.txt
Every line should show [OK]. If anything shows [FAIL], paste the output and we fix it.
"""

import sys

results = []

def check(name, fn):
    try:
        fn()
        results.append(("OK", name))
        print(f"  [OK]   {name}")
    except Exception as e:
        results.append(("FAIL", name, str(e)))
        print(f"  [FAIL] {name}")
        print(f"         Reason: {e}")

print("\n" + "="*55)
print("  AI Research Assistant — Setup Verification")
print("="*55 + "\n")

print(f"  Python: {sys.version}")
print(f"  Path:   {sys.executable}\n")

print("[ PDF & Text Processing ]")
check("pdfplumber",            lambda: __import__("pdfplumber"))
check("pymupdf (fitz)",        lambda: __import__("fitz"))
check("python-docx",           lambda: __import__("docx"))

print("\n[ Core NLP ]")
check("spaCy",                 lambda: __import__("spacy"))
check("spaCy English model",   lambda: __import__("spacy").load("en_core_web_sm"))
check("NLTK",                  lambda: __import__("nltk"))
check("KeyBERT",               lambda: __import__("keybert"))
check("Transformers",          lambda: __import__("transformers"))

print("\n[ Deep Learning ]")
def check_torch():
    torch = __import__("torch")
    print(f"         version: {torch.__version__}")
check("PyTorch",               check_torch)

print("\n[ Embeddings & Vector Search ]")
check("Sentence Transformers", lambda: __import__("sentence_transformers"))
check("FAISS",                 lambda: __import__("faiss"))

print("\n[ LLM & RAG ]")
check("OpenAI client",         lambda: __import__("openai"))
check("LangChain core",        lambda: __import__("langchain"))
check("LangChain OpenAI",      lambda: __import__("langchain_openai"))
check("LangChain community",   lambda: __import__("langchain_community"))

print("\n[ ML & Clustering ]")
check("scikit-learn",          lambda: __import__("sklearn"))
check("BERTopic",              lambda: __import__("bertopic"))
check("UMAP",                  lambda: __import__("umap"))
# We installed fast-hdbscan instead of hdbscan (no C compiler needed on Windows)
check("fast-hdbscan",          lambda: __import__("fast_hdbscan"))

print("\n[ Data & Visualization ]")
check("NumPy",                 lambda: __import__("numpy"))
check("Pandas",                lambda: __import__("pandas"))
check("Matplotlib",            lambda: __import__("matplotlib"))
check("Seaborn",               lambda: __import__("seaborn"))

print("\n[ Backend ]")
check("FastAPI",               lambda: __import__("fastapi"))
check("Uvicorn",               lambda: __import__("uvicorn"))
check("PyMongo",               lambda: __import__("pymongo"))

print("\n[ Utilities ]")
check("python-dotenv",         lambda: __import__("dotenv"))
check("ipykernel",             lambda: __import__("ipykernel"))
check("tqdm",                  lambda: __import__("tqdm"))
check("RAGAS",                 lambda: __import__("ragas"))

# Final summary
ok    = [r for r in results if r[0] == "OK"]
fails = [r for r in results if r[0] == "FAIL"]

print("\n" + "="*55)
print(f"  Result: {len(ok)} passed, {len(fails)} failed")
if fails:
    print("\n  Failed packages — paste this output to fix:")
    for f in fails:
        print(f"    - {f[1]}")
else:
    print("  All packages verified. You are ready for Phase 1.")
print("="*55 + "\n")