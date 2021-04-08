import allure
from ui.pages.base_page import BasePage
from ui.pages.audience_page import AudiencePage
from ui.pages.company_creation_page import CompanyCreationPage
from ui.locators.pages_locators import MainPageLocators


class MainPage(BasePage):

    url = 'https://target.my.com/dashboard'
    locators = MainPageLocators()

    @allure.step('Going to Company creation page...')
    def go_to_company_creation(self):
        try:
            self.click(self.locators.CREATE_COMPANY_BUTTON_2)
        except:
            self.click(self.locators.CREATE_COMPANY_BUTTON_1)
        return CompanyCreationPage(self.driver)

    @allure.step('Going to Audience section page...')
    def go_to_audience(self, ):
        self.click(self.locators.AUDIENCE_LOCATOR)
        return AudiencePage(self.driver)
