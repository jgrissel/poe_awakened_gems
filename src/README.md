# Path of Exile Awakened Gem Profit Calculator

A tool to calculate the profitability of leveling and corrupting Awakened gems in Path of Exile.

## Features

- **Real-time Pricing**: Fetches current market data from [poe.ninja](https://poe.ninja).
- **Profit Calculation**: Calculates the Expected Value (EV) and Return on Investment (ROI) for leveling Awakened gems to level 5 and corrupting them.
- **Detailed Breakdown**: Provides a detailed breakdown of costs (Base gem, Brambleback, GCP, Vaal Orb) and potential outcomes (Level 6, Level 5 Corrupted, Level 4).
- **League Selection**: Supports different leagues (e.g., Standard, Keepers).

## Prerequisites

- Python 3.x
- `pip` (Python package installer)

## Installation

1.  Clone the repository or download the source code.
2.  Navigate to the project directory:
    ```bash
    cd src
    ```
3.  Install the required Python packages:
    ```bash
    pip install requests flask
    ```

## Usage

1.  Start the Flask application:
    ```bash
    python app.py
    ```
2.  Open your web browser and navigate to:
    ```
    http://127.0.0.1:5000/
    ```
3.  The application will load and display a table of Awakened gems sorted by profitability. You can select the league from the dropdown menu.

## Project Structure

-   `app.py`: The main Flask application entry point.
-   `calculator.py`: Contains the logic for fetching data and calculating profitability.
-   `poe_client.py`: Handles API requests to poe.ninja.
-   `templates/index.html`: The frontend HTML/JavaScript for displaying the data.

## Logic

The calculator assumes the following for the "Vaal Orb" corruption outcome on an Awakened Gem:
-   **1/8**: +1 Level (Success: Level 6)
-   **1/8**: -1 Level (Failure: Level 4)
-   **6/8**: No Level Change (Neutral: Level 5 Corrupted) - *Note: This simplifies the actual outcomes which include quality changes, but effectively groups all non-level-changing outcomes.*

Prices are fetched for:
-   **Level 1 (Clean)**: Base cost.
-   **Level 6 (Corrupted)**: Success outcome value.
-   **Level 5 (Corrupted)**: Neutral outcome value.
-   **Level 4 (Corrupted)**: Failure outcome value.

Cost includes:
-   Base Gem Price
-   Leveling Cost (4x Wild Brambleback beasts)
-   Quality Cost (20x Gemcutter's Prisms)
-   Corruption Cost (1x Vaal Orb)
