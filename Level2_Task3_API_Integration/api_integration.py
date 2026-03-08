Rajput Girl, [3/8/2026 12:23 PM]
# ============================================================
#   PYTHON API INTEGRATION — Task 3 (Intermediate)
#   Features : Live Weather + Cryptocurrency Prices
#   APIs Used: OpenWeatherMap (free) + CoinGecko (free)
#   Saves    : api_report.txt
# ============================================================
#
#   BEFORE RUNNING:
#   1. Install library:
#          pip install requests
#
#   2. Get FREE weather API key:
#          Go to: https://openweathermap.org/api
#          Sign up (free) → Copy your API key
#          Paste it below where it says: API_KEY = "your_api_key_here"
#
#   CoinGecko needs NO API key — works directly!
#
# ============================================================

import requests
import json
import os
from datetime import datetime

# ============================================================
#   YOUR API KEY — PASTE IT HERE
#   Get free key from: https://openweathermap.org/api
# ============================================================
WEATHER_API_KEY = "your_api_key_here"   # <-- Replace this!

# ── Colors for terminal ──
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
BLUE   = "\033[94m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def print_success(msg): print(f"{GREEN}✅ {msg}{RESET}")
def print_error(msg):   print(f"{RED}❌ {msg}{RESET}")
def print_info(msg):    print(f"{YELLOW}ℹ️  {msg}{RESET}")
def print_section(msg): print(f"\n{BLUE}{BOLD}{'═'*52}\n   {msg}\n{'═'*52}{RESET}")


# ============================================================
#   WEATHER API — OpenWeatherMap
# ============================================================

def get_weather(city):
    print_section(f"WEATHER FOR: {city.upper()}")

    if WEATHER_API_KEY == "your_api_key_here":
        print_error("Please add your API key first!")
        print_info("Get free key from: https://openweathermap.org/api")
        return None

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q":     city,
        "appid": WEATHER_API_KEY,
        "units": "metric",    # Celsius
        "lang":  "en"
    }

    try:
        print_info(f"Fetching weather data for '{city}'...")
        response = requests.get(url, params=params, timeout=10)

        # Handle specific HTTP errors
        if response.status_code == 401:
            print_error("Invalid API key! Please check your key.")
            return None
        elif response.status_code == 404:
            print_error(f"City '{city}' not found! Please check the spelling.")
            return None

        response.raise_for_status()
        data = response.json()

        # Extract weather details
        weather = {
            "city":        data["name"],
            "country":     data["sys"]["country"],
            "temperature": data["main"]["temp"],
            "feels_like":  data["main"]["feels_like"],
            "min_temp":    data["main"]["temp_min"],
            "max_temp":    data["main"]["temp_max"],
            "humidity":    data["main"]["humidity"],
            "pressure":    data["main"]["pressure"],
            "condition":   data["weather"][0]["description"].title(),
            "wind_speed":  data["wind"]["speed"],
            "visibility":  data.get("visibility", 0) // 1000,
            "sunrise":     datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%I:%M %p"),
            "sunset":      datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%I:%M %p"),
            "fetched_at":  datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Weather emoji based on condition
        condition_lower = data["weather"][0]["main"].lower()
        emoji = {
            "clear":        "☀️",
            "clouds":       "☁️",
            "rain":         "🌧️",
            "drizzle":      "🌦️",
            "thunderstorm": "⛈️",
            "snow":         "❄️",
            "mist":         "🌫️",
            "haze":         "🌫️",
            "fog":          "🌫️",
        }.get(condition_lower, "🌡️")

Rajput Girl, [3/8/2026 12:23 PM]
# Display weather beautifully
        print(f"""
{CYAN}{BOLD}  {emoji}  {weather['city']}, {weather['country']}  {emoji}{RESET}
  {'─'*40}
  {BOLD}Condition   :{RESET}  {weather['condition']}
  {BOLD}Temperature :{RESET}  {weather['temperature']}°C  (Feels like {weather['feels_like']}°C)
  {BOLD}Min / Max   :{RESET}  {weather['min_temp']}°C  /  {weather['max_temp']}°C
  {BOLD}Humidity    :{RESET}  {weather['humidity']}%
  {BOLD}Wind Speed  :{RESET}  {weather['wind_speed']} m/s
  {BOLD}Pressure    :{RESET}  {weather['pressure']} hPa
  {BOLD}Visibility  :{RESET}  {weather['visibility']} km
  {BOLD}Sunrise     :{RESET}  {weather['sunrise']}
  {BOLD}Sunset      :{RESET}  {weather['sunset']}
  {'─'*40}
  {YELLOW}Fetched at: {weather['fetched_at']}{RESET}
        """)

        print_success("Weather data fetched successfully!")
        return weather

    except requests.exceptions.ConnectionError:
        print_error("No internet connection! Please check your network.")
    except requests.exceptions.Timeout:
        print_error("Request timed out! Please try again.")
    except requests.exceptions.HTTPError as e:
        print_error(f"HTTP Error: {e}")
    except KeyError as e:
        print_error(f"Unexpected response format: {e}")
    except Exception as e:
        print_error(f"Unexpected error: {e}")

    return None


# ============================================================
#   CRYPTO API — CoinGecko (No API key needed!)
# ============================================================

def get_crypto_prices():
    print_section("LIVE CRYPTOCURRENCY PRICES")
    print_info("Fetching from CoinGecko API (free, no key needed)...")

    # Top cryptocurrencies to fetch
    coins = [
        "bitcoin",
        "ethereum",
        "binancecoin",
        "ripple",
        "cardano",
        "solana",
        "dogecoin",
        "polkadot"
    ]

    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
        "ids":            ",".join(coins),
        "vs_currencies":  "usd,inr",          # USD and INR (Indian Rupee!)
        "include_24hr_change": "true",
        "include_market_cap":  "true"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Coin display names
        coin_names = {
            "bitcoin":     ("Bitcoin",     "BTC",  "₿"),
            "ethereum":    ("Ethereum",    "ETH",  "⟠"),
            "binancecoin": ("BNB",         "BNB",  "🔶"),
            "ripple":      ("XRP",         "XRP",  "💧"),
            "cardano":     ("Cardano",     "ADA",  "🔵"),
            "solana":      ("Solana",      "SOL",  "🌞"),
            "dogecoin":    ("Dogecoin",    "DOGE", "🐕"),
            "polkadot":    ("Polkadot",    "DOT",  "🔴"),
        }

        crypto_results = []

        print(f"""
{BOLD}  {'COIN':<18} {'PRICE (USD)':>14} {'PRICE (INR)':>16} {'24H CHANGE':>12}{RESET}
  {'─'*65}""")

        for coin_id, coin_data in data.items():
            name, symbol, icon = coin_names.get(coin_id, (coin_id, coin_id, "🪙"))

            price_usd   = coin_data.get("usd", 0)
            price_inr   = coin_data.get("inr", 0)
            change_24h  = coin_data.get("usd_24h_change", 0)
            market_cap  = coin_data.get("usd_market_cap", 0)

            # Color based on price change
            if change_24h >= 0:
                change_color = GREEN
                arrow = "▲"
            else:
                change_color = RED
                arrow = "▼"

            # Format large numbers
            def fmt_usd(n):
                if n >= 1000:
                    return f"${n:,.2f}"
                return f"${n:.4f}"

            def fmt_inr(n):
                if n >= 1000:
                    return f"₹{n:,.2f}"
                return f"₹{n:.4f}"

            print(f"  {icon} {name:<15} {fmt_usd(price_usd):>14} "
                  f"{fmt_inr(price_inr):>16} "
                  f"{change_color}{arrow} {abs(change_24h):.2f}%{RESET}")

Rajput Girl, [3/8/2026 12:23 PM]
crypto_results.append({
                "coin":         name,
                "symbol":       symbol,
                "price_usd":    price_usd,
                "price_inr":    price_inr,
                "change_24h":   round(change_24h, 2),
                "market_cap_usd": market_cap,
                "fetched_at":   datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        print(f"  {'─'*65}")
        print(f"\n  {YELLOW}Prices in USD and INR (Indian Rupee) ₹{RESET}")
        print(f"  {YELLOW}Green ▲ = price went UP in last 24h{RESET}")
        print(f"  {RED}Red   ▼ = price went DOWN in last 24h{RESET}\n")

        print_success("Crypto prices fetched successfully!")
        return crypto_results

    except requests.exceptions.ConnectionError:
        print_error("No internet connection! Please check your network.")
    except requests.exceptions.Timeout:
        print_error("Request timed out! Please try again.")
    except requests.exceptions.HTTPError as e:
        print_error(f"HTTP Error: {e}")
    except Exception as e:
        print_error(f"Unexpected error: {e}")

    return []


# ============================================================
#   SAVE REPORT to .txt file
# ============================================================

def save_report(weather_data, crypto_data, city):
    filename = f"api_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write("=" * 55 + "\n")
        f.write("         PYTHON API INTEGRATION REPORT\n")
        f.write(f"         Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 55 + "\n\n")

        # Weather section
        if weather_data:
            f.write("WEATHER DATA\n")
            f.write("-" * 40 + "\n")
            f.write(f"City        : {weather_data['city']}, {weather_data['country']}\n")
            f.write(f"Condition   : {weather_data['condition']}\n")
            f.write(f"Temperature : {weather_data['temperature']}C\n")
            f.write(f"Feels Like  : {weather_data['feels_like']}C\n")
            f.write(f"Min / Max   : {weather_data['min_temp']}C / {weather_data['max_temp']}C\n")
            f.write(f"Humidity    : {weather_data['humidity']}%\n")
            f.write(f"Wind Speed  : {weather_data['wind_speed']} m/s\n")
            f.write(f"Sunrise     : {weather_data['sunrise']}\n")
            f.write(f"Sunset      : {weather_data['sunset']}\n")
            f.write(f"Fetched At  : {weather_data['fetched_at']}\n\n")

        # Crypto section
        if crypto_data:
            f.write("CRYPTOCURRENCY PRICES\n")
            f.write("-" * 40 + "\n")
            f.write(f"{'COIN':<15} {'USD':>12} {'INR':>16} {'24H':>10}\n")
            f.write("-" * 55 + "\n")
            for coin in crypto_data:
                change = f"+{coin['change_24h']}%" if coin['change_24h'] >= 0 else f"{coin['change_24h']}%"
                f.write(
                    f"{coin['coin']:<15} "
                    f"${coin['price_usd']:>11,.2f} "
                    f"Rs{coin['price_inr']:>14,.2f} "
                    f"{change:>10}\n"
                )
            f.write(f"\nFetched At: {crypto_data[0]['fetched_at']}\n")

        f.write("\n" + "=" * 55 + "\n")
        f.write("         END OF REPORT\n")
        f.write("=" * 55 + "\n")

    print_success(f"Report saved to '{filename}'")
    return filename


# ============================================================
#   MAIN
# ============================================================

def main():
    print(f"""
{BLUE}{BOLD}
╔══════════════════════════════════════════════════╗
║           PYTHON API INTEGRATION                ║
║       Weather + Cryptocurrency Prices           ║
║                                                 ║
║   Weather API  : OpenWeatherMap (Free)          ║
║   Crypto  API  : CoinGecko (Free, No key!)      ║
╚══════════════════════════════════════════════════╝
{RESET}""")

Rajput Girl, [3/8/2026 12:23 PM]
print(f"{BOLD}What would you like to fetch?{RESET}")
    print("  1. Weather only")
    print("  2. Cryptocurrency prices only")
    print("  3. Both Weather + Crypto  (Recommended)")
    print("  4. Exit")

    choice = input("\n  Enter choice (1/2/3/4): ").strip()

    weather_data = None
    crypto_data  = []
    city         = ""

    if choice in ["1", "3"]:
        city = input("\n  Enter city name (e.g. Mumbai, Delhi, Pune): ").strip()
        if not city:
            print_error("City name cannot be empty!")
            return
        weather_data = get_weather(city)

    if choice in ["2", "3"]:
        crypto_data = get_crypto_prices()

    if choice == "4":
        print(f"\n{BOLD}  Goodbye! Happy Coding! 🐍{RESET}\n")
        return

    if choice not in ["1", "2", "3", "4"]:
        print_error("Invalid choice! Please enter 1, 2, 3, or 4.")
        return

    # Save report
    if weather_data or crypto_data:
        print_section("SAVING REPORT")
        save_report(weather_data, crypto_data, city)
        print(f"\n{YELLOW}  Report saved in: {os.getcwd()}{RESET}")

    print(f"\n{GREEN}{BOLD}  All done! Task 3 Complete! 🎉{RESET}\n")


if name == "main":
    main() 
