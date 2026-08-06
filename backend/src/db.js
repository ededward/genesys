const sqlite3 = require("sqlite3").verbose();
const path = require("path");
const fs = require("fs");

const databaseDir = path.join(__dirname, "..", "database");

if (!fs.existsSync(databaseDir)) {
    fs.mkdirSync(databaseDir);
}

const dbPath = path.join(__dirname, "..", "database", "genesys.db");

const db = new sqlite3.Database(dbPath, (err) => {
    if (err) {
        console.error(err.message);
    } else {
        console.log("Connected to SQLite database.");
    }
});

module.exports = db;