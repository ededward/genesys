const db = require("./db");

db.all(
    "PRAGMA table_info(cards)",
    (err, rows) => {
        if (err) {
            console.error(err);
            return;
        }

        console.log(rows);
    }
);