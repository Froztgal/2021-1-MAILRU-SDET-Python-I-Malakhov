import allure
from ui.pages.base_page import BasePage
from ui.locators.locators_android import MainPageANDROIDLocators


class MainPageANDROID(BasePage):
    locators = MainPageANDROIDLocators()

    @allure.step("Ищем {text}...")
    def send_value_and_find_text(self, text, returnable=False):
        self.click_for_android(self.locators.KEYBOARD_BUTTON)
        self.find(self.locators.SEARCH_FIELD).send_keys(text)
        self.click_for_android(self.locators.TEXT_INPUT_BUTTON)
        if returnable:
            return self.find(self.locators.result_locator(text)).text

    @allure.step("Нажимаем на кнопку открытия клавиатуры...")
    def click_on_keyboard_button(self):
        self.click_for_android(self.locators.KEYBOARD_BUTTON)

    @allure.step("Нажимаем на кнопку открытия меню...")
    def click_on_menu_button(self):
        self.click_for_android(self.locators.ASSISTANT_MENU_BUTTON)

    @allure.step("Вводим '{text}' в строку поиска...")
    def type_in_search_field(self, text):
        self.find(self.locators.SEARCH_FIELD).send_keys(text)

    @allure.step("Нажимаем на кнопку поиска...")
    def click_on_search_button(self):
        self.click_for_android(self.locators.TEXT_INPUT_BUTTON)

    @allure.step("Нажимаем на кнопку сокрытия экранной клавиатуры...")
    def hide_keyboard_button(self):
        self.driver.hide_keyboard()

    @allure.step("Ищем нужный элемент из предложений и свайпаем...")
    def find_and_swipe(self):
        self.swipe_to_element_left(self.locators.SUGGESTED_LIST, 5)

    @allure.step("Ищем нужный элемент из предложений и свайпаем...")
    def click_on_suggestion(self):
        self.click_for_android(self.locators.NEEDED_SUGGESTION)
