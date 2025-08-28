import re
import chromadb

from pathlib import Path
from typing import List, Dict, Any
from openai import OpenAI

from app.config import OPENAI_API_KEY, OPENAI_EMBEDDING_MODEL, CHROMA_PATH

client = OpenAI(api_key=OPENAI_API_KEY)


def _slugify(text: str) -> str:
    """
    Convert a string to a URL-friendly slug.

    Args:
        text (str): The input string to slugify."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")

    return text


def load_md_entries(md_path):
    """
    Load and parse book entries from a markdown file.
    Each entry starts with "## Title: <title>" and may contain a "Themes: ..." line.

    Args:
        md_path (str): Path to the markdown file.

    Returns:
        List[Dict[str, Any]]: A list of entries with title, summary, themes, and text for embedding.
    """
    content = Path(md_path).read_text(encoding="utf-8")

    pattern = r"^##\s*Title:\s*(.+?)\n(.*?)(?=^\s*##\s*Title:|\Z)"
    matches = re.finditer(pattern, content, flags=re.MULTILINE | re.DOTALL)

    entries = []
    for m in matches:
        title = m.group(1).strip()
        body = m.group(2).strip()

        themes = []
        tm = re.search(r"(?im)^\s*Teme:\s*(.+)\s*$", body)
        if tm:
            themes = [t.strip() for t in tm.group(1).split(",") if t.strip()]

        short_summary = re.split(r"(?im)^\s*Teme\s*:", body)[0].strip()

        text_for_embedding = f"Titlu: {title}\nRezumat: {short_summary}\nTeme: {', '.join(themes)}"
        entries.append({
            "title": title,
            "summary": short_summary,
            "themes": themes,
            "text": text_for_embedding
        })
    return entries


class RAGEngine:
    def __init__(self, chroma_path=CHROMA_PATH):
        self.client = chromadb.PersistentClient(path=chroma_path)
        self.col = self.client.get_or_create_collection(
            name="books",
            metadata={
                "hnsw:space": "cosine"
            }
        )

    def embed(self, texts: List[str]) -> List[List[float]]:
        resp = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=texts)
        return [d.embedding for d in resp.data]

    def ingest(self, md_path: str):
        entries = load_md_entries(md_path)
        ids, docs, metas = [], [], []
        for e in entries:
            ids.append(_slugify(e["title"]))
            docs.append(e["text"])
            metas.append({"title": e["title"], "themes": ", ".join(e["themes"])})
        embs = self.embed(docs)
        # Clear and add anew for idempotency (optional: upsert per id)
        try:
            self.col.delete(where={})
        except Exception:
            pass
        self.col.add(ids=ids, documents=docs, metadatas=metas, embeddings=embs)
        return len(entries)

    def search(self, query: str, k: int = 3):
        q_emb = self.embed([query])[0]
        res = self.col.query(query_embeddings=[q_emb], n_results=k)
        # Normalize output
        out = []
        for i in range(len(res["ids"][0])):
            out.append({
                "id": res["ids"][0][i],
                "document": res["documents"][0][i],
                "metadata": res["metadatas"][0][i],
                "distance": res.get("distances", [[None]])[0][i]
            })
        return out
