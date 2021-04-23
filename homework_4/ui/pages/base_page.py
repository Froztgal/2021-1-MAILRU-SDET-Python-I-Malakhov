import allure
import logging
from selenium.webdriver import ActionChains
from ui.locators.locators_web import BasePageLocators
from selenium.webdriver.support.wait import WebDriverWait
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException


CLICK_RETRY = 3
BASE_TIMEOUT = 5


logger = logging.getLogger('test')


class PageNotLoadedException(Exception):
    pass


class BasePage(object):
    locators = BasePageLocators()

    def __init__(self, driver, config):
        self.driver = driver
        self.config = config
        self.device = self.config['device_os']

        logger.info(f'{self.__class__.__name__} page is opening...')


    def find(self, locator, timeout=BASE_TIMEOUT):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    @property
    def action_chains(self):
        return ActionChains(self.driver)

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 5
        return WebDriverWait(self.driver, timeout=timeout)

    def scroll_to(self, element):
        self.driver.execute_script('arguments[0].scrollIntoView(true);', element)


    @allure.step('Clicking {locator}')
    def click_for_android(self, locator, timeout=None):
        for i in range(CLICK_RETRY):
            logger.info(f'Clicking on {locator}. Try {i+1} of {CLICK_RETRY}...')
            try:
                element = self.find(locator, timeout=timeout)
                element = self.wait(timeout).until(EC.element_to_be_clickable(locator))
                element.click()
                return
            except StaleElementReferenceException:
                if i == CLICK_RETRY - 1:
                    raise

    def swipe_up(self, swipetime=200):
        """
        Базовый метод свайпа по вертикали
        Описание работы:
        1. узнаем размер окна телефона
        2. Задаем за X - центр нашего экрана
        3. Указываем координаты откуда и куда делать свайп
        4. TouchAction нажимает на указанные стартовые координаты, немного ждет и передвигает нас из одной точки в другую.
        5. release() наши пальцы с экрана, а perform() выполняет всю эту цепочку команд.
        """
        action = TouchAction(self.driver)
        dimension = self.driver.get_window_size()
        x = int(dimension['width'] / 2)
        start_y = int(dimension['height'] * 0.8)
        end_y = int(dimension['height'] * 0.2)
        action. \
            press(x=x, y=start_y). \
            wait(ms=swipetime). \
            move_to(x=x, y=end_y). \
            release(). \
            perform()

    def swipe_to_element_up(self, locator, max_swipes):
        """
        :param locator: локатор, который мы ищем
        :param max_swipes: количество свайпов до момента, пока тест не перестанет свайпать вверх
        """
        already_swiped = 0
        while not self.driver.find_elements(*locator):
            if already_swiped > max_swipes:
                raise TimeoutException(f"Error with {locator}, please check function")
            self.swipe_up()
            already_swiped += 1

    def swipe_element_lo_left(self, locator, half=True):
        """
        :param half: прокручивать на половину
        :param locator: локатор, который мы ищем
        1. Находим наш элемент на экране
        2. Получаем его координаты (начала, конца по ширине и высоте)
        3. Находим центр элемента (по высоте)
        4. Делаем свайп влево, двигая центр элемента за его правую часть в левую сторону.
        """

        window_size = self.driver.get_window_size()
        max_width = window_size["width"] - 1
        web_element = self.find(locator, 10)
        left_x = web_element.location['x']
        if web_element.rect['width'] > max_width:
            tmp_width = max_width
        else:
            tmp_width = web_element.rect['width']
        if half:
            tmp_width = tmp_width / 2
        right_x = left_x + tmp_width
        upper_y = web_element.location['y']
        lower_y = upper_y + web_element.rect['height']
        middle_y = (upper_y + lower_y) / 2
        action = TouchAction(self.driver)
        action. \
            press(x=right_x, y=middle_y). \
            wait(ms=300). \
            move_to(x=left_x, y=middle_y). \
            release(). \
            perform()

    def swipe_to_element_left(self, locator, max_swipes, half=True):
        """
        :param half: прокручивать на половину
        :param locator: локатор, который мы ищем
        :param max_swipes: количество свайпов до момента, пока тест не перестанет свайпать вверх
        """
        already_swiped = 0
        while not self.driver.find_elements(*locator):
            if already_swiped > max_swipes:
                raise TimeoutException(f"Error with {locator}, please check function")
            self.swipe_element_lo_left(locator, half=half)
            already_swiped += 1