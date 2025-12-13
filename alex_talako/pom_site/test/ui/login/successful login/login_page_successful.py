import pytest
import os
import allure
import time
from alex_talako.pom_site.locators.login_locators.login_page import LoginPage

LOGIN = os.getenv("VALID_LOGIN")
PASSWORD = os.getenv("VALID_PASSWORD")

if not LOGIN or not PASSWORD:
    pytest.skip("Переменные окружения VALID_LOGIN или VALID_PASSWORD не установлены")

@allure.description("""Этот тест совершает успешную авторизацию пользователя""")
def test_login_successfully(web_browser):

    driver = LoginPage(web_browser)
    driver.btn_cookie.click()
    driver.btn_header_log_in.click()
    driver.btn_username_or_email.click()
    driver.btn_username_or_email.send_keys(LOGIN)
    driver.btn_password.click()
    driver.btn_password.send_keys(PASSWORD)
    time.sleep(10)
    driver.btn_log_in_account.click()
    time.sleep(5)
