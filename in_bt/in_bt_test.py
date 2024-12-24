from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time

# Selenium WebDriver options
def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)

# Function to scrape BEL stock data
def scrape_bel_stock_data():
    driver = get_driver()
    try:
        # Define the URL for the BEL stock page
        url = "https://www.businesstoday.in/stocks/bharat-electronics-ltd-bel-share-price-362766"
        driver.get(url)

        # Wait for the necessary elements to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "webenagecampnayprice"))
        )

        # Get the rendered HTML content
        time.sleep(3)  # Allow extra time for dynamic content to load
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Scrape current price
        current_price_div = soup.find("div", {"id": "webenagecampnayprice"})
        current_price = current_price_div.text.strip() if current_price_div else "Data not available"

        # Scrape 52-week high and low
        stock_summary = soup.find("ul", {"id": "stock-detail-table"})
        week_high_span = stock_summary.find("span", string="52-Week High (₹)").find_next("span") if stock_summary else None
        week_low_span = stock_summary.find("span", string="52-Week Low (₹)").find_next("span") if stock_summary else None
        week_high = week_high_span.text.strip() if week_high_span else "Data not available"
        week_low = week_low_span.text.strip() if week_low_span else "Data not available"

        # Scrape today's high and low
        today_performance = soup.find("div", {"id": "tchPerformanceBarId"})
        if today_performance:
            performance_values = today_performance.find_all("div", {"class": "tch_sld_val"})
            today_low = performance_values[0].text.strip() if len(performance_values) > 0 else "Data not available"
            today_high = performance_values[1].text.strip() if len(performance_values) > 1 else "Data not available"
        else:
            today_low = "Data not available"
            today_high = "Data not available"

        # Scrape percentage changes for different timeframes
        performance_data = {}
        performance_list = soup.find("ul", {"id": "stock-performance"})
        if performance_list:
            for li in performance_list.find_all("li", {"class": "stk_prf_li"}):
                time_frame = li.find("span", {"class": "stk_prf_lhs"}).text.strip()
                change = li.find("span", {"class": "stk_prf_rhs"}).text.strip()
                performance_data[time_frame] = change

        # Scrape stock analysis iframes
        swot_analysis = soup.find("div", {"id": "swot_analysis"})
        swot_iframe = swot_analysis.find("iframe")["src"] if swot_analysis else "Data not available"

        qvt_stock_score = soup.find("div", {"id": "qvt_stock_score"})
        qvt_iframe = qvt_stock_score.find("iframe")["src"] if qvt_stock_score else "Data not available"

        # Print the scraped data
        print(f"Current Price: {current_price}")
        print(f"52-Week High: {week_high}")
        print(f"52-Week Low: {week_low}")
        print(f"Today's High: {today_high}")
        print(f"Today's Low: {today_low}")
        print("Performance Data:")
        for time_frame, change in performance_data.items():
            print(f"  {time_frame}: {change}")

        print(f"SWOT Analysis URL: {swot_iframe}")
        print(f"QVT Stock Score URL: {qvt_iframe}")

    except TimeoutException:
        print("Timeout while waiting for page elements to load.")
    except Exception as e:
        print(f"Error extracting data: {e}")
    finally:
        # Close the WebDriver
        driver.quit()

# Run the scraper
if __name__ == "__main__":
    scrape_bel_stock_data()
