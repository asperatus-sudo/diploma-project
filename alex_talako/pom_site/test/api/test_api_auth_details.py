import pytest
import requests
import allure
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv('BASE_URL','https://tryhackme.com')
COOKIES_FROM_ENV = os.getenv("AUTH_COOKIE")

# Не забывать про куки
AUTH_HEADERS = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'Cookie': COOKIES_FROM_ENV
}


@allure.epic('EPIC 1: Функциональное тестирование TryHackMe')
@allure.feature('Feature 1.1: Профиль и аутентификация API')
@allure.story('Story 1.1.1: Валидация данных аутентифицированного пользователя')
def test_auth_details():
    api_url = f'{BASE_URL}/api/v2/users/self'

    session = requests.Session()
    session.headers.update(AUTH_HEADERS)

    with allure.step(f'Отправка GET запроса к {api_url}'):
        response = session.get(api_url)

    with allure.step('Проверка статус-кода HTTP 200 OK'):
        if response.status_code in [401, 403]:
            pytest.fail(
                f'Куки авторизации просрочены или невалидны. Их следует обновить. Получен статус {response.status_code}.')

        assert response.status_code == 200, \
            f'Ожидался статус-код 200, получен {response.status_code}.'

    with allure.step('Проверка наличия данных в теле ответа'):
        assert response.text, "Тело ответа не должно быть пустым"
        data = response.json()
        user_data = data.get('data').get('user')
        local_data = data.get('data').get('user').get('local')

        test_username = os.getenv('TEST_USERNAME')
        test_email = os.getenv('TEST_LOGIN')

    with allure.step('Проверка username в теле ответа'):
        assert user_data.get('username') == test_username, f"Username не совпал"

    with allure.step('Проверка email в теле ответа'):
        assert user_data.get('email') == test_email, f"Email не совпал"

    with allure.step('Проверка типа данных isPremium'):
        assert isinstance(user_data.get('isPremium'), bool), "isPremium должен быть булевым значением"

    with allure.step('Проверка соответствия страны'):
        assert local_data.get('country') == 'by', f"Ожидалась страна 'by', получена '{local_data.get('country')}'"

    with allure.step('Проверка типа данных _id'):
        assert isinstance(user_data.get('_id'), str), "ID пользователя должен быть строкой"