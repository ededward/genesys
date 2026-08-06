import requests
import json
import os
from pathlib import Path
from scraper.special_name import normalize_name
from scraper.database import insert_cards

URL = "https://db.ygoprodeck.com/api/v7/cardinfo.php"

def get_cards(url: str) -> dict[str, dict[int, str, int]]:
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    cards_info = response.json()["data"]

    cards = {
        normalize_name(card["name"]): {
            "id": card["id"],
            "type": card["frameType"],
            "images": len(card["card_images"])
        }
        for card in cards_info
    }

    return cards

if __name__ == "__main__":
    cards = get_cards(URL)

    insert_cards(cards)
    print("Inserted cards into database")

    """
    # print out output file path
    filename = "cards.json"
    print(os.path.abspath(filename))
    """
    
    # save in current directory
    output_file = Path(__file__).parent / "cards.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(cards, f, ensure_ascii=False, indent=2)

    print(f"Saved to {output_file}")