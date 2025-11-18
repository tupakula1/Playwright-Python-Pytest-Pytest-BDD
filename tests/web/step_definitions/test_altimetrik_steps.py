# /tests/web/step_definitions/test_altimetrik_steps.py

import pytest
import yaml
from pytest_bdd import scenarios, given, when, then
from pages.web.home_page import HomePage
from utils.logger import get_logger

logger = get_logger("STEP_DIFINITION")

# Playwright page fixture (browser created in your main conftest)
@pytest.fixture
def home_page(page):
    return HomePage(page)


# Load Feature
scenarios("../features/altimetrik_site.feature")


# -------------------- Step Definitions -------------------- #

@given("I open the Altimetrik landing page")
def open_landing_page(home_page, config):
    base_url = config.get("base_url")
    home_page.open(base_url)


@then('the landing page title should contain "Altimetrik"')
def validate_title(home_page):
    assert "Altimetrik" in home_page.get_title()
   

@then("the Altimetrik logo should be visible")
def validate_logo(home_page):
    logger.info("*** Validating Altimetrik logo visibility *** ")
    assert home_page.verify_logo_displayed(), "Altimetrik logo is NOT visible"
