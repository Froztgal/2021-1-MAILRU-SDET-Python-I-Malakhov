from selenium.webdriver.common.by import By


class BasePageLocators:
    pass


class AuthPageLocators:
    USERNAME_FIELD = (By.ID, "username")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "submit")
    CREATE_ACCOUNT_BUTTON = (By.XPATH, "//a[@href=\"/reg\"]")
    FLASH_FIELD = (By.ID, "flash")


class MainPageLocators:
    # Upper menu
    HOME_BUTTON = (By.XPATH, "//a[@href=\"/\"]")
    # Python
    PYTHON_BUTTON_MAIN = (By.XPATH, "//a[@href=\"https://www.python.org/\"]")
    PYTHON_BUTTON_SUB_HISTORY = (By.XPATH, "//a[@href=\"https://en.wikipedia.org/wiki/History_of_Python\"]")
    PYTHON_BUTTON_SUB_FLASK = (By.XPATH, "//a[@href=\"https://flask.palletsprojects.com/en/1.1.x/#\"]")
    # Linux
    LINUX_BUTTON_MAIN = (By.XPATH, "//a[contains(text(), 'Linux')]")
    LINUX_BUTTON_SUB_CENTOS = (By.XPATH, "//a[@href=\"https://getfedora.org/ru/workstation/download/\"]")
    # Network
    NETWORK_BUTTON_MAIN = (By.XPATH, "//a[contains(text(), 'Network')]")
    NETWORK_BUTTON_SUB_WIRESHARK_NEWS = (By.XPATH, "//a[@href=\"https://www.wireshark.org/news/\"]")
    NETWORK_BUTTON_SUB_WIRESHARK_DOWNLOAD = (By.XPATH, "//a[@href=\"https://www.wireshark.org/#download\"]")
    NETWORK_BUTTON_SUB_TCP_DUMP = (By.XPATH, "//a[@href=\"https://hackertarget.com/tcpdump-examples/\"]")
    LOGOUT_BUTTON = (By.XPATH, "//a[@href=\"/logout\"]")

    LOGGED_USER = (By.XPATH, f"//li[contains(text(), 'Logged as')]")
    VK_ID_FIELD = (By.XPATH, "//li[contains(text(), 'VK ID')]")
    # MainFrame
    API_BUTTON = (By.XPATH, "//img[@src=\"/static/images/laptop.png\"]")
    INTERNET_BUTTON = (By.XPATH, "//img[@src=\"/static/images/loupe.png\"]")
    SMTP_BUTTON = (By.XPATH, "//img[@src=\"/static/images/analytics.png\"]")


class RegisterPageLocators:
    USERNAME_FIELD = (By.ID, "username")
    EMAIL_FIELD = (By.ID, "email")
    PASSWORD_FIELD = (By.ID, "password")
    CONFIRM_PASSWORD_FIELD = (By.ID, "confirm")
    CONFIRM_CHECKBOX = (By.ID, "term")
    REGISTER_BUTTON = (By.ID, "submit")
    LOGIN_BUTTON = (By.XPATH, "//a[@href=\"/login\"]")
    FLASH_FIELD = (By.ID, "flash")
