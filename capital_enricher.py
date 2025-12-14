"""
capital_enricher.py

Enriches capital city facts by fetching summaries from Wikipedia using the MediaWiki API.
Includes caching to avoid redundant requests and child-friendly summary extraction.

Usage:
  from capital_enricher import get_enriched_fact
  fact_with_summary = get_enriched_fact('Jaipur')
  print(fact_with_summary)
"""
import json
import os
from urllib.request import urlopen
from urllib.error import URLError
import textwrap

CACHE_FILE = 'capital_facts_cache.json'
CACHE = {}


def load_cache():
    """Load cached Wikipedia summaries from disk."""
    global CACHE
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                CACHE = json.load(f)
        except Exception as e:
            print(f'Warning: Could not load cache: {e}')
            CACHE = {}


def save_cache():
    """Save cached Wikipedia summaries to disk."""
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(CACHE, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f'Warning: Could not save cache: {e}')


def fetch_wikipedia_summary(city_name: str, max_length: int = 200) -> str:
    """
    Fetch a summary of a city from Wikipedia using the MediaWiki API.
    
    Returns a short, child-friendly summary or empty string if unavailable.
    Results are cached in CACHE and on disk.
    """
    # check cache first
    if city_name in CACHE:
        return CACHE[city_name]
    
    try:
        # Wikipedia API endpoint
        url = (
            f'https://en.wikipedia.org/w/api.php?'
            f'action=query&titles={city_name}&prop=extracts&exintro=true&'
            f'explaintext=true&format=json'
        )
        with urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        # extract text from response
        pages = data.get('query', {}).get('pages', {})
        page_id = list(pages.keys())[0] if pages else None
        if not page_id:
            return ''
        
        extract = pages[page_id].get('extract', '').strip()
        if not extract:
            return ''
        
        # take first sentence(s) up to max_length
        sentences = extract.split('. ')
        summary = ''
        for sent in sentences:
            if len(summary) + len(sent) <= max_length:
                summary += sent + '. '
            else:
                break
        
        summary = summary.strip()
        if len(summary) > max_length:
            summary = summary[:max_length].rsplit(' ', 1)[0] + '...'
        
        # cache it
        CACHE[city_name] = summary
        save_cache()
        return summary
    except (URLError, json.JSONDecodeError, KeyError, IndexError, Exception) as e:
        # silently fail (network error, parsing, etc.)
        return ''


def get_enriched_fact(city_name: str, base_fact: str = '') -> dict:
    """
    Return a dict with 'fact' (base fact) and 'wikipedia_summary' (fetched summary).
    
    Returns: {'fact': str, 'wikipedia_summary': str, 'source': 'wikipedia'}
    """
    summary = fetch_wikipedia_summary(city_name)
    return {
        'fact': base_fact,
        'wikipedia_summary': summary,
        'source': 'wikipedia' if summary else 'local'
    }


if __name__ == '__main__':
    # Test: fetch a few cities
    load_cache()
    
    test_cities = ['Jaipur', 'New Delhi', 'London', 'Austin', 'Bengaluru']
    print('Fetching Wikipedia summaries for test cities...\n')
    
    for city in test_cities:
        result = get_enriched_fact(city)
        print(f'{city}:')
        if result['wikipedia_summary']:
            print(f"  {result['wikipedia_summary']}\n")
        else:
            print('  (No summary available)\n')
