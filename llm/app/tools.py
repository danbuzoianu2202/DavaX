import json

from pathlib import Path
from typing import Optional, Dict

DATA_PATH = Path(__file__).parent.parent / "data" / "book_summaries_full.json"


def _load_dict():
    data = json.loads(Path(DATA_PATH).read_text(encoding="utf-8"))

    return data


def get_summary_by_title(title):
    db = _load_dict()
    # Case-insensitive exact match
    for k, v in db.items():
        if k.lower().strip() == title.lower().strip():
            return v

    return None


# OpenAI function/tool schema
openai_tools = [
    {
        "type": "function",
        "function": {
            "name": "get_summary_by_title",
            "description": "Returnează rezumatul complet pentru un titlu exact de carte.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Titlul exact al cărții"}
                },
                "required": ["title"]
            }
        }
    }
]
