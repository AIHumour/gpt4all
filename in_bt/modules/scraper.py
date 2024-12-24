import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

# Initialize logger
logger = logging.getLogger(__name__)

def scrape_stock_summary(driver, url):
    """
    Scrapes stock summary and additional data from the given URL using Selenium.
    """
    try:
        logger.info(f"Navigating to URL: {url}")
        driver.get(url)

        # Wait for the stock summary and company details to load
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CLASS_NAME, "mrk_wdg_box"))
        )

        # Initialize data dictionary
        stock_data = {}

        # Scrape company details (name, sector, volume)
        try:
            company_details = driver.find_element(By.ID, "flyout-left-container-nse-bse-exchange")
            stock_data["name"] = company_details.find_element(By.CLASS_NAME, "cmp_nme_ttl").text.strip()

            # Extract sector
            sector_element = company_details.find_element(By.XPATH, ".//li[@class='cmp_dtl_li']/span[@class='cmp_dtl_val']")
            stock_data["sector"] = sector_element.text.strip()

            # Extract volume
            volume_element = company_details.find_element(By.ID, "volumeId")
            stock_data["volume"] = volume_element.text.strip()
        except NoSuchElementException as e:
            logger.warning(f"Could not extract company details: {e}")

        # Scrape stock summary table (Face Value, Beta, etc.)
        try:
            stock_table = driver.find_element(By.ID, "stock-detail-table")
            rows = stock_table.find_elements(By.CLASS_NAME, "stk_sum_li")
            for row in rows:
                try:
                    label = row.find_element(By.CLASS_NAME, "stk_sum_lbl").text.strip()
                    value_element = row.find_elements(By.CLASS_NAME, "stk_sum_val")
                    value = value_element[0].text.strip() if value_element else "N/A"
                    stock_data[label] = value
                except NoSuchElementException as e:
                    logger.warning(f"Could not process a row in the stock summary table: {e}")
        except Exception as e:
            logger.warning(f"Could not process stock summary table: {e}")

        # Scrape price details (current price, change, percentage change)
        try:
            stock_data["current_price"] = company_details.find_element(By.ID, "webenagecampnayprice").text.strip()
            price_change = company_details.find_element(By.CLASS_NAME, "cmp_amt").text.strip()
            change, percentage_change = price_change.split(" ")
            stock_data["change"] = change.strip("₹")
            stock_data["percentage_change"] = percentage_change.strip("()%")
        except Exception as e:
            logger.warning(f"Could not process price details: {e}")

        # Scrape performance data (today's performance and 52-week performance)
        try:
            performance_divs = driver.find_elements(By.CLASS_NAME, "tch_sld_itm")
            if len(performance_divs) > 0:
                today_performance = performance_divs[0]
                stock_data["low_today"] = today_performance.find_element(By.CLASS_NAME, "tch_sld_val").text.strip()
                stock_data["high_today"] = today_performance.find_element(By.CLASS_NAME, "tch_sld_rhs").text.strip()

                if len(performance_divs) > 1:
                    week_performance = performance_divs[1]
                    stock_data["low_52_week"] = week_performance.find_element(By.CLASS_NAME, "tch_sld_val").text.strip()
                    stock_data["high_52_week"] = week_performance.find_element(By.CLASS_NAME, "tch_sld_rhs").text.strip()
        except Exception as e:
            logger.warning(f"Could not process performance data: {e}")

        logger.info(f"Scraped data: {stock_data}")
        return stock_data

    except Exception as e:
        logger.error(f"Error scraping URL {url}: {e}")
        return None



def scrape_stock_analysis(driver, db_params, url):
    """
    Scrapes SWOT and QVT stock analysis data and saves it to the database.
    """
    stock_analysis_data = {
        "stock_name": "N/A",
        "swot_strength": "N/A",
        "swot_weakness": "N/A",
        "swot_opportunity": "N/A",
        "swot_threat": "N/A",
        "qvt_quality": "N/A",
        "qvt_valuation": "N/A",
        "qvt_technicals": "N/A",
    }

    try:
        logger.info(f"Navigating to URL: {url}")
        driver.get(url)

        # Wait for the SWOT and QVT sections to load
        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "mrk_wdg_box"))
            )
        except TimeoutException:
            logger.error(f"Timeout while waiting for SWOT/QVT sections on {url}")
            return None

        # Scrape the stock name
        try:
            stock_analysis_data["stock_name"] = driver.find_element(By.CLASS_NAME, "cmp_nme_ttl").text.strip()
        except NoSuchElementException:
            logger.warning(f"Stock name not found for URL: {url}")

        # Scrape SWOT data
        try:
            swot_section = driver.find_element(By.ID, "swot_analysis")
            stock_analysis_data["swot_strength"] = swot_section.find_element(
                By.XPATH, ".//div[contains(@class, 'tl__strengths-fill')]//span[@class='tl__tag_number--inYpa']"
            ).text.strip()
        except NoSuchElementException:
            logger.warning(f"SWOT Strength data not found for URL: {url}")

        # Scrape QVT data
        try:
            iframe = driver.find_element(By.XPATH, "//iframe[contains(@src, 'qvt-widget')]")
            driver.switch_to.frame(iframe)
            qvt_section = driver.find_element(By.CLASS_NAME, "stk_anl_rhs")
            stock_analysis_data["qvt_quality"] = qvt_section.find_element(
                By.XPATH, ".//div[contains(text(), 'Quality')]/parent::div/following-sibling::div"
            ).text.strip()
        except NoSuchElementException:
            logger.warning(f"QVT data not found for URL: {url}")
        finally:
            driver.switch_to.default_content()

        logger.info(f"Scraped stock analysis data: {stock_analysis_data}")
        return stock_analysis_data

    except Exception as e:
        logger.error(f"Unexpected error scraping SWOT/QVT data from {url}: {e}")
        return None

