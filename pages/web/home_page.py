# /pages/web/home_page.py

from sre_parse import State
from typing import Self
from pages.web.base_page import BasePage
from utils.yaml_utils import get_locator
from utils.logger import get_logger

class HomePage(BasePage):

    # ALT_LOGO = "img[alt='Altimetrik Logo'], img[alt='Altimetrik logo'], .navbar-brand img"
    
    def __init__(self, page):
        super().__init__(page)

        # Initialize logger
        self.logger = get_logger(self.__class__.__name__)

        # Load locators once during initialization
        self.logo_locator = get_locator("home_page","alt_logo")  

    def verify_logo_displayed(self):
        self.logger.info(" *** Checking if Altimetrik logo is visible *** ")
        return self.is_visible_with_wait(self.logo_locator,timeout=8000)
       
        
