import allure
from ui.pages.base_page import BasePage
from ui.locators.pages_locators import AuthPageLocators


class AuthPage(BasePage):

    def __init__(self, driver, base_url):
        super(AuthPage, self).__init__(driver, base_url)
        self.locators = AuthPageLocators()

    @allure.step('Going to Create account page...')
    def go_to_create_account_page(self):
        from ui.pages.reg_page import RegPage
        self.click(self.locators.CREATE_ACCOUNT_BUTTON)
        return RegPage(self.driver, self.base_url)

    @allure.step('Logging...')
    def login(self, username='username', password='password'):
        from ui.pages.main_page import MainPage
        self.fulfill(self.locators.USERNAME_FIELD, username)
        self.fulfill(self.locators.PASSWORD_FIELD, password)
        self.click(self.locators.LOGIN_BUTTON)
        return MainPage(self.driver, self.base_url)
