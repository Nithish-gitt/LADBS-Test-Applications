from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def navigate(self, url):
        self.driver.get(url)

    def find_element(self, locator):
        return self.driver.find_element(*locator)

    def click(self, locator):
        element = self.find_element(locator)
        element.click()

    def type_text(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        element = self.find_element(locator)
        return element.text

    def wait_for_element(self, locator, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.presence_of_element_located(locator))
        return self.find_element(locator)

    def get_title(self):
        return self.driver.title
