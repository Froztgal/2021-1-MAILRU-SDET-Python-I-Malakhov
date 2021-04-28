import allure
from ui.pages.base_page import BasePage
from ui.locators.pages_locators import AudiencePageLocators
from selenium.common.exceptions import TimeoutException as TE


class AudiencePage(BasePage):

    url = 'https://target.my.com/segments/segments_list'
    locators = AudiencePageLocators()

    @allure.step('Creating segment {segment_name}...')
    def create_segment(self, segment_name):
        try:
            self.click(self.locators.CREATE_SEGMENT_BUTTON_2)
        except:
            self.click(self.locators.CREATE_SEGMENT_BUTTON_1)
        self.click(self.locators.CHECKBOX_1)
        self.click(self.locators.ADD_SEGMENT_BUTTON)
        self.fulfill(self.locators.NAME_FIELD, segment_name)
        self.click(self.locators.FINALLY_CREATE_SEGMENT_BUTTON)

    @allure.step('Deleting {segment_name}...')
    def delete_segment(self, segment_name):
        try:
            seg_id = self.check_segment(segment_name)
            self.click(self.locators.get_checkbox_by_id(seg_id))
            self.click(self.locators.ACTION_BUTTON)
            self.click(self.locators.DELETE_BUTTON)
            return seg_id
        except:
            return None

    @allure.step('Checking {segment_name}...')
    def check_segment(self, segment_name):
        try:
            self.fulfill(self.locators.FIND_FIELD, segment_name)
            element = self.find(self.locators.get_check_field_by_name(segment_name))
            seg_id = element.get_attribute('data-id')
            element.click()
            return seg_id
        except TE:
            return None
        except Exception as e:
            raise e
