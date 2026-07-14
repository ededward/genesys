import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

GEN_URL = "https://www.yugioh-card.com/en/genesys/"
CARD_URL = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
SPECIAL_NAMES = {
    "K9-   Lupis": "K9-ØØ Lupis",
    "The Three Champions of Swordsoul": "The Three Brave Swordsouls"
}

def get_genesys_points(url: str) -> dict[str, int]:
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    card_map = {}

    # Find the table rows (name | points)
    # The site uses a simple table structure
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
        except:
            continue

        card_map[name] = points

    return card_map

def get_passcode(name: str) -> int:
    response = requests.get(
        CARD_URL,
        params = {"name": name}, 
        timeout=10
    )
    response.raise_for_status()

    data = response.json()
    return data["data"][0]["id"]

def normalize_name(name: str) -> str:
    return SPECIAL_NAMES.get(name, name)

if __name__ == "__main__":
    try:
        genesys_map = get_genesys_points(GEN_URL)
    except requests.RequestException as e:
        print(f"Failed to fetch Genesys data: {e}")
        exit(1)

    for name, points in genesys_map.items():
        fixed_name = SPECIAL_NAMES.get(name, name)

        passcode = get_passcode(fixed_name)
        print(f'{passcode} $genesys {points} -- {name}')
        """ #way to update dict
        passcode = get_passcode(name.replace(" ", "_"))

        genesys_map[name] = {
            "points": points,
            "passcode": passcode,
        }
        """
    print(len(genesys_map))