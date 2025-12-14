"""
Simple CLI wrapper around `capital_lookup.py` for interactive use.

Run `python cli.py` to start a small REPL where you can pick country,
enter state names, get capitals, and ask for a random suggestion.
Includes Wikipedia enrichment if capital_enricher.py is available.
"""
from capital_lookup import find_capital, random_pick, get_fact_with_enrichment
import textwrap


def main():
    print('Capital Quest (CLI) — US, India, UK')
    print('Type commands or "help" for instructions.')
    country = 'us'
    country_display = {'us': 'United States', 'india': 'India', 'uk': 'United Kingdom'}

    while True:
        prompt_name = country_display.get(country, country)
        cmd = input(f'[{prompt_name}]> ').strip()
        if not cmd:
            continue
        if cmd.lower() in ('quit', 'exit'):
            print('Goodbye!')
            break
        if cmd.lower() in ('help', '?'):
            print('Commands:')
            print('  country [US|India|UK]   - switch country')
            print('  find <state name>       - lookup capital for state')
            print('  random                  - pick a random state and show capital')
            print('  quit/exit               - exit')
            continue
        parts = cmd.split(maxsplit=1)
        verb = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else None

        if verb == 'country' and arg:
            arg_lower = arg.lower()
            if arg_lower in ('us', 'india', 'uk'):
                country = arg_lower
                country_display = {'us': 'United States', 'india': 'India', 'uk': 'United Kingdom'}
                print(f"Switched to {country_display.get(country, country)}")
            else:
                print('Unknown country. Use us, india, or uk.')
            continue

        if verb == 'find' and arg:
            res = find_capital(arg, country)
            if not res:
                print('No match found. Try a fuller name or use "random".')
            else:
                print(f"State/Region: {res['state']}")
                print(f"Capital: {res['capital']}")
                enriched = get_fact_with_enrichment(res['capital'])
                print(f"\nFun fact: {enriched['fact']}")
                if enriched.get('wikipedia_summary'):
                    print(f"\nMore info: {enriched['wikipedia_summary']}")
            continue

        if verb == 'random':
            res = random_pick(country)
            if not res:
                print('No data for that country.')
            else:
                print(f"State/Region: {res['state']}")
                print(f"Capital: {res['capital']}")
                enriched = get_fact_with_enrichment(res['capital'])
                print(f"\nFun fact: {enriched['fact']}")
                if enriched.get('wikipedia_summary'):
                    print(f"\nMore info: {enriched['wikipedia_summary']}")
            continue

        print('Unknown command. Type "help" for instructions.')


if __name__ == '__main__':
    main()
