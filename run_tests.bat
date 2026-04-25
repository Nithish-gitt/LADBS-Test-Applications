@echo off
echo Running tests with Allure...
pytest tests/ --alluredir=reports/allure-results -v

echo.
echo Generating Allure report...
allure generate reports/allure-results -o reports/allure-report --clean

echo.
echo Opening Allure report...
allure open reports/allure-report
