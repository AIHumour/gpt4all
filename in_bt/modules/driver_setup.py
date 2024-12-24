from selenium import webdriver

def setup_driver():
    """
    Configures and returns a Selenium WebDriver instance.
    """
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-webgl")  # Suppress WebGL warnings
        return webdriver.Chrome(options=options)
    except Exception as e:
        raise RuntimeError(f"Error initializing WebDriver: {e}")
