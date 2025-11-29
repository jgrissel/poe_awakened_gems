import requests
import json
import urllib.parse

leagues_to_try = ["Settlers of Kalguur", "Hardcore Settlers"]

target_gem = "Awakened Unleash Support"

for league in leagues_to_try:
    encoded_league = urllib.parse.quote(league)
    URL = f"https://poe.ninja/api/data/itemoverview?league={encoded_league}&type=SkillGem"

    print(f"\n--- Fetching data for league: {league} ---")
    try:
        response = requests.get(URL)
        if response.status_code != 200:
            print(f"Failed: {response.status_code}")
            continue
            
        data = response.json()
        lines = data.get('lines', [])
        print(f"Total gems found: {len(lines)}")
        
        variants = [item for item in lines if item.get('name') == target_gem]
        
        print(f"Found {len(variants)} variants for '{target_gem}':")
        for v in variants:
            print(json.dumps({
                "gemLevel": v.get('gemLevel'),
                "gemQuality": v.get('gemQuality'),
                "corrupted": v.get('corrupted'),
                "chaosValue": v.get('chaosValue'),
                "listingCount": v.get('count')
            }, indent=2))
            
    except Exception as e:
        print(f"Error: {e}")
