import logging
import allure
import pytest
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import conftest
from ui.locators.pages_locators import BasePageLocators
from _pytest.fixtures import FixtureRequest
from utils.decorators import wait

CLICK_RETRY = 3
time_out = 5
logger = logging.getLogger('test')


class PageNotLoadedException(Exception):
    pass


class BasePage(object):

    def __init__(self, driver, base_url):
        self.base_url = base_url
        self.url = base_url
        self.driver = driver
        self.locators = BasePageLocators()
        logger.info(f'{self.__class__.__name__} page is opening...')
        self.is_complete()

    def find(self, locator, timeout=time_out):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    def find_hidden(self, locator):
        return self.driver.execute_script(f"return document.getElementById('{locator}').innerHTML;")

    @property
    def action_chains(self):
        return ActionChains(self.driver)

    def wait(self, timeout=time_out):
        return WebDriverWait(self.driver, timeout=timeout)

    def is_complete(self):
        def _status():
            return self.driver.execute_script('return arguments[0] == document.readyState;', 'complete')
        return wait(_status, error=PageNotLoadedException, check=True, timeout=time_out, interval=0.1)

    def scroll_to(self, element):
        self.driver.execute_script('arguments[0].scrollIntoView(true);', element)

    @allure.step('Typing {text} into {locator}')
    def fulfill(self, locator, text, timeout=time_out):
        logger.info(f'Typing {text} into {locator}...')
        field = self.find(locator, timeout)
        field.clear()
        field.send_keys(text)

    @allure.step('Clicking {locator}')
    def click(self, locator, timeout=time_out):
        for i in range(CLICK_RETRY):
            logger.info(f'Clicking on {locator}. Try {i+1} of {CLICK_RETRY}...')
            try:
                element = self.find(locator, timeout=timeout)
                self.scroll_to(element)
                element = self.wait(timeout).until(EC.element_to_be_clickable(locator))
                element.click()
                return
            except StaleElementReferenceException:
                if i == CLICK_RETRY - 1:
                    raise

    # @allure.step('Uploading file {file_path} in {locator}')
    # def upload(self, locator, file_path, timeout=time_out):
    #     logger.info(f'Uploading image ({file_path}) into {locator}...')
    #     upload_field = self.find(locator, timeout)
    #     upload_field.send_keys(file_path)
