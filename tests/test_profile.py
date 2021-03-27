import pytest
from tests.base import BaseCase
from ui.locators import basic_locators
import personal_data


class TestProfile(BaseCase):
    @pytest.mark.UI("UI")
    def test_profile(self, login):
        rand_fio = personal_data.get_random_fio()
        rand_email = personal_data.get_random_email()
        rand_phone = personal_data.get_random_phone()
        self.click(basic_locators.PROFILE_LOCATOR)
        self.fulfill(basic_locators.PROFILE_FIO_LOCATOR, rand_fio)
        self.fulfill(basic_locators.PROFILE_EMAIL_LOCATOR, rand_email)
        self.fulfill(basic_locators.PROFILE_PHONE_LOCATOR, rand_phone)
        self.click(basic_locators.SAVE_BUTTON_LOCATOR)
        self.click(basic_locators.COMPANY_LOCATOR)
        self.click(basic_locators.PROFILE_LOCATOR)
        res_fio = self.find(basic_locators.PROFILE_FIO_LOCATOR).get_attribute('value')
        res_email = self.find(basic_locators.PROFILE_EMAIL_LOCATOR).get_attribute('value')
        res_phone = self.find(basic_locators.PROFILE_PHONE_LOCATOR).get_attribute('value')
        assert res_fio == rand_fio and res_email == rand_email and res_phone == rand_phone
