import logging
from poe_client import get_currency_prices, get_beast_prices, get_gem_prices

logger = logging.getLogger(__name__)

def calculate_profitability(league="Keepers"):
    logger.info(f"Starting profitability calculation for league: {league}...")
    
    # 1. Fetch Data
    currency_prices = get_currency_prices(league)
    brambleback_price = get_beast_prices(league)
    all_gems = get_gem_prices(league)
    
    if not currency_prices or not brambleback_price or not all_gems:
        logger.error("Failed to fetch necessary data.")
        return []

    vaal_orb_price = currency_prices.get("Vaal Orb", 0)
    gcp_price = currency_prices.get("Gemcutter's Prism", 0)
    divine_price = currency_prices.get("Divine Orb", 1) # Avoid division by zero, though unlikely

    logger.info(f"Prices - Divine: {divine_price}c, Brambleback: {brambleback_price}c, Vaal: {vaal_orb_price}c, GCP: {gcp_price}c")

    # 2. Process Gems
    # We need to group gems by name to find different variants (Lvl 1, Lvl 5, Lvl 6)
    gems_by_name = {}
    
    for gem in all_gems:
        name = gem.get('name')
        if not name.startswith("Awakened"):
            continue
            
        if name not in gems_by_name:
            gems_by_name[name] = []
        gems_by_name[name].append(gem)

    results = []

    for name, variants in gems_by_name.items():
        # Find specific variants
        # Lvl 1: Level 1, not corrupted (Base)
        # Lvl 5: Level 5, not corrupted (Target for corruption)
        # Lvl 6: Level 6, corrupted (Success)
        # Lvl 5 Corrupted: Level 5, corrupted (Neutral outcome)
        
        lvl_1_price = float('inf')
        lvl_5_clean_price = 0
        lvl_6_price = float('inf')
        lvl_5_corrupted_price = float('inf')
        
        # Helper to get price in chaos
        def get_price(variant):
            return variant.get('chaosValue', 0)

        # Store candidates to select best match later
        lvl_6_corr_20q = []
        lvl_5_corr_20q = []
        lvl_4_corr_20q = []
        
        # Fallback buckets (any quality)
        lvl_6_corr_any = []
        lvl_5_corr_any = []
        lvl_4_corr_any = []

        for v in variants:
            level = v.get('gemLevel')
            corrupted = v.get('corrupted', False)
            quality = v.get('gemQuality', 0)
            price = get_price(v)
            
            if level == 1 and not corrupted:
                if price < lvl_1_price:
                    lvl_1_price = price
            
            elif corrupted:
                if level == 6:
                    if quality == 20: lvl_6_corr_20q.append(price)
                    else: lvl_6_corr_any.append(price)
                elif level == 5:
                    if quality == 20: lvl_5_corr_20q.append(price)
                    else: lvl_5_corr_any.append(price)
                elif level == 4:
                    if quality == 20: lvl_4_corr_20q.append(price)
                    else: lvl_4_corr_any.append(price)

        # Helper to pick best price (min)
        def get_best_price(strict_bucket, fallback_bucket):
            if strict_bucket:
                return min(strict_bucket)
            if fallback_bucket:
                return min(fallback_bucket)
            return 0

        lvl_6_price = get_best_price(lvl_6_corr_20q, lvl_6_corr_any)
        lvl_5_corrupted_price = get_best_price(lvl_5_corr_20q, lvl_5_corr_any)
        lvl_4_price = get_best_price(lvl_4_corr_20q, lvl_4_corr_any)

        # If we didn't find a base gem, skip
        if lvl_1_price == float('inf'):
            continue
            
        # Fallbacks for missing outcome data (if 0, it means NO listings found at all)
        # If lvl 5 corrupted is missing, we can't really calculate EV properly.
        # But let's leave them as 0 and the math will just show low profit.
        
        # 3. Calculate Costs
        cost_base = lvl_1_price
        cost_leveling = 4 * brambleback_price
        cost_quality = 20 * gcp_price
        total_investment_chaos = cost_base + cost_leveling + cost_quality + vaal_orb_price
        
        # 4. Calculate Expected Value (EV)
        # 1/8: +1 Level (Lvl 6)
        # 1/8: -1 Level (Lvl 4)
        # 6/8: Neutral (Lvl 5 Corrupted) - combining the 75% outcomes
        
        ev_chaos = (0.125 * lvl_6_price) + (0.75 * lvl_5_corrupted_price) + (0.125 * lvl_4_price)
        
        profit_chaos = ev_chaos - total_investment_chaos
        roi = (profit_chaos / total_investment_chaos) * 100 if total_investment_chaos > 0 else 0

        results.append({
            "name": name,
            "base_price_div": round(lvl_1_price / divine_price, 2),
            "lvl6_price_div": round(lvl_6_price / divine_price, 2),
            "investment_div": round(total_investment_chaos / divine_price, 2),
            "ev_div": round(ev_chaos / divine_price, 2),
            "profit_div": round(profit_chaos / divine_price, 2),
            "roi": round(roi, 1),
            "details": {
                "brambleback_cost": round(cost_leveling / divine_price, 2),
                "quality_cost": round(cost_quality / divine_price, 2),
                "lvl5_corrupted_price": round(lvl_5_corrupted_price / divine_price, 2)
            },
            "breakdown": {
                "prices_chaos": {
                    "base": lvl_1_price,
                    "brambleback_unit": brambleback_price,
                    "gcp_unit": gcp_price,
                    "vaal_orb": vaal_orb_price,
                    "lvl6": lvl_6_price,
                    "lvl5_corr": lvl_5_corrupted_price,
                    "lvl4": lvl_4_price
                },
                "costs_chaos": {
                    "base": cost_base,
                    "leveling": cost_leveling,
                    "quality": cost_quality,
                    "total": total_investment_chaos
                },
                "math": {
                    "ev": ev_chaos,
                    "profit": profit_chaos
                }
            },
            "validation": {
                "lvl6_count": len(lvl_6_corr_20q) + len(lvl_6_corr_any),
                "lvl6_strict": len(lvl_6_corr_20q),
                "lvl5_count": len(lvl_5_corr_20q) + len(lvl_5_corr_any),
                "lvl5_strict": len(lvl_5_corr_20q),
                "lvl4_count": len(lvl_4_corr_20q) + len(lvl_4_corr_any),
                "lvl4_strict": len(lvl_4_corr_20q)
            }
        })

    # Sort by Profit descending
    results.sort(key=lambda x: x['profit_div'], reverse=True)
    
    return results
