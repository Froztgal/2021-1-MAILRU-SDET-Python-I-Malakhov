import allure
from ui.pages.base_page import BasePage
from ui.locators.pages_locators import MainPageLocators


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
        self.find(self.locators.PYTHON_BUTTON_MAIN)
        self.click(self.locators.PYTHON_BUTTON_SUB_HISTORY)

    @allure.step('Going to Python flask page...')
    def go_to_python_flask_page(self):
        self.find(self.locators.PYTHON_BUTTON_MAIN)
        self.click(self.locators.PYTHON_BUTTON_SUB_FLASK)

    @allure.step('Going to Linux main page...')
    def go_to_linux_main_page(self):
        self.click(self.locators.LINUX_BUTTON_MAIN)

    @allure.step('Going to Linux Centos7 page...')
    def go_to_linux_main_page(self):
        self.find(self.locators.LINUX_BUTTON_MAIN)
        self.click(self.locators.LINUX_BUTTON_SUB_CENTOS)

    @allure.step('Going to Network main page...')
    def go_to_network_main_page(self):
        self.click(self.locators.NETWORK_BUTTON_MAIN)

    @allure.step('Going to Network Wireshark news page...')
    def go_to_network_wireshark_news_page(self):
        self.find(self.locators.NETWORK_BUTTON_MAIN)
        self.click(self.locators.NETWORK_BUTTON_SUB_WIRESHARK_NEWS)

    @allure.step('Going to Network Wireshark download page...')
    def go_to_network_wireshark_download_page(self):
        self.find(self.locators.NETWORK_BUTTON_MAIN)
        self.click(self.locators.NETWORK_BUTTON_SUB_WIRESHARK_DOWNLOAD)

    @allure.step('Going to Network TCPDUMP page...')
    def go_to_network_tcpdump_page(self):
        self.find(self.locators.NETWORK_BUTTON_MAIN)
        self.click(self.locators.NETWORK_BUTTON_SUB_TCP_DUMP)
