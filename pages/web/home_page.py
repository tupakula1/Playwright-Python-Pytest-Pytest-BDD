# /pages/web/home_page.py

from pages.web.base_page import BasePage

class HomePage(BasePage):

    ALT_LOGO = "img[alt='Altimetrik Logo'], img[alt='Altimetrik logo'], .navbar-brand img"

    def __init__(self, page):
        super().__init__(page)

    def verify_logo_displayed(self):
        return self.is_visible(self.ALT_LOGO)
        
