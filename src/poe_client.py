import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://poe.ninja/api/data"

def get_currency_prices(league="Keepers"):
    """Fetches currency prices to find Vaal Orb and Gemcutter's Prism."""
    url = f"{BASE_URL}/currencyoverview?league={league}&type=Currency"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        prices = {}
        for line in data.get('lines', []):
            name = line.get('currencyTypeName')
            price = line.get('chaosEquivalent')
            if name in ["Divine Orb", "Vaal Orb", "Gemcutter's Prism"]:
                prices[name] = price
        return prices
    except Exception as e:
        print(f"Error fetching currency prices: {e}")
        return {}

def get_beast_prices(league="Keepers"):
    """Fetches beast prices to find Wild Brambleback."""
    url = f"{BASE_URL}/itemoverview?league={league}&type=Beast"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        for line in data.get('lines', []):
            if line.get('name') == "Wild Brambleback":
                return line.get('chaosValue', 0)
        return 0
    except Exception as e:
        print(f"Error fetching beast prices: {e}")
        return 0

def get_gem_prices(league="Keepers"):
    """Fetches all skill gem prices."""
    url = f"{BASE_URL}/itemoverview?league={league}&type=SkillGem"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('lines', [])
    except Exception as e:
        print(f"Error fetching gem prices: {e}")
        return []
