import pytest
import requests
import json
import allure
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv('BASE_URL','https://tryhackme.com')

@allure.epic('EPIC 1: Функциональное тестирование TryHackMe')
@allure.feature('Feature 1.8: Тестирование авторизации API')
@allure.story('Story 1.8.1: Негативный сценарий: вход с неверными данными')
@pytest.mark.parametrize("url, expected_status_code", [
    ("https://tryhackme.com/api/v2/auth/login", 403),

])
def test_api_login_invalid_credentials(url, expected_status_code):
    with allure.step(f'Подготовка тестовых данных и payload'):

        payload = json.dumps({
            "login": os.getenv("INVALID_TEST_LOGIN"),
            "password": os.getenv("INVALID_TEST_PASSWORD"),
        })

        headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        }

    with allure.step(f'Вызов метода POST: {url} с неверными данными'):
        response = requests.request("POST", url, headers=headers, data=payload)

    with allure.step(f'Проверка статус кода: {expected_status_code}'):
        assert response.status_code == expected_status_code, \
            f'Статус код не совпадает. Ожидался {expected_status_code}, получен {response.status_code}. ' \
            f'Ответ сервера: {response.text}'
    with allure.step('Проверка сообщения об ошибке в теле ответа JSON'):
        try:
            response_json = response.json()
            expected_error_message = 'There was a problem, please try again later.'

            assert 'message' in response_json, "В JSON ответе отсутствует ключ 'message'"
            assert response_json["message"] == expected_error_message, \
                f"Ожидалось сообщение: '{expected_error_message}', получено: '{response_json['message']}'"

        except json.JSONDecodeError:
            pytest.fail('Ответ сервера не является валидным JSON')