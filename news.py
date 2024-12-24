import requests
from bs4 import BeautifulSoup

def scrape_bel_stock_data():
    # Define the URL
    url = "https://www.businesstoday.in/stocks/bharat-electronics-ltd-bel-share-price-362766"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Fetch the webpage content
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
        return None

    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # DEBUG: Print raw content of the page
    with open("debug.html", "w", encoding="utf-8") as f:
        f.write(soup.prettify())

    try:
        # Example: Locate current price (update this based on inspection)
        current_price = soup.find("span", {"class": "price"}).text.strip()
        print(f"Current Price: ₹{current_price}")
    except Exception as e:
        print(f"Error extracting data: {e}")
        print("The HTML structure may have changed. Please check the 'debug.html' file.")

# Run the scraper
if __name__ == "__main__":
    scrape_bel_stock_data()
