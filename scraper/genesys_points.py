import requests
import json
from bs4 import BeautifulSoup
from pathlib import Path
from scraper.special_name import normalize_name
from scraper.database import update_genesys_points

CONFIG_HEADER = """#[2026.06 TCG Genesys]
# Genernated by genesys-gen
!2026.06 TCG Genesys

$genesys 100

# Genesys points
"""

LINK_PEND_HEADER = """

# Disable Pendulum and Link monsters
"""

URL = "https://www.yugioh-card.com/en/genesys/"

SKIP_LINK_PEND = {
    "Clown Crew Dristy"
}

BANNED = {
    "Dimension Shifter",
    "Dimensional Fissure"
}

def get_genesys_points(url: str) -> dict[str, int]:
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    card_map = {}

    # find the table rows (name | points)
    table = soup.find("table")
    if not table:
        raise Exception("Could not find point table on page")

    rows = table.find_all("tr")

    for row in rows[1:]:  # skip header
        cols = row.find_all("td")
        if len(cols) < 2:
            continue

        name = cols[0].get_text(strip=True)
        points_text = cols[1].get_text(strip=True)

        # extract first integer in case extra text exists
        try:
            points = int(points_text.split()[0])
        except (IndexError, ValueError):
            continue

        card_map.update({
            name: {
                "points": points
            }
        })

    return card_map

if __name__ == "__main__":
    # get cards and points list
    try:
        genesys_map = get_genesys_points(URL)
    except requests.RequestException as e:
        print(f"Failed to fetch Genesys data: {e}")
        exit(1)

    normalized_genesys_map = {
        normalize_name(name): data
        for name, data in genesys_map.items()
    }

    updated = update_genesys_points(normalized_genesys_map)
    print(f"Updated {updated} Genesys cards")

    # output Genesys json file
    output_file = Path(__file__).parent / "genesys.json"
        
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(genesys_map, f, ensure_ascii=False, indent=2)

    print(f"Saved to {output_file}")


    # get cards info
    cards_file = Path(__file__).parent / "cards.json"
    
    with open(cards_file, "r", encoding="utf-8") as f:
        cards = json.load(f)

    points_data = []
    link_and_pend = []

    # generate Genesys point list
    for name, genesys_data in genesys_map.items():
        # get fixed name if in list, otherwise get original name
        fixed_name = normalize_name(name)
        if fixed_name not in cards or fixed_name in BANNED:
            continue
 
        points_data.append(
            f'{cards[fixed_name]["id"]} $genesys {genesys_data["points"]} -- {fixed_name}'
        )

    # ban Link and Pendulum, and some cards for format custumization
    for name, card_data in cards.items():
        if name in SKIP_LINK_PEND:
            continue
        if (
            name in BANNED
            or "link" in card_data["type"].lower()
            or "pendulum" in card_data["type"].lower()
        ):
            # add alt art into the list
            x = 0
            while x < card_data["images"]:
                link_and_pend.append(
                    f'{card_data["id"] + x} 0'
                )
                x += 1

    #check for name mismatch
    missing = [
        name
        for name in genesys_map
        if normalize_name(name) not in cards
    ]

    print(f"Missing: {len(missing)}")

    for name in missing:
        print(f"Missing: {name}")

    # output config file to MDPro3
    output_file = Path(__file__).parent / "lflist_genesys.conf"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(CONFIG_HEADER)
        f.write("\n".join(points_data))
        f.write(LINK_PEND_HEADER)
        f.write("\n".join(link_and_pend))

    print(f"Saved to {output_file}")