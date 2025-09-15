from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict
from sitemap_loader import load_from_sitemap
import threading

SITEMAP_URL = "https://loboandco.com/page-sitemap.xml"
BRAND_NAME = "Lobo and Company"

app = FastAPI(title=f"{BRAND_NAME} Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

knowledge_base: List[Dict[str, str]] = []
lock = threading.Lock()

class Question(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": f"{BRAND_NAME} Chatbot funcionando 🚀", "sitemap": SITEMAP_URL}

@app.get("/health")
def health():
    return {"ok": True, "pages_indexed": len(knowledge_base)}

@app.post("/chat")
def chat(q: Question):
    query = (q.question or "").strip().lower()
    if not query:
        return {"answer": "Hazme una pregunta sobre el contenido del sitio."}

    hits = []
    with lock:
        for page in knowledge_base:
            text = page["text"].lower()
            if any(tok in text for tok in query.split()):
                snippet = page["text"][:360]
                hits.append({"url": page["url"], "snippet": snippet})

    if not hits:
        return {"answer": f"No encontré información exacta. Intenta con otras palabras o revisa el sitio: {SITEMAP_URL}"}

    return {"brand": BRAND_NAME, "results": hits[:5]}

@app.post("/reload")
def reload_kb():
    global knowledge_base
    pages = load_from_sitemap(SITEMAP_URL)
    with lock:
        knowledge_base = pages
    return {"reloaded": True, "pages": len(knowledge_base)}

@app.on_event("startup")
def startup_event():
    global knowledge_base
    pages = load_from_sitemap(SITEMAP_URL)
    with lock:
        knowledge_base = pages
