# /pages/web/base_page.py

from asyncio import wait_for
from playwright.sync_api import expect
from utils.logger import get_logger


class BasePage:
    def __init__(self, page):
        self.page = page
        self.logger = get_logger(self.__class__.__name__)

    def open(self, url):
        """Navigate to a given URL."""
        self.page.goto(url,wait_until="load")

    def click(self, locator):
        """Click with auto-wait"""
        self.page.locator(locator).click()

    def is_visible(self, locator):
        """Simple visibility check"""
        return self.page.locator(locator).is_visible()
    
    def is_visible_with_wait(self, locator, timeout=5000):
        """
        Wait for element to be visible using expect API.
        """
        element = self.page.locator(locator)
        expect(element).to_be_visible(timeout=timeout)
        return True

    def get_title(self):
        return self.page.title()
    
    def wait_for_title(self, text, timeout=5000):
        """
        Wait for page.title() to contain expected text.
        """
        expect(self.page).to_have_title(text, timeout=timeout)
        
    def wait_for_text(self, locator, text, timeout=5000):
        """
        Wait until text is visible inside a locator.
        """
        element = self.page.locator(locator)
        expect(element).to_have_text(text, timeout=timeout)
        return True
