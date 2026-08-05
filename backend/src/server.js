const express = require("express");
const fs = require("fs");
const path = require("path");

const app = express();
const PORT = 3000;

app.use(express.json());

const cardsPath = path.join(__dirname, "data", "cards.json");
const genesysPath = path.join(__dirname, "data", "genesys.json");

function loadCards() {
    return JSON.parse(
        fs.readFileSync(cardsPath, "utf-8")
    );
}

function loadGenesys() {
    return JSON.parse(
        fs.readFileSync(genesysPath, "utf-8")
    );
}

app.get("/", (req, res) => {
    res.send("Genesys backend is running!");
});

// All cards
app.get("/api/cards", (req, res) =>{
    const cards = loadCards();

    res.json(cards);
});

// Search cards with partial name
app.get("/api/cards/search", (req, res) => {
    const cards = loadCards();

    const query = req.query.name?.toLowerCase();

    if (!query) {
        return res.status(400).json({
            error: "Missing search query"
        });
    }

    const results = Object.entries(cards)
        .filter(([name]) =>
            name.toLowerCase().includes(query)
        )
        .map(([name, data]) => ({
            name,
            ...data
        }));

    res.json(results);
});

// Search card with full name
app.get("/api/cards/:name", (req, res) => {
    const cards = loadCards();
    const searchName = req.params.name.toLocaleLowerCase();
    const matchedName = Object.keys(cards).find(
        name => name.toLocaleLowerCase() === searchName
    );

    if (!matchedName) {
        return res.status(404).json({
            error: "Card not found"
        });
    }

    res.json({
        name: matchedName,
        ...cards[matchedName]
    });
})

// All cards with Genesys points
app.get("/api/genesys", (req, res) => {
    res.json(loadGenesys());
})

// Search cards with partial name in Genesys format
app.get("/api/genesys/search", (req, res) => {
    const cards = loadGenesys();

    const query = req.query.name?.toLowerCase();

    if (!query) {
        return res.status(400).json({
            error: "Missing search query"
        });
    }

    const results = Object.entries(cards)
        .filter(([name]) =>
            name.toLowerCase().includes(query)
        )
        .map(([name, points]) => ({
            name,
            points
        }));

    res.json(results);
});

// Search card with full name in Genesys format
app.get("/api/genesys/:name", (req, res) => {
    const cards = loadGenesys();
    const searchName = req.params.name.toLocaleLowerCase();
    const matchedName = Object.keys(cards).find(
        name => name.toLocaleLowerCase() === searchName
    );

    if (!matchedName) {
        return res.status(404).json({
            error: "Card not found"
        });
    }

    res.json({
        name: matchedName,
        points: cards[matchedName]
    });
})

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});