# Pulse - Daily Summary Bot
# Fetches: weather (wttr.in) + a quote (zenquotes.io)
# Runs: every day at 8 AM IST via GitHub Actions
import requests
from datetime import date

# --- FUNCTION 1: Weather ---
def get_weather(city="Thiruvananthapuram"):
    """Fetch today's weather as a one-line text summary."""
    url = f"https://wttr.in/{city}?format=3"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text.strip()  # remove trailing whitespace/newlines
    except Exception as e:
        return f"Weather unavailable ({e})"

# --- FUNCTION 2: Quote ---
def get_quote():
    """Fetch a random motivational quote from ZenQuotes."""
    url = "https://zenquotes.io/api/random"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()  # converts JSON text to a Python List
        quote = data[0]["q"]    # the quote text
        author = data[0]["a"]   # the author name
        return f'"{quote}" - {author}'
    except Exception as e:
        return f"Quote unavailable ({e})"
    
# --- FUNCTION 3:Get currency rate  ---

def get_currency_rate():
    try:
        response = requests.get("https://open.er-api.com/v6/latest/USD")
        data = response.json()
        inr_rate = data["rates"]["INR"]
        return f"💵 1 USD = {inr_rate:.2f} INR"
    except Exception:
        return "💵 Currency rate data currently unavailable"

# --- FUNCTION 4: Build the summary ---
def build_summary():
    weather_data = get_weather()
    quote_data = get_quote()
    currency_data = get_currency_rate() # Calling the third data source
    
    # Adding the new data blank to the f-string template
    summary = f"""==========
PULSE Daily Summary
==========

WEATHER
{weather_data}

FINANCE
{currency_data}

TODAY'S QUOTE
{quote_data}
"""
    return summary
# --- FUNCTION 5: Run everything ---
def run():
    """Main entry point. Called by GitHub Actions."""
    summary = build_summary()
    
    # Print to the GitHub Actions Log (visible in the Actions tab)
    print(summary)
    
    # Save to a file (uploaded as a downloadable artifact by the workflow)
    with open("daily_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)
        
    print("Pulse ran successfully.")

# --- Entry point guard ---
if __name__ == "__main__":
    run()