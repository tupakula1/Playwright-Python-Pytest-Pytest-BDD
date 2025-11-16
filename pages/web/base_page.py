# /pages/web/base_page.py

class BasePage:
    def __init__(self, page):
        self.page = page

    def open(self, url):
        """Navigate to a given URL."""
        self.page.goto(url)

    def click(self, locator):
        self.page.locator(locator).click()

    def is_visible(self, locator):
        return self.page.locator(locator).is_visible()

    def get_title(self):
        return self.page.title()
