"""
capital_lookup.py

Provides lookup functions for US states, Indian states/UTs, and UK constituent countries.
Includes enrichment with Wikipedia summaries via capital_enricher.py.

Usage examples:
  from capital_lookup import find_capital, random_pick, get_fact_with_enrichment
  print(find_capital('California', 'us'))
  print(get_fact_with_enrichment('Sacramento'))
"""
import random
import textwrap

try:
    from capital_enricher import get_enriched_fact
    HAS_ENRICHER = True
except ImportError:
    HAS_ENRICHER = False

DATA = {
    'us': {
        'Alabama': 'Montgomery', 'Alaska': 'Juneau', 'Arizona': 'Phoenix', 'Arkansas': 'Little Rock', 'California': 'Sacramento',
        'Colorado': 'Denver', 'Connecticut': 'Hartford', 'Delaware': 'Dover', 'Florida': 'Tallahassee', 'Georgia': 'Atlanta',
        'Hawaii': 'Honolulu', 'Idaho': 'Boise', 'Illinois': 'Springfield', 'Indiana': 'Indianapolis', 'Iowa': 'Des Moines',
        'Kansas': 'Topeka', 'Kentucky': 'Frankfort', 'Louisiana': 'Baton Rouge', 'Maine': 'Augusta', 'Maryland': 'Annapolis',
        'Massachusetts': 'Boston', 'Michigan': 'Lansing', 'Minnesota': 'St. Paul', 'Mississippi': 'Jackson', 'Missouri': 'Jefferson City',
        'Montana': 'Helena', 'Nebraska': 'Lincoln', 'Nevada': 'Carson City', 'New Hampshire': 'Concord', 'New Jersey': 'Trenton',
        'New Mexico': 'Santa Fe', 'New York': 'Albany', 'North Carolina': 'Raleigh', 'North Dakota': 'Bismarck', 'Ohio': 'Columbus',
        'Oklahoma': 'Oklahoma City', 'Oregon': 'Salem', 'Pennsylvania': 'Harrisburg', 'Rhode Island': 'Providence', 'South Carolina': 'Columbia',
        'South Dakota': 'Pierre', 'Tennessee': 'Nashville', 'Texas': 'Austin', 'Utah': 'Salt Lake City', 'Vermont': 'Montpelier',
        'Virginia': 'Richmond', 'Washington': 'Olympia', 'West Virginia': 'Charleston', 'Wisconsin': 'Madison', 'Wyoming': 'Cheyenne',
        'District of Columbia': 'Washington, D.C.'
    },
    'india': {
        'Andhra Pradesh': 'Amaravati', 'Arunachal Pradesh': 'Itanagar', 'Assam': 'Dispur', 'Bihar': 'Patna', 'Chhattisgarh': 'Raipur',
        'Goa': 'Panaji', 'Gujarat': 'Gandhinagar', 'Haryana': 'Chandigarh', 'Himachal Pradesh': 'Shimla', 'Jharkhand': 'Ranchi',
        'Karnataka': 'Bengaluru', 'Kerala': 'Thiruvananthapuram', 'Madhya Pradesh': 'Bhopal', 'Maharashtra': 'Mumbai', 'Manipur': 'Imphal',
        'Meghalaya': 'Shillong', 'Mizoram': 'Aizawl', 'Nagaland': 'Kohima', 'Odisha': 'Bhubaneswar', 'Punjab': 'Chandigarh',
        'Rajasthan': 'Jaipur', 'Sikkim': 'Gangtok', 'Tamil Nadu': 'Chennai', 'Telangana': 'Hyderabad', 'Tripura': 'Agartala',
        'Uttar Pradesh': 'Lucknow', 'Uttarakhand': 'Dehradun', 'West Bengal': 'Kolkata',
        'Andaman and Nicobar Islands': 'Port Blair', 'Chandigarh (UT)': 'Chandigarh',
        'Dadra and Nagar Haveli and Daman and Diu': 'Daman', 'Delhi': 'New Delhi', 'Jammu and Kashmir': 'Srinagar',
        'Ladakh': 'Leh', 'Puducherry': 'Puducherry', 'Lakshadweep': 'Kavaratti'
    },
    'uk': {
        'England': 'London', 'Scotland': 'Edinburgh', 'Wales': 'Cardiff', 'Northern Ireland': 'Belfast'
    }
}

FUN_FACTS = {
    # US Capitals
    'Montgomery': 'Montgomery is famous for the Civil Rights movement and has beautiful historic sites.',
    'Juneau': 'Juneau is Alaska\'s capital and can only be reached by plane or boat!',
    'Phoenix': 'Phoenix is one of the hottest US cities with desert landscapes and Native American culture.',
    'Little Rock': 'Little Rock is known for its role in Civil Rights history and beautiful parks.',
    'Sacramento': 'Sacramento started as a Gold Rush town and has a historic riverfront.',
    'Denver': 'Denver is nicknamed the "Mile High City" because it sits exactly 1 mile above sea level!',
    'Hartford': 'Hartford is home to the oldest continuously published newspaper in the US.',
    'Dover': 'Dover is one of the oldest cities in the US with colonial-era buildings.',
    'Tallahassee': 'Tallahassee is surrounded by beautiful forests and natural springs.',
    'Atlanta': 'Atlanta is known for being a major hub and played a key role in Civil Rights history.',
    'Honolulu': 'Honolulu is on the island of Oahu and is famous for beaches like Waikiki.',
    'Boise': 'Boise sits in a valley surrounded by mountains and is a great outdoor adventure city.',
    'Springfield': 'Springfield is the capital of Illinois and has lots of Abraham Lincoln sites to visit.',
    'Indianapolis': 'Indianapolis is famous for the Indy 500 car race and has cool racing museums!',
    'Des Moines': 'Des Moines is in the heart of farm country and has great science museums.',
    'Topeka': 'Topeka is the capital of Kansas and has beautiful sunflower fields nearby.',
    'Frankfort': 'Frankfort is known for bourbon distilleries and historic Main Street.',
    'Baton Rouge': 'Baton Rouge sits on the mighty Mississippi River with Southern charm.',
    'Augusta': 'Augusta is Maine\'s capital and is close to beautiful lakes and outdoor activities.',
    'Annapolis': 'Annapolis is home to the US Naval Academy and has historic colonial streets.',
    'Boston': 'Boston is famous for the Freedom Trail and being the birthplace of the American Revolution!',
    'Lansing': 'Lansing is Michigan\'s capital and is surrounded by Great Lakes and natural beauty.',
    'St. Paul': 'St. Paul sits across the Mississippi River from Minneapolis and has fantastic museums.',
    'Jackson': 'Jackson is Mississippi\'s capital and has important Civil Rights museums.',
    'Jefferson City': 'Jefferson City sits on the Missouri River and is named after Thomas Jefferson.',
    'Helena': 'Helena is Montana\'s capital surrounded by beautiful mountains and outdoor adventures.',
    'Lincoln': 'Lincoln is Nebraska\'s capital and is home to the Cornhuskers university.',
    'Carson City': 'Carson City is Nevada\'s capital and was named after the famous frontiersman Kit Carson.',
    'Concord': 'Concord is New Hampshire\'s capital and has a beautiful state house building.',
    'Trenton': 'Trenton sits on the Delaware River and has important Revolutionary War history.',
    'Santa Fe': 'Santa Fe has beautiful Pueblo-style architecture and amazing art galleries and museums!',
    'Albany': 'Albany is one of the oldest surviving settlements of the original British thirteen colonies.',
    'Raleigh': 'Raleigh is North Carolina\'s capital and has beautiful museums and gardens.',
    'Bismarck': 'Bismarck is North Dakota\'s capital on the Missouri River with scenic views.',
    'Columbus': 'Columbus is Ohio\'s largest city and has great science and natural history museums.',
    'Oklahoma City': 'Oklahoma City has a fascinating history and beautiful memorials.',
    'Salem': 'Salem is Oregon\'s capital and was founded as a fur trading post.',
    'Harrisburg': 'Harrisburg sits on the Susquehanna River and has historic Pennsylvania history.',
    'Providence': 'Providence is Rhode Island\'s capital and has beautiful colonial architecture.',
    'Columbia': 'Columbia is South Carolina\'s capital and has beautiful historic districts.',
    'Pierre': 'Pierre is South Dakota\'s capital and sits on the Missouri River.',
    'Nashville': 'Nashville is famous as "Music City USA" and has the Grand Ole Opry!',
    'Austin': "Austin is famous for live music and concerts — 'Keep Austin Weird' is its motto!",
    'Salt Lake City': 'Salt Lake City is surrounded by mountains and hosted the 2002 Winter Olympics.',
    'Montpelier': 'Montpelier is Vermont\'s capital and is surrounded by beautiful forests and mountains.',
    'Richmond': 'Richmond is Virginia\'s capital and has important American history and museums.',
    'Olympia': 'Olympia is Washington\'s capital and sits on Puget Sound with scenic views.',
    'Charleston': 'Charleston is West Virginia\'s capital and sits on the Kanawha River.',
    'Madison': 'Madison is Wisconsin\'s capital and sits between two beautiful lakes.',
    'Cheyenne': 'Cheyenne is Wyoming\'s capital and has a great frontier heritage.',
    'Washington, D.C.': 'Washington, D.C. is the capital of the USA and has amazing free museums and monuments!',
    # India Capitals
    'Amaravati': 'Amaravati is an ancient city with temples and is known for silk production.',
    'Itanagar': 'Itanagar is surrounded by mountains and forests in northeast India.',
    'Dispur': 'Dispur is Assam\'s capital and is known for tea gardens nearby.',
    'Patna': 'Patna is an ancient city on the Ganges River with Buddhist heritage sites.',
    'Raipur': 'Raipur is known for steel production and has beautiful temples.',
    'Panaji': 'Panaji is a beautiful coastal city with Portuguese colonial architecture.',
    'Gandhinagar': 'Gandhinagar is a planned city named after Mahatma Gandhi.',
    'Chandigarh': 'Chandigarh is a beautiful planned city with great architecture and gardens.',
    'Shimla': 'Shimla is a hill station with cool weather and beautiful mountain views!',
    'Ranchi': 'Ranchi is surrounded by waterfalls and beautiful natural scenery.',
    'Bengaluru': 'Bengaluru is India\'s tech hub — the "Silicon Valley of India" with IT companies!',
    'Thiruvananthapuram': 'Thiruvananthapuram has beautiful beaches and is known for spices.',
    'Bhopal': 'Bhopal is known for beautiful lakes and historic palaces.',
    'Mumbai': "Mumbai is India's largest city and is famous for Bollywood movies!",
    'Imphal': 'Imphal is in a beautiful valley surrounded by mountains.',
    'Shillong': 'Shillong is a hill station known as the "Scotland of the East" with cool weather.',
    'Aizawl': 'Aizawl is a beautiful hill city with scenic mountain views.',
    'Kohima': 'Kohima is a hill station surrounded by beautiful landscapes.',
    'Bhubaneswar': 'Bhubaneswar is known for ancient temples and beautiful beaches nearby.',
    'Jaipur': 'Jaipur is the famous "Pink City" with beautiful palaces and amazing forts nearby!',
    'Gangtok': 'Gangtok is a hill station with mountain views and Buddhist monasteries.',
    'Chennai': 'Chennai has beautiful temples and a long coastline on the Bay of Bengal.',
    'Hyderabad': 'Hyderabad is known for pearls, biryani food, and IT industry.',
    'Agartala': 'Agartala is known for beautiful palaces and temples.',
    'Lucknow': 'Lucknow is known for beautiful Mughal architecture and amazing biryani food!',
    'Dehradun': 'Dehradun is a hill city with yoga centers and nature all around.',
    'Kolkata': 'Kolkata is known for literature, art, and is the "City of Joy"!',
    'Port Blair': 'Port Blair is on the Andaman Islands with beautiful beaches.',
    'Daman': 'Daman has beautiful beaches and Portuguese colonial architecture.',
    'New Delhi': 'New Delhi is India\'s capital with India Gate, palaces, and amazing monuments!',
    'Srinagar': 'Srinagar is in Kashmir and is famous for beautiful houseboats and gardens.',
    'Leh': 'Leh is high in the mountains of Ladakh with amazing trekking and Buddhist sites.',
    'Puducherry': 'Puducherry has beautiful beaches and French colonial architecture.',
    'Kavaratti': 'Kavaratti is in the Lakshadweep Islands with beautiful tropical beaches.',
    # UK Capitals
    'London': 'London has the famous River Thames and is full of history back to Roman times!',
    'Edinburgh': 'Edinburgh has a castle on a volcanic rock — great for imagining knights and history!',
    'Cardiff': 'Cardiff is Wales\' capital and has beautiful castles and museums.',
    'Belfast': 'Belfast is Northern Ireland\'s capital with historic architecture and museums.'
}


def normalize(s: str) -> str:
    """Normalize strings for case-insensitive matching."""
    return s.strip().lower()


def find_capital(query: str, country_key: str):
    """Find capital for a given state/region `query` in country `country_key`.

    Returns a dict with keys `state` and `capital` or `None` if not found.
    Matching strategy: exact -> startswith -> includes (case-insensitive).
    """
    if not query:
        return None
    country_key = country_key.lower()
    map_ = DATA.get(country_key)
    if not map_:
        return None
    q = normalize(query)
    # exact
    for k in map_.keys():
        if normalize(k) == q:
            return {'state': k, 'capital': map_[k]}
    # startswith
    for k in map_.keys():
        if normalize(k).startswith(q):
            return {'state': k, 'capital': map_[k]}
    # includes
    for k in map_.keys():
        if q in normalize(k):
            return {'state': k, 'capital': map_[k]}
    return None


def random_pick(country_key: str):
    """Return a random (state, capital) tuple for the given country key."""
    country_key = country_key.lower()
    map_ = DATA.get(country_key)
    if not map_:
        return None
    state = random.choice(list(map_.keys()))
    return {'state': state, 'capital': map_[state]}


def get_fact_with_enrichment(capital_name: str) -> dict:
    """Return fact + Wikipedia summary for a capital.
    
    Returns a dict with keys: 'fact', 'wikipedia_summary', 'source'.
    If enricher unavailable, returns only the local fact.
    """
    base_fact = FUN_FACTS.get(capital_name, f'{capital_name} is an interesting place to visit!')
    if HAS_ENRICHER:
        try:
            return get_enriched_fact(capital_name, base_fact)
        except Exception:
            # fallback if enricher fails
            return {'fact': base_fact, 'wikipedia_summary': '', 'source': 'local'}
    return {'fact': base_fact, 'wikipedia_summary': '', 'source': 'local'}


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Lookup capital for a state/region (US, India, UK).'
    )
    parser.add_argument('--country', '-c', default='us', choices=['us', 'india', 'uk'], help='Country key (us|india|uk)')
    parser.add_argument('--state', '-s', help='State/region name to lookup')
    parser.add_argument('--random', '-r', action='store_true', help='Pick a random state in the country')

    args = parser.parse_args()

    if args.random:
        item = random_pick(args.country)
    else:
        if not args.state:
            parser.error('Either --state/-s or --random/-r must be provided')
        item = find_capital(args.state, args.country)

    if not item:
        print('No match found. Try a full state name like "California" or "Karnataka".')
    else:
        print(f"State/Region: {item['state']}")
        print(f"Capital: {item['capital']}")
        enriched = get_fact_with_enrichment(item['capital'])
        print('\nFun fact:')
        print(textwrap.fill(enriched['fact'], width=70))
        if enriched.get('wikipedia_summary'):
            print('\nMore info:')
            print(textwrap.fill(enriched['wikipedia_summary'], width=70))
