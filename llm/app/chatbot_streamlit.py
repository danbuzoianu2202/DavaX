import streamlit as st

from openai import OpenAI
from app.rag import RAGEngine

from app.tools import openai_tools, get_summary_by_title
from app.config import OPENAI_API_KEY, OPENAI_CHAT_MODEL, TOP_K
from app.moderation import contains_offensive, polite_response

st.set_page_config(page_title="Smart Librarian", page_icon="📚")
st.title("📚 Smart Librarian — RAG + Tool Completion")

client = OpenAI(api_key=OPENAI_API_KEY)
rag = RAGEngine()

with st.sidebar:
    st.header("Setări")
    top_k = st.slider("Top K rezultate RAG", 1, 5, TOP_K)
    do_tts = st.checkbox("Generează audio (TTS) — opțional", value=False)
    do_image = st.checkbox("Generează imagine reprezentativă — opțional", value=False)

q = st.text_input("Întreabă-mă despre ce fel de carte vrei:", placeholder="Ex: Vreau o carte despre prietenie și magie")


def run_chat(question: str):
    if contains_offensive(question):
        return polite_response()

    hits = rag.search(question, k=top_k)
    context = "\n".join(f"- {h['metadata'].get('title','')}: {h['document'][:300]}..." for h in hits)

    messages = [
        { "role": "system", "content": "Ești Smart Librarian, un asistent care recomandă cărți pe baza CONTEXTULUI local (RAG). Alege o singură carte, răspunde în română, concis." },
        { "role": "user", "content": question },
        { "role": "system", "content": f"CONTEXT (RAG):\n{context}" }
    ]

    resp = client.chat.completions.create(
        model=OPENAI_CHAT_MODEL,
        messages=messages,
        tools=openai_tools,
        tool_choice="auto"
    )
    msg = resp.choices[0].message
    answer = msg.content or ""
    title_for_tool = None

    if msg.tool_calls:
        for tc in msg.tool_calls:
            if tc.function.name == "get_summary_by_title":
                import json
                args = tc.function.arguments
                if isinstance(args, str):
                    try:
                        args = json.loads(args)
                    except Exception:
                        args = {}
                title_for_tool = args.get("title")

    if title_for_tool:
        det = get_summary_by_title(title_for_tool)
        if det:
            answer += f"\n\n**Rezumat detaliat — {title_for_tool}:**\n{det}"

    return answer

if st.button("Recomandă"):
    if not q.strip():
        st.warning("Te rog introdu o întrebare.")
    else:
        out = run_chat(q.strip())
        st.markdown(out)

        if do_tts:
            try:
                import pyttsx3
                tts = pyttsx3.init()
                tts.save_to_file(out, "smart_librarian_tts.wav")
                tts.runAndWait()
                with open("smart_librarian_tts.wav", "rb") as f:
                    st.download_button("Descarcă audio (WAV)", f, file_name="smart_librarian.wav")
            except Exception as e:
                st.info(f"TTS local indisponibil: {e}")

        if do_image:
            # Simplă integrare cu OpenAI image generation
            img = client.images.generate(model="gpt-image-1", prompt=f"Create a book-cover style illustration for: {q.strip()}", size="1024x1024")
            import base64
            if hasattr(img.data[0], "b64_json") and img.data[0].b64_json:
                from base64 import b64decode
                img_bytes = b64decode(img.data[0].b64_json)
                st.image(img_bytes, caption="Copertă / imagine sugestivă")
            elif hasattr(img.data[0], "url") and img.data[0].url:
                st.image(img.data[0].url, caption="Copertă / imagine sugestivă")