# Implementation Plan - League Selection

## Goal
Allow users to select the Path of Exile league (e.g., Keepers, Standard, Hardcore Keepers) to ensure accurate pricing data.

## Proposed Changes

### Backend
1.  **[poe_client.py](file:///C:/Users/james/.gemini/antigravity/scratch/poe_gem_calc/src/poe_client.py)**
    *   Update `get_currency_prices`, `get_beast_prices`, and `get_gem_prices` to accept a `league` argument.
    *   Default to "Keepers".

2.  **[calculator.py](file:///C:/Users/james/.gemini/antigravity/scratch/poe_gem_calc/src/calculator.py)**
    *   Update `calculate_profitability` to accept a `league` argument.
    *   Pass this argument to the `poe_client` functions.

3.  **[app.py](file:///C:/Users/james/.gemini/antigravity/scratch/poe_gem_calc/src/app.py)**
    *   Update `/api/data` endpoint to read `league` from query parameters (e.g., `request.args.get('league', 'Keepers')`).
    *   Pass the league to `calculate_profitability`.

### Frontend
1.  **[index.html](file:///C:/Users/james/.gemini/antigravity/scratch/poe_gem_calc/src/templates/index.html)**
    *   Add a `<select>` dropdown in the `.controls` div.
    *   Options: "Keepers", "Standard", "Hardcore Keepers".
    *   Update `fetchData()` to get the value from the dropdown and append it to the API URL (e.g., `/api/data?league=Keepers`).

## Verification
*   Select "Keepers" -> Verify prices match user screenshot (approx 11div/247c for Awakened Unleash).
*   Select "Standard" -> Verify prices change to Standard values.
