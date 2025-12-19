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

    with allure.step("Принятие куки и переход к логину"):
        driver.btn_cookie.click()
        driver.btn_header_log_in.click()

    with allure.step("Ввод учетных данных"):
        driver.btn_username_or_email.click()
        driver.btn_username_or_email.send_keys(LOGIN)
        driver.btn_password.click()
        driver.btn_password.send_keys(PASSWORD)

    with allure.step("Ожидание ручного решения капчи"):
        # Даем время на ввод капчи
        time.sleep(50)

    with allure.step("Валидация успешного входа"):
        # Ждем немного, пока прогрузится профиль
        time.sleep(5)


    with allure.step("Закрываем сезонное предложение на сайте"):
        # Сезонное, значит по окончанию декабря этот тест упадёт и надо исправить
        if driver.btn_close_proposition.is_visible():
            driver.btn_close_proposition.click()

    with allure.step("Проверка успешной авторизации"):
        assert driver.btn_profile.is_visible(), "Ошибка: Аватар профиля не найден. Авторизация не удалась."

    with allure.step("Выбираем возможные действия с профилем"):
        driver.btn_profile.click()

    with allure.step("Выбираем просмотр профиля"):
        driver.btn_view_profile.click()
        time.sleep(5)
       # Для того, чтоб увидеть, что прогрузились данные профиля

    with allure.step("Финальная валидация профиля"):
        current_url = driver.get_current_url()
        assert "/p/Asperatus." in current_url, f"Ожидался переход в профиль, но текущий URL: {current_url}"