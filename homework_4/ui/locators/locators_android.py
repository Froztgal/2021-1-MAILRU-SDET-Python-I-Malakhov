from appium.webdriver.common.mobileby import MobileBy


class BasePageANDROIDLocators:
    pass


class MainPageANDROIDLocators(BasePageANDROIDLocators):
    KEYBOARD_BUTTON = (MobileBy.ID, 'ru.mail.search.electroscope:id/keyboard')
    SEARCH_FIELD = (MobileBy.ID, 'ru.mail.search.electroscope:id/input_text')
    TEXT_INPUT_BUTTON = (MobileBy.ID, 'ru.mail.search.electroscope:id/text_input_action')
    RESULT_HEADER = (MobileBy.ID, 'ru.mail.search.electroscope:id/item_dialog_fact_card_title')
    SUGGESTED_LIST = (MobileBy.ID, 'ru.mail.search.electroscope:id/suggests_list')
    NEEDED_SUGGESTION = (MobileBy.XPATH, '//android.widget.TextView[@text="численность населения россии"]')
    ASSISTANT_MENU_BUTTON = (MobileBy.ID, 'ru.mail.search.electroscope:id/assistant_menu_bottom')
    CHECK_NEWS = (MobileBy.ID, 'ru.mail.search.electroscope:id/player_track_name')
    # STOP_PLAYER_BUTTON = (MobileBy.ID, 'ru.mail.search.electroscope:id/play_button')

    @staticmethod
    def math_expression_result_locator(query_string):
        return MobileBy.XPATH, f'//android.widget.TextView[@text="{query_string}"]/../following-sibling::*[1]'


class MenuPageANDROIDLocators(BasePageANDROIDLocators):
    NEWS_SOURCE_BUTTON = (MobileBy.ID, 'ru.mail.search.electroscope:id/user_settings_field_news_sources')
    ABOUT_APP_BUTTON = (MobileBy.ID, 'ru.mail.search.electroscope:id/user_settings_about')

    ADDITIONAL_CHECK_NEEDED_NEWS_SOURCE = (MobileBy.ID,
                                           'ru.mail.search.electroscope:id/user_settings_field_new_sources_hint')


class NewsSourcePageANDROIDLocators(BasePageANDROIDLocators):
    NEEDED_NEWS_SOURCE = (MobileBy.XPATH, '//android.widget.TextView[@text="Вести FM"]')
    CHECK_NEEDED_NEWS_SOURCE = (MobileBy.XPATH, '//android.widget.TextView[@text="Вести FM"]/following-sibling::*[1]')


class AboutAppPageANDROIDLocators(BasePageANDROIDLocators):
    ABOUT_VERSION_TEXT = (MobileBy.ID, 'ru.mail.search.electroscope:id/about_version')
    ABOUT_COPYRIGHT_TEXT = (MobileBy.ID, 'ru.mail.search.electroscope:id/about_copyright')
