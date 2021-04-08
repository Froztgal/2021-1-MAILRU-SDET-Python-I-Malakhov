import pytest
from homework_1.ui.locators import basic_locators
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from homework_1 import personal_data

time_out = 10


class BaseCase:
    driver = None
    config = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config):
        self.driver = driver
        self.config = config

    def wait(self, timeout=time_out):
        return WebDriverWait(self.driver, timeout=timeout)

    def find(self, locator, timeout=time_out):
        return self.wait(timeout).until(ec.presence_of_element_located(locator))

    def fulfill(self, locator, text, timeout=time_out):
        field = self.find(locator, timeout)
        field.clear()
        field.send_keys(text)

    def click(self, locator, timeout=time_out):
        try:
            self.find(locator, timeout)
            element = self.wait(timeout).until(ec.element_to_be_clickable(locator))
            # element.click()
            self.driver.execute_script("arguments[0].click();", element)
        except:
            raise

    @pytest.fixture(scope='function')
    def login(self):
        self.click(basic_locators.LOGIN_LOCATOR_1)
        self.fulfill(basic_locators.EMAIL_FIELD_LOCATOR, personal_data.email)
        self.fulfill(basic_locators.PASSWORD_FIELD_LOCATOR, personal_data.password)
        self.click(basic_locators.LOGIN_LOCATOR_2)
