import os
from dotenv import load_dotenv
import allure
from alex_talako.pom_site.locators.login_locators.login_page import LoginPage

load_dotenv()

BASE_URL = os.getenv('BASE_URL')
LOGIN = os.getenv('TEST_LOGIN')
PASSWORD = os.getenv('TEST_PASSWORD')


@allure.epic('EPIC 2: Функциональное тестирование TryHackMe')
@allure.feature('Feature 2.4: UI Авторизация и доступ к форме')
@allure.story('Story 2.4.1: Валидация полей ввода и доступности элементов логина')
def test_login_successfully(web_browser):

    driver = LoginPage(web_browser)

    with allure.step('Переход к форме логина'):
        driver.btn_cookie.click()
        driver.btn_header_log_in.click()
        assert '/login' in web_browser.current_url, 'Ошибка: Не удалось перейти на страницу логина'

    with allure.step('Проверка отрисовки полей'):
        assert driver.btn_username_or_email.is_visible(), 'Поле ввода логина отсутствует'
        assert driver.btn_password.is_visible(), 'Поле ввода пароля отсутствует'
        assert driver.btn_log_in_account.is_visible(), "Кнопка 'Log in' не найдена"

    with allure.step('Имитация ввода и проверка активности'):
        driver.btn_username_or_email.send_keys(LOGIN)
        driver.btn_password.send_keys(PASSWORD)

        assert driver.btn_log_in_account.is_clickable(), 'Кнопка входа заблокирована после ввода данных'

    with allure.step('Проверка доступности ссылок регистрации и Magic Link'):
        assert driver.btn_send_magic_link.is_visible(), 'Ссылка Magic Link не найдена'
        assert driver.btn_sign_up.is_visible(), 'Ссылка Sign Up не найдена'
