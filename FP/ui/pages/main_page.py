import allure
import logging
from ui.pages.base_page import BasePage
from ui.locators.pages_locators import MainPageLocators

logger = logging.getLogger('test')


class MainPage(BasePage):

    def __init__(self, driver, base_url):
        super(MainPage, self).__init__(driver, base_url)
        self.url += 'welcome/'
        self.locators = MainPageLocators()

    @allure.step('Logging out...')
    def go_to_login_page(self):
        from ui.pages.auth_page import AuthPage
        self.click(self.locators.LOGOUT_BUTTON)
        return AuthPage(self.driver, self.base_url)

    @allure.step('Going to Home page...')
    def go_to_home_page(self):
        self.click(self.locators.HOME_BUTTON)
        return MainPage(self.driver, self.base_url)

    @allure.step('Going to Python main page...')
    def go_to_python_main_page(self):
        self.click(self.locators.PYTHON_BUTTON_MAIN)

    @allure.step('Going to Python history page...')
    def go_to_python_history_page(self):
        element_main = self.find(self.locators.PYTHON_BUTTON_MAIN)
        element_sub = self.find(self.locators.PYTHON_BUTTON_SUB_HISTORY)
        ach = self.action_chains
        ach.move_to_element(element_main)
        ach.click(element_sub)
        ach.perform()

    @allure.step('Going to Python flask page...')
    def go_to_python_flask_page(self):
        element_main = self.find(self.locators.PYTHON_BUTTON_MAIN)
        element_sub = self.find(self.locators.PYTHON_BUTTON_SUB_FLASK)
        ach = self.action_chains
        ach.move_to_element(element_main)
        ach.click(element_sub)
        ach.perform()
        self.driver.switch_to.window(self.driver.window_handles[1])

    @allure.step('Going to Linux Centos7 page...')
    def go_to_linux_centos_page(self):
        element_main = self.find(self.locators.LINUX_BUTTON_MAIN)
        element_sub = self.find(self.locators.LINUX_BUTTON_SUB_CENTOS)
        ach = self.action_chains
        ach.move_to_element(element_main)
        ach.click(element_sub)
        ach.perform()
        self.driver.switch_to.window(self.driver.window_handles[1])

    @allure.step('Going to Network Wireshark news page...')
    def go_to_network_wireshark_news_page(self):
        element_main = self.find(self.locators.NETWORK_BUTTON_MAIN)
        element_sub = self.find(self.locators.NETWORK_BUTTON_SUB_WIRESHARK_NEWS)
        ach = self.action_chains
        ach.move_to_element(element_main)
        ach.click(element_sub)
        ach.perform()
        self.driver.switch_to.window(self.driver.window_handles[1])

    @allure.step('Going to Network Wireshark download page...')
    def go_to_network_wireshark_download_page(self):
        element_main = self.find(self.locators.NETWORK_BUTTON_MAIN)
        element_sub = self.find(self.locators.NETWORK_BUTTON_SUB_WIRESHARK_DOWNLOAD)
        ach = self.action_chains
        ach.move_to_element(element_main)
        ach.click(element_sub)
        ach.perform()
        self.driver.switch_to.window(self.driver.window_handles[1])

    @allure.step('Going to Network TCPDUMP page...')
    def go_to_network_tcpdump_page(self):
        element_main = self.find(self.locators.NETWORK_BUTTON_MAIN)
        element_sub = self.find(self.locators.NETWORK_BUTTON_SUB_TCP_DUMP)
        ach = self.action_chains
        ach.move_to_element(element_main)
        ach.click(element_sub)
        ach.perform()
        self.driver.switch_to.window(self.driver.window_handles[1])

    @allure.step('Going to API page...')
    def go_to_api_page(self):
        self.click(self.locators.API_BUTTON)
        self.driver.switch_to.window(self.driver.window_handles[1])

    @allure.step('Going to future of internet page...')
    def go_to_internet_page(self):
        self.click(self.locators.INTERNET_BUTTON)
        self.driver.switch_to.window(self.driver.window_handles[1])

    @allure.step('Going to SMTP page...')
    def go_to_smtp_page(self):
        self.click(self.locators.SMTP_BUTTON)
        self.driver.switch_to.window(self.driver.window_handles[1])

    @allure.step('Searching for logged username...')
    def get_logged_username(self):
        return self.find(self.locators.LOGGED_USER)

    @allure.step('Searching for VK_ID...')
    def get_vk_id(self, socket_client, id):
        url = 'vk_id_add/superuser'
        socket_client.mock_post(url, jdata={'vk_id': id})
        self.driver.refresh()
        return self.find(self.locators.VK_ID_FIELD)
