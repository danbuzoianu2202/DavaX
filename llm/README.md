# 📚 Smart Librarian — RAG + Tool Completion

Un chatbot care recomandă cărți în funcție de interesele utilizatorului, folosind **OpenAI GPT** + **RAG cu ChromaDB**.
După recomandare, apelează un **tool** local (`get_summary_by_title`) care returnează **rezumatul complet** al cărții.

## ✅ Ce conține
- `data/book_summaries.md` — 13+ cărți cu **rezumate scurte** + teme principale
- `data/book_summaries_full.json` — **rezumate detaliate** pentru tool
- `app/rag.py` — inițializare ChromaDB, ingesție + semantic search cu embeddings OpenAI
- `app/tools.py` — tool-ul `get_summary_by_title` + schema function-calling
- `app/chatbot_cli.py` — aplicație **CLI** cu RAG + tool-calling
- `app/chatbot_streamlit.py` — interfață **Streamlit** (opțională)
- `app/moderation.py` — filtru simplu de limbaj nepotrivit (opțional)
- `app/config.py` — configurare modele și parametri
- `app/main.py` — entrypoint
- `chroma_db/` — folderul de persistență pentru Chroma (se creează la rulare)
- `requirements.txt` — dependențe

## 🔧 Cerințe
- **Python 3.10+**
- Cheie OpenAI în variabila de mediu `OPENAI_API_KEY`

```bash
# Linux/Mac
export OPENAI_API_KEY=sk-...

# Windows (PowerShell)
$Env:OPENAI_API_KEY="sk-..."
```

## ▶️ Instalare & rulare
```bash
cd smart_librarian
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 1) Ingestie în ChromaDB
python -m app.chatbot_cli --ingest

# 2) Rulare CLI (mod conversațional)
python -m app.chatbot_cli

# sau one-shot
python -m app.chatbot_cli --ask "Vreau o carte despre prietenie și magie"
```

### Streamlit (opțional)
```bash
streamlit run app/chatbot_streamlit.py
```

## 💡 Cum funcționează
1. **RAG**: întrebarea utilizatorului este transformată în embedding (OpenAI `text-embedding-3-small`) și căutată în **ChromaDB** (cosine).  
2. Primele `TOP_K` rezultate formează **CONTEXTUL** pentru modelul de chat (`gpt-4o-mini` implicit).
3. Modelul alege **o singură recomandare** și poate iniția un **tool call** către `get_summary_by_title(title)`.
4. Tool-ul întoarce **rezumatul complet** din `data/book_summaries_full.json`, care se afișează sub recomandare.

## 🧰 Tool: `get_summary_by_title(title: str) -> str`
- Implementare locală în `app/tools.py`.
- Potrivește **case-insensitive** un titlu exact din dicționarul local și întoarce rezumatul complet.

## 🧱 Moderation (opțional)
- `app/moderation.py` conține un filtru simplu bazat pe cuvinte ca să nu trimitem prompturi nepotrivite către LLM.
- Dacă mesajul conține termeni jignitori, chatbotul răspunde politicos și **nu** interoghează LLM-ul.

## 🔊 TTS / 🗣️ STT / 🖼️ Image (opțional)
- **TTS**: în varianta Streamlit se încearcă `pyttsx3` local pentru a genera un fișier WAV descărcabil.  
  (Pe unele sisteme este nevoie de drivere / voices instalate. Alternativ puteți integra OpenAI `tts-1`.)  
- **STT**: ușor de adăugat folosind OpenAI `whisper-1` (nu inclus în CLI by default).  
- **Image**: buton opțional în Streamlit pentru generarea unei imagini reprezentative cu `gpt-image-1`.

## 🧪 Exemple de întrebări
- „Vreau o carte despre **libertate** și **control social**.”  
- „Ce-mi recomanzi dacă iubesc **poveștile fantastice**?”  
- „Vreau o carte cu **prietenie** și **magie**.”  
- „Ce este **1984**?”

## 📝 Observații
- Vector store: **ChromaDB** (nu OpenAI Vector Store).  
- Dacă doriți să folosiți alt vector store, înlocuiți `RAGEngine` din `app/rag.py`.  
- Puteți extinde datasetul adăugând intrări noi în `data/book_summaries.md` și re-rulând `--ingest`.

## 🚑 Troubleshooting
- **`OPENAI_API_KEY` lipsă**: setați variabila de mediu.
- **Eroare TTS**: încercați fără TTS sau instalați drivere/voce locală.
- **Zero rezultate RAG**: creșteți `TOP_K` sau reformulați întrebarea.

---

**MOST IMPORTANT:** înțelegeți fluxul: *User → RAG retriever → GPT recomandă → Tool call pentru rezumat complet*.
