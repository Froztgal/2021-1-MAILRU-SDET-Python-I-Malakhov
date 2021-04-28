import allure
from ui.pages.base_page import BasePage
from ui.locators.pages_locators import CompanyCreationPageLocators


class CompanyCreationPage(BasePage):

    url = 'https://target.my.com/campaign/new'
    locators = CompanyCreationPageLocators()

    @allure.step('Creating company...')
    def create_company(self, name, file_path):
        self.click(self.locators.TRAFIC_CONVERSION_BUTTON)
        self.fulfill(self.locators.URL_FIELD_1, self.driver.current_url)
        self.click(self.locators.COMPANY_NAME_FIELD)
        self.fulfill(self.locators.COMPANY_NAME_FIELD, name)
        element = self.find(self.locators.FORMAT_BUTTON)
        self.scroll_to(element)
        self.click(self.locators.FORMAT_BUTTON)
        element = self.find(self.locators.IMAGE_UPLOAD_BUTTON_0)
        self.scroll_to(element)
        self.upload(self.locators.IMAGE_UPLOAD_BUTTON, file_path)
        self.click(self.locators.IMAGE_SAVE_BUTTON)
        self.fulfill(self.locators.URL_FIELD_2, self.driver.current_url)
        element = self.find(self.locators.SUBMIT_BUTTON)
        self.scroll_to(element)
        self.click(self.locators.SUBMIT_BUTTON)

    @allure.step('Cheking existance of Company...')
    def check_company(self, name):
        self.fulfill(self.locators.FIND_FIELD, name)
        return self.find(self.locators.get_check_field_by_name(name))
