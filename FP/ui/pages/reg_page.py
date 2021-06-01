import allure
from ui.pages.base_page import BasePage
from ui.locators.pages_locators import RegisterPageLocators


class RegPage(BasePage):

    url = super(BasePage).url + '/reg'
    locators = RegisterPageLocators()

    @allure.step('Creating user...')
    def create_user(self, username, password, email, re_password=None, chekbox=True):
        from ui.pages.main_page import MainPage
        if re_password is None:
            re_password = password
        self.fulfill(self.locators.USERNAME_FIELD, username)
        self.fulfill(self.locators.EMAIL_FIELD, email)
        self.fulfill(self.locators.PASSWORD_FIELD, password)
        self.fulfill(self.locators.CONFIRM_PASSWORD_FIELD, re_password)
        if chekbox:
            self.click(self.locators.CONFIRM_CHECKBOX)
        self.click(self.locators.REGISTER_BUTTON)
        return MainPage(self.driver)

    @allure.step('Going to Logging page...')
    def go_to_login_page(self):
        from ui.pages.auth_page import AuthPage
        self.click(self.locators.LOGIN_BUTTON)
        return AuthPage(self.driver)

    @allure.step('Reading flash information...')
    def get_flash_information(self):
        return self.find_hidden('flash')
