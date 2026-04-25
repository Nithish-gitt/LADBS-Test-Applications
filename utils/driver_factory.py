from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from config.config import BROWSER, IMPLICIT_WAIT


class DriverFactory:
    @staticmethod
    def create_driver(browser=BROWSER):
        driver = None

        if browser.lower() == 'chrome':
            options = ChromeOptions()
            # Uncomment the line below to run headless
            # options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')

            driver = webdriver.Chrome(options=options)

        elif browser.lower() == 'firefox':
            driver = webdriver.Firefox()

        elif browser.lower() == 'edge':
            driver = webdriver.Edge()

        else:
            driver = webdriver.Chrome()

        driver.implicitly_wait(IMPLICIT_WAIT)
        driver.maximize_window()

        return driver
