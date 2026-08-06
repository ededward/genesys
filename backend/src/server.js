const express = require("express");
const path = require("path");
const db = require("./db");
const app = express();
const PORT = 3000;

app.use(express.json());

app.get("/", (req, res) => {
    res.send("Genesys backend is running!");
});

// All cards
app.get("/api/cards", (req, res) =>{
    db.all(
        "SELECT * FROM cards",
        (err, rows) => {
            if (err) {
                return res.status(500).json({
                    error: error.message
                });
            }
            res.json(rows);
        }
    );
});

// Search cards with partial name
app.get("/api/cards/search", (req, res) => {
    const query = req.query.name?.toLowerCase();

    if (!query) {
        return res.status(400).json({
            error: "Missing search query"
        });
    }

    db.all(
        `
        SELECT *
        FROM cards
        WHERE LOWER(name) LIKE ?
        `,
        [`%${query}%`],
        (err, rows) => {
            if (err) {
                return res.status(500).json({
                    error: err.message
                });
            }

            res.json(rows);
        }
    );
});

// Search card with full name
app.get("/api/cards/:name", (req, res) => {
    const name = req.params.name;

    db.get(
        `
        SELECT *
        FROM cards
        WHERE LOWER(name) = LOWER(?)
        `,
        [name],
        (err, row) => {
            if (err) {
                return res.status(500).json({
                    error: err.message
                });
            }

            if (!row) {
                return res.status(404).json({
                    error: "Card not found"
                });
            }

            res.json(row);
        }
    );
});

// All cards with Genesys points
app.get("/api/genesys", (req, res) => {
    db.all(
        `
        SELECT *
        FROM cards
        WHERE points > 0
        `,
        (err, rows) => {
            if (err) {
                return res.status(500).json({
                    error: err.message
                });
            }

            res.json(rows);
        }
    );
});

// Search cards with partial name in Genesys format
app.get("/api/genesys/search", (req, res) => {
    const query = req.query.name?.toLowerCase();

    if (!query) {
        return res.status(400).json({
            error: "Missing search query"
        });
    }

    db.all(
        `
        SELECT *
        FROM cards
        WHERE points > 0
        AND LOWER(name) LIKE ?
        `,
        [`%${query}%`],
        (err, rows) => {
            if (err) {
                return res.status(500).json({
                    error: err.message
                });
            }

            res.json(rows);
        }
    );
});

// Search card with full name in Genesys format
app.get("/api/genesys/:name", (req, res) => {
    const name = req.params.name;

    db.get(
        `
        SELECT *
        FROM cards
        WHERE points > 0
        AND LOWER(name) = LOWER(?)
        `,
        [name],
        (err, row) => {
            if (err) {
                return res.status(500).json({
                    error: err.message
                });
            }

            if (!row) {
                return res.status(404).json({
                    error: "Card not found"
                });
            }

            res.json(row);
        }
    );
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});