SPECIAL_NAMES = {
    "K9-   Lupis": "K9-ØØ Lupis",
    "The Fallen & The Virtuous": "The Fallen &amp; The Virtuous",
    "The Three Champions of Swordsoul": "The Three Brave Swordsouls"
}

def normalize_name(name: str) -> str:
    return SPECIAL_NAMES.get(name, name)