from selenium.webdriver.common.by import By

# Login locators
LOGIN_LOCATOR_1 = (By.XPATH, "//div[contains(text(), 'Войти')]")
EMAIL_FIELD_LOCATOR = (By.NAME, 'email')
PASSWORD_FIELD_LOCATOR = (By.NAME, 'password')
LOGIN_LOCATOR_2 = (By.CLASS_NAME, "authForm-module-button-2G6lZu")

# Logout locators
LOGOUT_LOCATOR_1 = (By.XPATH, "//div[contains(text(), 'Баланс: ')]")
LOGOUT_LOCATOR_2 = (By.XPATH, "//a[@href=\"/logout\"]")

# Profile locators
PROFILE_FIO_LOCATOR = (By.XPATH, "//div[@data-name=\"fio\"]/div/input")
PROFILE_EMAIL_LOCATOR = (By.XPATH, "//div[@data-class-name=\"AdditionalEmailRow\"]/div/div/div/input")
PROFILE_PHONE_LOCATOR = (By.XPATH, "//div[@data-name=\"phone\"]/div/input")
SAVE_BUTTON_LOCATOR = (By.CLASS_NAME, "button__text")

# Section locators
COMPANY_LOCATOR = (By.XPATH, "//a[@href=\"/dashboard\"]")
# AUDIENCE_LOCATOR = (By.XPATH, "//a[@href=\"/segments\"]")
# BILLING_LOCATOR = (By.XPATH, "//a[@href=\"/billing\"]")
STATISTICS_LOCATOR = (By.XPATH, "//a[@href=\"/statistics\"]")
PRO_LOCATOR = (By.XPATH, "//a[@href=\"/pro\"]")
PROFILE_LOCATOR = (By.XPATH, "//a[@href=\"/profile\"]")
# TOOLS_LOCATOR = (By.XPATH, "//a[@href=\"/tools\"]")
# HELP_LOCATOR = (By.XPATH, "//a[@href=\"//target.my.com/help/advertisers/ru\"]")
