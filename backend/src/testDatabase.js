const db = require("./db");

db.all(
    `
    SELECT name, points 
    FROM cards 
    WHERE points = 6 
    LIMIT 10
    `,
    (err, rows) => {
        if (err) {
            console.error(err);
            return;
        }

        console.log(rows);
        db.close();
    }
);