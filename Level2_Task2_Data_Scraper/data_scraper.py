Rajput Girl, [3/8/2026 12:15 PM]
# ============================================================
#   PYTHON DATA SCRAPER — Task 2 (Intermediate)
#   News Source  : Times of India (India)
#   Products     : books.toscrape.com
#   Saves        : news.csv + products.csv
# ============================================================
#
#   BEFORE RUNNING install libraries:
#   Open terminal and type:
#       pip install requests beautifulsoup4
#
# ============================================================

import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime

# Colors for terminal output
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
BLUE   = "\033[94m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def print_header():
    print(f"""
{BLUE}{BOLD}
╔══════════════════════════════════════════════╗
║           PYTHON DATA SCRAPER               ║
║   Times of India News + Product Prices      ║
╚══════════════════════════════════════════════╝
{RESET}""")

def print_success(msg): print(f"{GREEN}✅ {msg}{RESET}")
def print_error(msg):   print(f"{RED}❌ {msg}{RESET}")
def print_info(msg):    print(f"{YELLOW}   {msg}{RESET}")
def print_section(msg): print(f"\n{BLUE}{BOLD}{'='*50}\n  {msg}\n{'='*50}{RESET}")


# ============================================================
#   SAVE TO CSV
# ============================================================

def save_to_csv(data, filename, fields):
    if not data:
        print_error(f"No data to save to {filename}")
        return
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)
    print_success(f"Saved {len(data)} records to '{filename}'")


# ============================================================
#   SCRAPER 1 — NEWS HEADLINES from Times of India
# ============================================================

def scrape_news():
    print_section("SCRAPING TIMES OF INDIA HEADLINES")
    print_info("Fetching latest Indian news...")

    # Times of India RSS feed — most reliable way to get TOI headlines
    # RSS feeds are publicly available and scraping-friendly
    url = "https://timesofindia.indiatimes.com/rssfeedstopstories.cms"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        print_success(f"Connected to Times of India! Status: {response.status_code}")

        # Parse RSS/XML with BeautifulSoup
        soup = BeautifulSoup(response.content, "xml")

        headlines = []
        items = soup.find_all("item")

        if not items:
            # Fallback: try HTML parser
            soup = BeautifulSoup(response.text, "html.parser")
            items = soup.find_all("item")

        for item in items:
            title = item.find("title")
            desc  = item.find("description")
            link  = item.find("link")
            pub   = item.find("pubDate")

            if title:
                headline_text = title.get_text(strip=True)
                # Clean up CDATA if present
                headline_text = headline_text.replace("<![CDATA[", "").replace("]]>", "").strip()

                if len(headline_text) > 10:
                    headlines.append({
                        "headline":    headline_text,
                        "description": desc.get_text(strip=True)[:100] + "..." if desc else "N/A",
                        "link":        link.get_text(strip=True) if link else "N/A",
                        "published":   pub.get_text(strip=True) if pub else "N/A",
                        "source":      "Times of India",
                        "scraped_at":  datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })

Rajput Girl, [3/8/2026 12:15 PM]
# If RSS didn't work, try direct website
        if not headlines:
            print_info("RSS feed failed. Trying direct website...")
            headlines = scrape_toi_direct(headers)

        print_success(f"Found {len(headlines)} headlines!\n")
        for i, item in enumerate(headlines[:10], 1):
            print(f"  {BOLD}{i:2}.{RESET} {item['headline']}")

        if len(headlines) > 10:
            print_info(f"...and {len(headlines) - 10} more saved to news.csv")

        save_to_csv(headlines, "news.csv",
                    ["headline", "description", "link", "published", "source", "scraped_at"])
        return headlines

    except requests.exceptions.ConnectionError:
        print_error("No internet connection! Please check your network.")
    except requests.exceptions.Timeout:
        print_error("Request timed out. Please try again.")
    except requests.exceptions.HTTPError as e:
        print_error(f"HTTP Error: {e}")
    except Exception as e:
        print_error(f"Unexpected error: {e}")

    return []


def scrape_toi_direct(headers):
    """Fallback: scrape TOI website directly"""
    headlines = []
    seen = set()

    try:
        url  = "https://timesofindia.indiatimes.com"
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")

        # TOI uses various heading tags for news
        for tag in soup.find_all(["h1", "h2", "h3", "figcaption"], limit=80):
            text = tag.get_text(strip=True)
            if (len(text) > 20
                    and text not in seen
                    and not any(skip in text.lower() for skip in
                                ["times of india", "subscribe", "sign in",
                                 "download app", "follow us", "advertisement"])):
                seen.add(text)
                headlines.append({
                    "headline":    text,
                    "description": "N/A",
                    "link":        url,
                    "published":   "N/A",
                    "source":      "Times of India",
                    "scraped_at":  datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
    except Exception as e:
        print_error(f"Direct scrape also failed: {e}")

    return headlines


# ============================================================
#   SCRAPER 2 — PRODUCT PRICES from books.toscrape.com
#   (This site is MADE for practice scraping — 100% legal!)
# ============================================================

def scrape_products():
    print_section("SCRAPING PRODUCT PRICES")
    print_info("Fetching from books.toscrape.com (practice site)...")

    base_url   = "https://books.toscrape.com"
    products   = []
    rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

    try:
        for page in range(1, 4):
            url = f"{base_url}/catalogue/page-{page}.html"
            print_info(f"Scraping page {page}...")

            response = requests.get(
                url,
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=10
            )
            response.raise_for_status()

            soup  = BeautifulSoup(response.text, "html.parser")
            books = soup.find_all("article", class_="product_pod")

            for book in books:
                title      = book.find("h3").find("a")["title"]
                price_raw  = book.find("p", class_="price_color").get_text(strip=True)
                price      = price_raw.encode("ascii", "ignore").decode().replace("£", "").strip()
                rating_tag = book.find("p", class_="star-rating")
                rating     = rating_map.get(
                    rating_tag["class"][1] if rating_tag else "Zero", 0
                )
                avail        = book.find("p", class_="instock")
                availability = avail.get_text(strip=True) if avail else "Unknown"
                link_href    = book.find("h3").find("a")["href"]
                link         = f"{base_url}/catalogue/{link_href.replace('../', '')}"

Rajput Girl, [3/8/2026 12:15 PM]
products.append({
                    "title":        title,
                    "price_GBP":    price,
                    "rating":       f"{rating}/5 stars",
                    "availability": availability,
                    "link":         link,
                    "scraped_at":   datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

        print_success(f"Found {len(products)} products!\n")
        print(f"  {'#':<4} {'TITLE':<42} {'PRICE':>8}  {'RATING'}")
        print(f"  {'-'*4} {'-'*42} {'-'*8}  {'-'*12}")

        for i, p in enumerate(products[:15], 1):
            short = (p["title"][:40] + "..") if len(p["title"]) > 40 else p["title"]
            print(f"  {i:<4} {short:<42} {p['price_GBP']:>7}  {p['rating']}")

        if len(products) > 15:
            print_info(f"...and {len(products) - 15} more saved to products.csv")

        save_to_csv(products, "products.csv",
                    ["title", "price_GBP", "rating", "availability", "link", "scraped_at"])
        return products

    except requests.exceptions.ConnectionError:
        print_error("No internet connection! Please check your network.")
    except requests.exceptions.Timeout:
        print_error("Request timed out. Please try again.")
    except requests.exceptions.HTTPError as e:
        print_error(f"HTTP Error: {e}")
    except Exception as e:
        print_error(f"Unexpected error: {e}")

    return []


# ============================================================
#   ANALYSIS — Quick stats on scraped products
# ============================================================

def analyze_products(products):
    if not products:
        return

    print_section("QUICK ANALYSIS")

    prices = []
    for p in products:
        try:
            prices.append(float(p["price_GBP"]))
        except ValueError:
            pass

    if prices:
        print(f"  Total products scraped   : {len(products)}")
        print(f"  Cheapest product         : {min(prices):.2f} GBP")
        print(f"  Most expensive product   : {max(prices):.2f} GBP")
        print(f"  Average price            : {sum(prices)/len(prices):.2f} GBP")

    ratings = {}
    for p in products:
        r = p["rating"]
        ratings[r] = ratings.get(r, 0) + 1

    print(f"\n  Rating breakdown:")
    for r in sorted(ratings.keys()):
        bar = "=" * ratings[r]
        print(f"    {r:14}: [{bar}] ({ratings[r]} books)")


# ============================================================
#   MAIN
# ============================================================

def main():
    print_header()

    print(f"{BOLD}What would you like to scrape?{RESET}")
    print("  1. Times of India News only")
    print("  2. Product Prices only")
    print("  3. Both (News + Products)")

    choice = input("\n  Enter choice (1/2/3): ").strip()

    news     = []
    products = []

    if choice == "1":
        news = scrape_news()

    elif choice == "2":
        products = scrape_products()
        analyze_products(products)

    elif choice == "3":
        news     = scrape_news()
        products = scrape_products()
        analyze_products(products)

    else:
        print_error("Invalid choice! Please enter 1, 2, or 3.")
        return

    print_section("SCRAPING COMPLETE!")
    if news:
        print_success(f"{len(news)} headlines saved to 'news.csv'")
    if products:
        print_success(f"{len(products)} products saved to 'products.csv'")

    print(f"\n{YELLOW}  Files saved in: {os.getcwd()}{RESET}")
    print(f"\n{BOLD}  Thank you for using Python Data Scraper!{RESET}\n")


if name == "main":
    main()
