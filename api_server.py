"""
api_server.py

Simple Flask server exposing capital lookup and enrichment via REST API.

Endpoints:
  GET /api/capital?country=us&state=California
  GET /api/enriched?capital=Sacramento
  GET /api/random?country=us

Run:
  python api_server.py
Then access http://localhost:5000/api/capital?country=us&state=california
"""
from flask import Flask, request, jsonify
from capital_lookup import find_capital, random_pick, get_fact_with_enrichment
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # enable CORS for all routes


@app.route('/api/capital', methods=['GET'])
def api_capital():
    """Lookup capital for a state/region."""
    country = request.args.get('country', 'us').lower()
    state = request.args.get('state', '')
    
    if not state:
        return jsonify({'error': 'Missing state parameter'}), 400
    
    result = find_capital(state, country)
    if not result:
        return jsonify({'error': 'Capital not found'}), 404
    
    return jsonify(result)


@app.route('/api/enriched', methods=['GET'])
def api_enriched():
    """Get enriched fact (local + Wikipedia) for a capital."""
    capital = request.args.get('capital', '')
    
    if not capital:
        return jsonify({'error': 'Missing capital parameter'}), 400
    
    enriched = get_fact_with_enrichment(capital)
    return jsonify(enriched)


@app.route('/api/random', methods=['GET'])
def api_random():
    """Get a random state/capital for a country."""
    country = request.args.get('country', 'us').lower()
    
    result = random_pick(country)
    if not result:
        return jsonify({'error': 'No data for country'}), 404
    
    return jsonify(result)


@app.route('/api/lookup', methods=['GET'])
def api_lookup():
    """Combined endpoint: find capital + get enrichment."""
    country = request.args.get('country', 'us').lower()
    state = request.args.get('state', '')
    
    if not state:
        return jsonify({'error': 'Missing state parameter'}), 400
    
    capital_result = find_capital(state, country)
    if not capital_result:
        return jsonify({'error': 'Capital not found'}), 404
    
    enriched = get_fact_with_enrichment(capital_result['capital'])
    
    return jsonify({
        'state': capital_result['state'],
        'capital': capital_result['capital'],
        'fact': enriched.get('fact', ''),
        'wikipedia_summary': enriched.get('wikipedia_summary', ''),
        'source': enriched.get('source', 'local')
    })


if __name__ == '__main__':
    print('Starting Capital Quest API server on http://localhost:5000')
    print('Endpoints:')
    print('  GET /api/capital?country=us&state=california')
    print('  GET /api/enriched?capital=Sacramento')
    print('  GET /api/random?country=us')
    print('  GET /api/lookup?country=us&state=california')
    app.run(debug=False, port=5000)
