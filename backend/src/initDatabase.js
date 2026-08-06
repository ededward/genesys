const db = require("./db");

db.serialize(() => {
    db.run(`
        CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            type TEXT NOT NULL,
            images INTEGER NOT NULL,
            points INTEGER NOT NULL DEFAULT 0,
            updated_at TEXT
        )
    `);
});

db.close();