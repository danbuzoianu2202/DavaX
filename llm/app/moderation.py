BAD_WORDS = {
    "idiot", "stupid", "moron", "fuck", "shit", "bastard", "prost", "tâmpit"
}


def contains_offensive(text):
    """
    Check if the input text contains any offensive words.

    Args:
        text (str): The input text to check.
    """
    t = text.lower()

    return any(b in t for b in BAD_WORDS)


def polite_response():
    """Generate a polite response when offensive content is detected.

    Returns:
        str: A polite message asking the user to reformulate their question."""
    return ("Aș prefera să păstrăm conversația într-un registru politicos. "
            "Poți reformula întrebarea și te ajut cu drag.")
