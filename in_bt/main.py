import logging
import time
import requests
from modules.scraper import scrape_stock_summary
from modules.db_handler import save_stock_summary_data, ensure_stock_summary_table_exists
from modules.driver_setup import setup_driver
from config.db_settings import DB_PARAMS

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Constants
TIMEOUT = 130  # Timeout for HTTP requests

def is_url_valid(url):
    """
    Check if the URL is valid and reachable.
    """
    try:
        response = requests.head(url, timeout=TIMEOUT)
        if response.status_code == 404:
            logger.warning(f"URL {url} returned 404. Skipping.")
            return False
        return True
    except requests.RequestException as e:
        logger.warning(f"Error checking URL {url}: {e}")
        return False

def process_url(driver, url, db_params):
    """
    Process a single URL to scrape and save stock data.
    If no data is found, return False; otherwise, return True.
    """
    logger.info(f"Processing URL: {url}")
    try:
        # Scrape the stock summary data
        stock_summary_data = scrape_stock_summary(driver, url)

        if stock_summary_data:
            # Insert the stock data into the database immediately
            save_stock_summary_data(db_params, stock_summary_data)
            logger.info(f"Stock summary data saved for URL: {url}")
            return True
        else:
            logger.warning(f"No data found for URL: {url}")
            return False
    except Exception as e:
        logger.error(f"Error processing URL {url}: {e}")
        return False

def main(start_id=366519, end_id=366739, base_url=None):
    """
    Main function to iterate through stock URLs, scrape data, and save to the database.
    If no data is found for a URL, wait 10 seconds and retry from that URL.
    """
    logger.info("Starting stock scraper...")

    # Ensure the database table exists
    try:
        ensure_stock_summary_table_exists(DB_PARAMS)
    except Exception as e:
        logger.error(f"Error ensuring database tables exist: {e}")
        return

    # Set up the WebDriver
    try:
        driver = setup_driver()
    except Exception as e:
        logger.error(f"Failed to initialize WebDriver: {e}")
        return

    # Use the default base URL if not provided
    if not base_url:
        base_url = "https://www.businesstoday.in/stocks/utique-enterprises-ltd-appleind-share-price-"

    current_id = start_id  # Keep track of the current ID
    try:
        while current_id <= end_id:
            url = f"{base_url}{current_id}"
            if not is_url_valid(url):
                current_id += 1
                continue

            success = process_url(driver, url, DB_PARAMS)

            if success:
                # Move to the next ID if processing is successful
                current_id += 1
            else:
                # If no data is found, wait for 10 seconds and retry the same URL
                logger.warning(f"Retrying URL: {url} after 130 seconds...")
                time.sleep(30)

    except Exception as e:
        logger.error(f"Unexpected error during scraping: {e}")
    finally:
        try:
            driver.quit()
        except Exception as e:
            logger.error(f"Error while closing WebDriver: {e}")

        logger.info("Stock scraper finished.")

if __name__ == "__main__":
    # Example configuration values
    # starting 361150
    START_ID = 366519
    END_ID = 366739
    BASE_URL = "https://www.businesstoday.in/stocks/utique-enterprises-ltd-appleind-share-price-"

    main(start_id=START_ID, end_id=END_ID, base_url=BASE_URL)
