import logging
from modules.scraper import scrape_stock_summary, scrape_stock_analysis
from modules.db_handler import (
    save_stock_summary_data,
    ensure_stock_summary_table_exists,
    ensure_stock_analysis_table_exists,
    save_stock_analysis_data,
)
from modules.url_extractor import generate_urls
from modules.driver_setup import setup_driver
from config.db_settings import DB_PARAMS

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def main(start_id=361150, num_stocks=3, base_url=None):
    """
    Main function to iterate through stock URLs, scrape data, and save to the database.
    """
    logger.info("Starting stock scraper...")

    # Ensure tables exist
    try:
        ensure_stock_summary_table_exists(DB_PARAMS)
        ensure_stock_analysis_table_exists(DB_PARAMS)
    except Exception as e:
        logger.error(f"Error ensuring database tables exist: {e}")
        return

    # Initialize WebDriver
    try:
        driver = setup_driver()
    except Exception as e:
        logger.error(f"Failed to initialize WebDriver: {e}")
        return

    # Use default base URL if none provided
    if not base_url:
        base_url = "https://www.businesstoday.in/stocks/utique-enterprises-ltd-appleind-share-price-"

    try:
        # Generate URLs to scrape
        urls = generate_urls(base_url, start_id, num_stocks)
        logger.info(f"Generated {len(urls)} URLs to scrape.")

        # Scrape data from each URL
        for url in urls:
            try:
                logger.info(f"Processing URL: {url}")

                # Scrape and save stock summary data
                stock_summary_data = scrape_stock_summary(driver, url)
                if stock_summary_data:
                    save_stock_summary_data(DB_PARAMS, stock_summary_data)
                    logger.info(f"Stock summary data saved for URL: {url}")

                # Scrape and save stock analysis data
                stock_analysis_data = scrape_stock_analysis(driver, DB_PARAMS, url)
                if stock_analysis_data:
                    save_stock_analysis_data(DB_PARAMS, stock_analysis_data)
                    logger.info(f"Stock analysis data saved for URL: {url}")

            except Exception as e:
                logger.error(f"Error processing URL {url}: {e}")

    except Exception as e:
        logger.error(f"Unexpected error during scraping: {e}")
    finally:
        try:
            driver.quit()
        except Exception as e:
            logger.error(f"Error while closing WebDriver: {e}")

        logger.info("Stock scraper finished.")


if __name__ == "__main__":
    # Example configuration values; replace with config file/environment variables if needed
    START_ID = 361150
    NUM_STOCKS = 3
    BASE_URL = "https://www.businesstoday.in/stocks/utique-enterprises-ltd-appleind-share-price-"

    main(start_id=START_ID, num_stocks=NUM_STOCKS, base_url=BASE_URL)
