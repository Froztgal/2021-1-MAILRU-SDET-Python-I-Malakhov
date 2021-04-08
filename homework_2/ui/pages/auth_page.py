import allure
import data
from ui.pages.base_page import BasePage
from ui.pages.main_page import MainPage
from ui.locators.pages_locators import AuthPageLocators


class AuthPage(BasePage):

    url = 'https://target.my.com/'
    locators = AuthPageLocators()

    @allure.step('Logging...')
    def login(self, email=data.email, password=data.password):
        self.click(self.locators.LOGIN_LOCATOR_1)
        self.fulfill(self.locators.EMAIL_FIELD_LOCATOR, email)
        self.fulfill(self.locators.PASSWORD_FIELD_LOCATOR, password)
        self.click(self.locators.LOGIN_LOCATOR_2)
        return MainPage(self.driver)
