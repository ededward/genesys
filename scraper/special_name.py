SPECIAL_NAMES = {
    "K9-�� Lupis": "K9-ØØ Lupis",
    "The Three Champions of Swordsoul": "The Three Brave Swordsouls",
    "Exstellarknight Constellar Ptolemy O7": "Exstellarknight Constellar Ptolemy Ω7",
    "Calamity of the Sacred Beasts - Hamon, Lord of Striking Thunder": "Hamon, Lord of Striking Thunder - Sacred Beast of Sinful Catastrophe",
    "Infinity of the Sacred Beasts - Raviel, Lord of Phantasms": "Raviel, Lord of Phantasms - Sacred Beast of Endless Eternity",
    "Stellarnova Binding": "Stellarnova Bonds"
}

def normalize_name(name: str) -> str:
    return SPECIAL_NAMES.get(name, name)