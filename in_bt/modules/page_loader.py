from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def load_page(driver, url):
    driver.get(url)
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "webenagecampnayprice"))
        )
        return driver.page_source
    except TimeoutException:
        raise TimeoutException("Page elements did not load within the timeout period.")
