# conftest.py
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser_instance(config):
    with sync_playwright() as playwright:
        browser = playwright[config["browser"]].launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture
def page(browser_instance):
    context = browser_instance.new_context()
    page = context.new_page()
    yield page
    context.close()
