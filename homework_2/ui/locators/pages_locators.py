from selenium.webdriver.common.by import By


class BasePageLocators:
    pass


class AuthPageLocators:
    # Login locators
    LOGIN_LOCATOR_1 = (By.XPATH, "//div[contains(text(), 'Войти')]")
    EMAIL_FIELD_LOCATOR = (By.NAME, 'email')
    PASSWORD_FIELD_LOCATOR = (By.NAME, 'password')
    LOGIN_LOCATOR_2 = (By.XPATH, "(//div[contains(text(), 'Войти')])[2]")


class MainPageLocators:
    # Section locators
    COMPANY_LOCATOR = (By.XPATH, "//a[@href=\"/dashboard\"]")
    AUDIENCE_LOCATOR = (By.XPATH, "//a[@href=\"/segments\"]")
    # BILLING_LOCATOR = (By.XPATH, "//a[@href=\"/billing\"]")
    # STATISTICS_LOCATOR = (By.XPATH, "//a[@href=\"/statistics\"]")
    # PRO_LOCATOR = (By.XPATH, "//a[@href=\"/pro\"]")
    # PROFILE_LOCATOR = (By.XPATH, "//a[@href=\"/profile\"]")
    # TOOLS_LOCATOR = (By.XPATH, "//a[@href=\"/tools\"]")
    # HELP_LOCATOR = (By.XPATH, "//a[@href=\"//target.my.com/help/advertisers/ru\"]")

    # Create company buttons
    CREATE_COMPANY_BUTTON_1 = (By.XPATH, "//a[@href='/campaign/new']")
    CREATE_COMPANY_BUTTON_2 = (By.XPATH, "//div[contains(text(), 'Создать кампанию')]")


class CompanyCreationPageLocators:
    TRAFIC_CONVERSION_BUTTON = (By.XPATH, "//div[contains(text(), 'Трафик')]")
    URL_FIELD_1 = (By.XPATH, "//input[@placeholder='Введите ссылку']")
    COMPANY_NAME_FIELD = (By.XPATH, "//div[@class='campaign-name']//input")
    FORMAT_BUTTON = (By.ID, "patterns_4")
    IMAGE_UPLOAD_BUTTON_0 = (By.XPATH, "//div[contains(text(), '240 × 400')]")
    IMAGE_UPLOAD_BUTTON = (By.XPATH, "(//input[@type='file'])[2]")
    IMAGE_SAVE_BUTTON = (By.XPATH, "//input[@value='Сохранить изображение']")
    URL_FIELD_2 = (By.XPATH, "//input[@placeholder='Введите адрес ссылки']")
    SUBMIT_BUTTON = (By.XPATH, "(//button[@data-class-name='Submit'])[2]")
    FIND_FIELD = (By.XPATH, "//input[@placeholder='Поиск...']")

    @staticmethod
    def get_check_field_by_name(campaign_name):
        return By.XPATH, f"//li[@title='{campaign_name}']"


class AudiencePageLocators(BasePageLocators):
    CREATE_SEGMENT_BUTTON_1 = (By.XPATH, "//a[@href='/segments/segments_list/new/']")
    CREATE_SEGMENT_BUTTON_2 = (By.XPATH, "//div[contains(text(), 'Создать')]")
    CHECKBOX_1 = (By.XPATH, "//input[@type='checkbox']")
    ADD_SEGMENT_BUTTON = (By.XPATH, "(//button[@data-class-name='Submit'])[2]")
    NAME_FIELD = (By.XPATH, "//input[@maxlength='60']")
    FINALLY_CREATE_SEGMENT_BUTTON = (By.XPATH, "//button[@data-class-name='Submit']")
    ACTION_BUTTON = (By.XPATH, "//span[contains(text(), 'Действия')]")
    DELETE_BUTTON = (By.XPATH, "//li[contains(text(), 'Удалить')]")
    FIND_FIELD = (By.XPATH, "//input[@placeholder='Поиск по названию или id...']")

    @staticmethod
    def get_check_field_by_name(segment_name):
        return By.XPATH, f"//li[contains(text(), '{segment_name}')]"

    @staticmethod
    def get_checkbox_by_id(segment_id):
        return By.XPATH, f"//span[contains(text(), '{segment_id}')]/preceding-sibling::input"

