import requests
import json

LEAGUE = "Settlers"
URL = f"https://poe.ninja/api/data/itemoverview?league={LEAGUE}&type=SkillGem"

print(f"Fetching data from {URL}...")
try:
    response = requests.get(URL)
    response.raise_for_status()
    data = response.json()
    
    lines = data.get('lines', [])
    print(f"Total gems found: {len(lines)}")
    
    target_gem = "Awakened Unleash Support"
    print(f"\nSearching for '{target_gem}'...")
    
    variants = [item for item in lines if item.get('name') == target_gem]
    
    print(f"Found {len(variants)} variants:")
    for v in variants:
        print(json.dumps({
            "name": v.get('name'),
            "gemLevel": v.get('gemLevel'),
            "gemQuality": v.get('gemQuality'),
            "corrupted": v.get('corrupted'),
            "chaosValue": v.get('chaosValue'),
            "listingCount": v.get('count')
        }, indent=2))
        
except Exception as e:
    print(f"Error: {e}")
