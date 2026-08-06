import sqlite3
from pathlib import Path

DB_PATH = (
    Path(__file__).parent.parent
    / "backend"
    / "database"
    / "genesys.db"
)


def get_connection():
    return sqlite3.connect(DB_PATH)


def insert_cards(cards):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO cards (id, name, type, images)
    VALUES (?, ?, ?, ?)
    ON CONFLICT(id) DO UPDATE SET
        name = excluded.name,
        type = excluded.type,
        images = excluded.images
    """

    for name, data in cards.items():
        cursor.execute(
            query,
            (
                data["id"],
                name,
                data["type"],
                data["images"]
            )
        )

    conn.commit()
    conn.close()

def update_genesys_points(genesys_cards):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE cards
    SET points = ?
    WHERE name = ?
    """

    updated = 0

    for name, data in genesys_cards.items():
        cursor.execute(
            query,
            (
                data["points"],
                name
            )
        )

        if cursor.rowcount > 0:
            updated += 1

    conn.commit()
    conn.close()

    return updated