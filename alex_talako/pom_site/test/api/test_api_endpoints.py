import pytest
import requests
import allure
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv('BASE_URL')

@allure.epic('EPIC 1: Функциональное тестирование TryHackMe')
@allure.feature('Feature 1.2: Доступность публичных страниц')
@allure.story('Story 1.2.1: Проверка статус-кодов основных эндпоинтов')
@pytest.mark.parametrize('endpoint_path, expected_status_code, expected_final_path', [
    ("/challenges", 200, "/challenges"),
    ("/pricing", 200, "/pricing"),
    ("/login", 200, "/login"),
    ("/hacktivities", 200, "/hacktivities"),
    ("/dashboard", 200, "/dashboard"),
])
def test_public_endpoints_status(endpoint_path, expected_status_code,expected_final_path):
    full_url = f"{BASE_URL}{endpoint_path}"
    with allure.step(f'Подготовка тестовых данных для {full_url}'):
        payload = {}
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        }

        # Мы изолируем каждый тест
        session = requests.Session()

    with allure.step(f'Вызов метода: {full_url}'):
        response = session.get(full_url, headers=headers, data=payload)

    with allure.step(f'Проверка статус кода для: {full_url}'):
        assert response.status_code == expected_status_code, \
            f'Статус код не совпадает. Ожидался {expected_status_code}, получен {response.status_code}'

    with allure.step('Проверка, что конечный URL соответствует ожидаемому пути'):
        final_url = response.url
        expected_full_url = BASE_URL + expected_final_path
        assert final_url == expected_full_url, \
            f"Ожидалась страница {expected_full_url}, но в итоге перенаправлены на {final_url}"

    with allure.step('Проверка на not-found'):
        assert "/not-found" not in final_url, \
            f"Перешли на страницу ошибки {final_url}"
