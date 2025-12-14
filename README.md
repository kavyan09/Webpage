# Capital Quest

An interactive learning tool for children to explore capital cities of US states, Indian states/UTs, and UK countries. Features comprehensive fun facts and Wikipedia enrichment.

## Project Files

- `index.html` – Main interactive webpage
- `styles.css` – Child-friendly responsive styling
- `script.js` – JavaScript client for the webpage (fetches data from API)
- `capital_lookup.py` – Core data and lookup functions
- `capital_enricher.py` – Wikipedia API integration for enriched facts
- `cli.py` – Interactive command-line tool
- `api_server.py` – Flask REST API server (serves data to the webpage)

## Quick Start

### Option 1: Python CLI (No server needed)

```bash
python cli.py
```

Then use commands:
```
country us
find california
random
quit
```

### Option 2: Interactive Webpage (with API enrichment)

1. **Install dependencies:**
   ```bash
   pip install flask flask-cors
   ```

2. **Start the API server** (in one terminal):
   ```bash
   python api_server.py
   ```
   The server will run on `http://localhost:5000`

3. **Start a simple web server** (in another terminal, from the same folder):
   ```bash
   python -m http.server 8000
   ```

4. **Open your browser:**
   - Navigate to `http://localhost:8000/index.html`
   - Select a country, enter a state name, and click "Find Capital"
   - Click "Surprise Me!" for a random capital
   - Use the 🔊 button to hear the capital name spoken aloud (if supported by your browser)

## Features

- **Interactive search:** Find capitals by state/region name (with auto-suggestions)
- **Comprehensive fun facts:** Every capital has an engaging, child-friendly fact
- **Wikipedia enrichment:** Optional integration with Wikipedia for additional info (requires internet)
- **Speech synthesis:** Hear capital names read aloud
- **Multiple countries:** US (51 regions), India (28 states + UTs), UK (4 constituent countries)
- **Responsive design:** Works on phones, tablets, and desktop

## API Endpoints

If running `api_server.py`, you can call:

```
GET /api/capital?country=us&state=california
GET /api/enriched?capital=Sacramento
GET /api/random?country=us
GET /api/lookup?country=us&state=california
```

Example:
```bash
curl "http://localhost:5000/api/lookup?country=us&state=california"
```

## Notes

- **Caching:** Wikipedia summaries are cached in `capital_facts_cache.json` to avoid repeated API calls.
- **Offline mode:** The webpage works offline with local fun facts; Wikipedia enrichment requires internet.
- **Browser support:** Web Speech API (🔊 button) works in Chrome, Edge, Safari. Firefox support is limited.

## Data Coverage

- **US:** All 50 states + District of Columbia
- **India:** All 28 states + 8 Union Territories
- **UK:** England, Scotland, Wales, Northern Ireland

---

Made for curious kids! 🌍