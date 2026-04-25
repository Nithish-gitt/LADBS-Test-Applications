import pytest
import allure
from datetime import datetime


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        # Capture screenshot on failure if driver exists
        if hasattr(item.instance, 'driver') and item.instance.driver:
            try:
                screenshot = item.instance.driver.get_screenshot_as_png()
                allure.attach(
                    screenshot,
                    name=f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception:
                pass


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: mark test as regression test"
    )
