# Capital Quest

A small interactive webpage for children to learn capitals of regions in the United States, India, and the United Kingdom.

Files:
- `index.html` — main page
- `styles.css` — styles
- `script.js` — data and interaction (includes mappings for US, India, UK)

How to run locally:
- Open `index.html` directly in a browser, or serve with a simple HTTP server:

PowerShell / pwsh:

```pwsh
# From the folder e:\Program
cd e:\Program
python -m http.server 8000
# then open http://localhost:8000 in a browser
```

Notes:
- The page includes a speech button that uses the browser's Web Speech API to read the capital aloud.
- Data includes US states (plus D.C.), many Indian states/UTs, and the UK constituent countries.

Want me to add more fun facts, more countries, or audio pronunciations in different voices? Reply with what you'd like next.