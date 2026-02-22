import pytest
import requests
import allure
import os
from dotenv import load_dotenv
from requests.exceptions import Timeout, RequestException

load_dotenv()

BASE_URL = os.getenv('BASE_URL')


@allure.epic('EPIC 1: Функциональное тестирование TryHackMe')
@allure.feature('Feature 1.4: Доступность публичных страниц')
@allure.story('Story 1.4.1: Проверка работы главной страницы сайта (Smoke)')
@pytest.mark.smoke
def test_main_website_availability():
    url = f'{BASE_URL}/'

    with allure.step(f'Отправка GET запроса к {url} с таймаутом 10 секунд'):
        try:
            response = requests.get(url, timeout=10)
        except (Timeout, RequestException) as e:
            pytest.fail(f"Сайт недоступен или превышен таймаут: {e}")

    with allure.step(f'Проверка статус-кода: {url} '):
        assert response.status_code == 200, \
            f'Ожидался статус 200 OK, но получен {response.status_code}'

    with allure.step("Проверка наличия ключевого слова 'TryHackMe' в теле ответа"):
        assert "<title>TryHackMe" in response.text or "TryHackMe" in response.text, "Ключевое слово 'TryHackMe' не найдено. Сайт не загрузился корректно."