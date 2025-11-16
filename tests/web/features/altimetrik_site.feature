Feature: Validate Altimetrik Website Functionality
    Background:
        Given I open the Altimetrik landing page


    Scenario: Verify Altimetrik landing page is loaded
        Then the landing page title should contain "Altimetrik"
        And the Altimetrik logo should be visible