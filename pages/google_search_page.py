from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage


class GoogleSearchPage(BasePage):
    # Locators
    SEARCH_BOX = (By.NAME, 'q')
    SEARCH_BUTTON = (By.NAME, 'btnK')
    SEARCH_RESULTS = (By.ID, 'search')

    def __init__(self, driver):
        super().__init__(driver)

    def open(self):
        self.navigate('https://www.google.com')

    def search(self, query):
        self.wait_for_element(self.SEARCH_BOX)
        self.type_text(self.SEARCH_BOX, query)
        search_input = self.find_element(self.SEARCH_BOX)
        search_input.send_keys(Keys.RETURN)

    def get_search_results(self):
        self.wait_for_element(self.SEARCH_RESULTS)
        return self.find_element(self.SEARCH_RESULTS)

    def is_search_results_displayed(self):
        try:
            self.wait_for_element(self.SEARCH_RESULTS)
            return True
        except Exception:
            return False
