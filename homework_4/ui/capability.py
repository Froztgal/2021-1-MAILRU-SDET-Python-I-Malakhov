import os
from selenium import webdriver


def capability_select(device_os, download_dir):
    capability = None
    if device_os == 'android':
        capability = {"platformName": "Android",
                      "platformVersion": "8.1",
                      "automationName": "Appium",
                      "appPackage": "ru.mail.search.electroscope",
                      "appActivity": ".ui.activity.AssistantActivity",
                      "app": os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                          '../apk/Marussia_v1.39.1.apk')
                                             ),
                      "orientation": "PORTRAIT",
                      'autoGrantPermissions': 'true'
                      }
    else:
        raise ValueError("Incorrect device os type")
    return capability