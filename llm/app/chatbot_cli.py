import argparse
import json

from openai import OpenAI
from app.rag import RAGEngine
from pathlib import Path

from app.tools import openai_tools, get_summary_by_title
from app.config import OPENAI_API_KEY, OPENAI_CHAT_MODEL, TOP_K
from app.moderation import contains_offensive, polite_response

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = (
    "Ești un bibliotecar foarte destept, un asistent care recomandă cărți. Ți se oferă un CONTEXT "
    "cu rezultate relevante dintr-o bază locală (RAG). Alege o singură carte care se potrivește "
    "cel mai bine întrebării utilizatorului. Răspunde scurt și conversațional în română, "
    "indicând titlul exact, de ce e potrivită și temele principale. "
    "După recomandare, dacă ți se cere (sau consideri util), cheamă funcția get_summary_by_title "
    "pentru a afișa rezumatul complet."
)


def build_context_snippet(hits):
    """
    Build a context snippet from RAG search hits for use in the system prompt.

    Args:
        hits: List of search results containing metadata and document text.

    Returns:
        str: Formatted context string with book titles and document excerpts.
    """
    lines = list()
    for hit in hits:
        t = hit['metadata'].get('title', '')
        lines.append(f"- {t}: {hit['document'][:300]}...")
    return "\n".join(lines)


def chat_once(rag, question, k=TOP_K):
    """
    Handles a single chat interaction: searches RAG, builds context, sends prompt to OpenAI, and returns the answer.

    Args:
        rag: The RAG engine instance for searching documents.
        question: The user's question.
        k: Number of top results to retrieve from RAG.

    Returns:
        str: The assistant's answer, possibly including a detailed summary if requested.
    """
    if contains_offensive(question):
        return polite_response()

    hits = rag.search(question, k=k)
    context = build_context_snippet(hits)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
        {"role": "system", "content": f"CONTEXT (RAG):\n{context}"}
    ]

    resp = client.chat.completions.create(
        model=OPENAI_CHAT_MODEL,
        messages=messages,
        tools=openai_tools,
        tool_choice="auto"
    )

    chat_message = resp.choices[0].message
    answer = chat_message.content or ""

    # If the model requested a tool call, execute it and append the result
    if chat_message.tool_calls:
        for tool_call in chat_message.tool_calls:
            if tool_call.function.name == "get_summary_by_title":
                title = (tool_call.function.arguments or {}).get("title") if isinstance(tool_call.function.arguments, dict) else None
                # Some SDKs pass arguments as a JSON string; handle both
                if title is None and isinstance(tool_call.function.arguments, str):
                    # crude parse; in practice use json.loads
                    try:
                        title = json.loads(tool_call.function.arguments).get("title")
                    except Exception:
                        title = None
                if title:
                    summary = get_summary_by_title(title)
                    if summary:
                        answer = (answer or "") + f"\n\n**Rezumat detaliat — {title}:**\n{summary}"
                    else:
                        answer = (answer or "") + f"\n\n(Nu am găsit un rezumat complet pentru: {title})"
    return answer


def main():
    """
    Entry point for the Smart Librarian CLI.

    Handles command-line arguments for ingesting data, asking questions, or running an interactive REPL.
    """
    parser = argparse.ArgumentParser(description="Smart Librarian CLI")
    parser.add_argument("--ingest", action="store_true", help="Ingest book summaries into ChromaDB and exit")
    parser.add_argument("--ask", type=str, help="Pune o întrebare direct (one-shot)")
    parser.add_argument("--top_k", type=int, default=TOP_K, help="Câte rezultate să fie aduse din RAG")
    args = parser.parse_args()

    rag = RAGEngine()

    if args.ingest:
        md_path = Path(__file__).parent.parent / "data" / "book_summaries.md"
        n = rag.ingest(str(md_path))
        print(f"Ingestat {n} înregistrări în ChromaDB.")

        return

    if args.ask:
        print(chat_once(rag, args.ask, k=args.top_k))

        return

    print("Smart Librarian (CLI). Tastează 'quit' pentru ieșire.")

    while True:
        q = input("> ")
        if not q or q.lower().strip() in {"quit", "exit"}:
            break
        print(chat_once(rag, q, k=args.top_k))

if __name__ == "__main__":
    main()