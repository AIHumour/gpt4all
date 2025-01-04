from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def setup_driver():
    """
    Set up the Selenium WebDriver with optimized headless mode enabled.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Enable headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
    chrome_options.add_argument("--window-size=1920,1080")  # Set a standard window size
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource issues
    chrome_options.add_argument("--disable-extensions")  # Disable extensions
    chrome_options.add_argument("--disable-logging")  # Reduce logging noise
    chrome_options.add_argument("--log-level=3")  # Minimize Chrome logs
    chrome_options.add_argument("--disable-popup-blocking")  # Disable pop-ups
    chrome_options.add_argument("--ignore-certificate-errors")  # Ignore SSL errors
    chrome_options.add_argument("--disable-software-rasterizer")  # Disable WebGL software fallback
    chrome_options.add_argument("--disable-webgl")  # Completely disable WebGL
    chrome_options.add_argument("--enable-features=NetworkService,NetworkServiceInProcess")  # Optimize network handling
    chrome_options.add_argument("--disable-background-timer-throttling")  # Disable background throttling
    chrome_options.add_argument("--disable-backgrounding-occluded-windows")  # Disable occluded window throttling
    chrome_options.add_argument("--disable-renderer-backgrounding")  # Prevent renderer throttling

    # Use the ChromeDriverManager to automatically manage ChromeDriver installation
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    return driver
