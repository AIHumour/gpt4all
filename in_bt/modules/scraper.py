import logging 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def sanitize_value(value):
    if isinstance(value, str):
        return value.replace("\u20b9", "").replace(",", "").strip()
    return value or "N/A"

def scrape_performance(driver):
    performance_data = {}
    try:
        performance_section = driver.find_element(By.ID, "stock-performance")
        performance_items = performance_section.find_elements(By.CLASS_NAME, "stk_prf_li")
        for item in performance_items:
            time_period = item.find_element(By.CLASS_NAME, "stk_prf_lhs").text.strip()
            performance_value = item.find_element(By.CLASS_NAME, "stk_prf_rhs").text.strip()
            performance_data[time_period] = performance_value
    except NoSuchElementException:
        logger.warning("Performance section not found.")
    return performance_data or {"1 Day": "N/A", "1 Week": "N/A", "1 Month": "N/A"}

def scrape_performance_details(driver):
    performance_details = {
        "Today’s Performance": {"Low": "N/A", "High": "N/A"},
        "52 Week’s Performance": {"Low": "N/A", "High": "N/A"}
    }
    try:
        performance_bar = driver.find_element(By.ID, "tchPerformanceBarId")
        sliders = performance_bar.find_elements(By.CLASS_NAME, "tch_sld_itm")
        for slider in sliders:
            performance_type = slider.find_element(By.CLASS_NAME, "tch_sld_nme").text.strip()
            low_value = sanitize_value(slider.find_element(By.XPATH, ".//div[@class='tch_sld_lhs']/span[@class='tch_sld_val']").text)
            high_value = sanitize_value(slider.find_element(By.XPATH, ".//div[@class='tch_sld_rhs']/span[@class='tch_sld_val']").text)
            performance_details[performance_type] = {"Low": low_value, "High": high_value}
    except NoSuchElementException:
        logger.warning("Performance details section not found.")
    return performance_details

def scrape_summary_data(driver):
    """
    Scrapes the stock summary table for fields like beta, price-to-book, dividend yield, etc.
    Returns a dictionary of the scraped data.
    """
    summary_data = {
        "beta": "N/A",
        "price_to_book": "N/A",
        "dividend_yield": "N/A",
        "pe_ratio": "N/A",
        "eps": "N/A",
        "market_cap": "N/A",
    }

    try:
        # Wait for the stock summary section to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "stk_sum_wrp"))
        )

        # Locate the stock summary table
        stock_table = driver.find_element(By.ID, "stock-detail-table")
        rows = stock_table.find_elements(By.CLASS_NAME, "stk_sum_li")

        # Iterate through each row in the summary table
        for row in rows:
            try:
                label = row.find_element(By.CLASS_NAME, "stk_sum_lbl").text.strip()
                value = sanitize_value(row.find_element(By.CLASS_NAME, "stk_sum_val").text)

                # Map fields explicitly to avoid mismatches
                if "Beta" in label:
                    summary_data["beta"] = value
                elif "Price-to-Book" in label:
                    summary_data["price_to_book"] = value
                elif "Dividend Yield" in label:
                    summary_data["dividend_yield"] = value
                elif "Price-to-Earnings" in label:
                    summary_data["pe_ratio"] = value
                elif "Earnings Per Share" in label:
                    summary_data["eps"] = value
                elif "Market Cap" in label:
                    summary_data["market_cap"] = value

            except NoSuchElementException as e:
                logger.warning(f"Missing data for a row in the stock summary table: {e}")

    except TimeoutException:
        logger.error("Stock summary table did not load in time.")
    except NoSuchElementException as e:
        logger.error(f"Stock summary table not found: {e}")
    except Exception as e:
        logger.error(f"Unexpected error while scraping summary data: {e}")

    return summary_data



def scrape_stock_summary(driver, url):
    try:
        logger.info(f"Navigating to URL: {url}")
        driver.get(url)
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "mrk_wdg_box")))

        stock_data = {}
        stock_data["competitors"] = []
        stock_data["about"] = "N/A"
        stock_data["management_team"] = []

        summary_data = {}

        try:
            company_details = driver.find_element(By.ID, "flyout-left-container-nse-bse-exchange")
            stock_data["name"] = company_details.find_element(By.CLASS_NAME, "cmp_nme_ttl").text.strip()
            stock_data["sector"] = company_details.find_element(By.XPATH, ".//li[@class='cmp_dtl_li']/span[@class='cmp_dtl_val']").text.strip()
            stock_data["volume"] = sanitize_value(company_details.find_element(By.ID, "volumeId").text)

            # Extract current price, change, and percentage change
            stock_data["current_price"] = sanitize_value(company_details.find_element(By.ID, "webenagecampnayprice").text)
            price_change = company_details.find_element(By.CLASS_NAME, "cmp_amt").text.strip()
            change, percentage_change = price_change.split(" ")
            stock_data["change"] = sanitize_value(change)
            stock_data["percentage_change"] = percentage_change.strip("()%")
        except NoSuchElementException:
            logger.warning("Price details not found.")
            stock_data["current_price"] = stock_data["change"] = stock_data["percentage_change"] = "N/A"

        try:
            stock_table = driver.find_element(By.ID, "stock-detail-table")
            rows = stock_table.find_elements(By.CLASS_NAME, "stk_sum_li")
            for row in rows:
                label = row.find_element(By.CLASS_NAME, "stk_sum_lbl").text.strip()
                value = sanitize_value(row.find_element(By.CLASS_NAME, "stk_sum_val").text)

                # Map fields explicitly for required columns
                if label in ["Beta", "Price-to-Book (X)*", "Dividend Yield (%)", "Price-to-Earnings (P/E) (X)*", "Earnings Per Share (₹)", "Market Cap (₹ Cr.)*"]:
                    summary_data[label] = value
        except NoSuchElementException:
            logger.warning("Stock summary table not found.")

        stock_data["summary_data"] = scrape_summary_data(driver)
        stock_data["performance"] = scrape_performance(driver)
        stock_data["performance_details"] = scrape_performance_details(driver)

        # Competitors
        try:
            competitors_section = driver.find_element(By.ID, "competitorsPerformanceId")
            for competitor in competitors_section.find_elements(By.CLASS_NAME, "mst_trk_li"):
                competitor_data = {
                    "name": competitor.find_element(By.CLASS_NAME, "mst_trk_ttl").text.strip(),
                    "url": competitor.find_element(By.CLASS_NAME, "mst_trk_lnk").get_attribute("href"),
                }
                competitor_text = competitor.find_element(By.CLASS_NAME, "mst_trk_txt").text.strip()
                price_data = competitor_text.split(" ")
                competitor_data["current_price"] = sanitize_value(price_data[0])
                competitor_data["price_change"] = sanitize_value(price_data[1])
                competitor_data["percentage_change"] = sanitize_value(price_data[2].strip("()%"))
                stock_data["competitors"].append(competitor_data)
        except NoSuchElementException:
            logger.warning("Competitors section not found.")

        # About section
        try:
            about_section = driver.find_element(By.CLASS_NAME, "abt_cnt_wrp")
            stock_data["about"] = about_section.text.strip()
        except NoSuchElementException:
            logger.warning("'About' section not found.")

        # Management team
        try:
            management_team = driver.find_elements(By.CLASS_NAME, "abt_li")
            for member in management_team:
                stock_data["management_team"].append({
                    "name": member.find_element(By.CLASS_NAME, "abt_li_ttl").text.strip(),
                    "position": member.find_element(By.CLASS_NAME, "abt_li_txt").text.strip()
                })
        except NoSuchElementException:
            logger.warning("Management team section not found.")

        # SWOT
        try:
            swot_section = driver.find_element(By.ID, "swot_analysis")
            stock_data["swot"] = {
                "strengths": swot_section.find_element(By.XPATH, ".//span[contains(text(), 'Strengths')]/following-sibling::span").text.strip(),
                "weaknesses": swot_section.find_element(By.XPATH, ".//span[contains(text(), 'Weaknesses')]/following-sibling::span").text.strip(),
                "opportunities": swot_section.find_element(By.XPATH, ".//span[contains(text(), 'Opportunity')]/following-sibling::span").text.strip(),
                "threats": swot_section.find_element(By.XPATH, ".//span[contains(text(), 'Threats')]/following-sibling::span").text.strip(),
            }
        except NoSuchElementException:
            logger.warning("SWOT section not found.")

        # QVT
        try:
            qvt_section = driver.find_element(By.ID, "qvt_stock_score")
            stock_data["qvt"] = {
                "quality": qvt_section.find_element(By.XPATH, ".//span[contains(text(), 'Quality')]/following-sibling::span").text.strip(),
                "valuation": qvt_section.find_element(By.XPATH, ".//span[contains(text(), 'Valuation')]/following-sibling::span").text.strip(),
                "technicals": qvt_section.find_element(By.XPATH, ".//span[contains(text(), 'Technicals')]/following-sibling::span").text.strip(),
            }
        except NoSuchElementException:
            logger.warning("QVT section not found.")

        logger.info(f"Scraped data: {stock_data}")
        return stock_data

    except Exception as e:
        logger.error(f"Error scraping URL {url}: {e}")
        return None
