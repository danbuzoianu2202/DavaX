import os

# Config loader for environment variables and defaults.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
OPENAI_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
CHROMA_PATH = os.getenv("CHROMA_PATH", str((os.path.dirname(__file__) + "/../chroma_db")))
TOP_K = int(os.getenv("TOP_K", "3"))
