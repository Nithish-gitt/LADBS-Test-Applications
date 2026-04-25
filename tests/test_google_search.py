import pytest
import allure
from utils.driver_factory import DriverFactory
from pages.google_search_page import GoogleSearchPage


@allure.epic("Google Search")
@allure.feature("Search Functionality")
class TestGoogleSearch:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.driver = DriverFactory.create_driver()
        self.google_search_page = GoogleSearchPage(self.driver)
        yield
        if self.driver:
            self.driver.quit()

    @allure.story("Homepage Navigation")
    @allure.title("Verify Google homepage opens successfully")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_should_open_google_homepage(self):
        with allure.step("Open Google homepage"):
            self.google_search_page.open()
        
        with allure.step("Verify page title contains 'Google'"):
            title = self.google_search_page.get_title()
            assert 'Google' in title, 'Page title should contain Google'

    @allure.story("Search Feature")
    @allure.title("Verify search for Selenium WebDriver returns results")
    @allure.severity(allure.severity_level.NORMAL)
    def test_should_search_for_selenium_webdriver(self):
        with allure.step("Open Google homepage"):
            self.google_search_page.open()
        
        with allure.step("Search for 'Selenium WebDriver'"):
            self.google_search_page.search('Selenium WebDriver')

        with allure.step("Verify search results are displayed"):
            results_displayed = self.google_search_page.is_search_results_displayed()
            assert results_displayed is True, 'Search results should be displayed'
