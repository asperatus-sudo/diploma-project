import pytest
import requests
import allure
import time
import os
from dotenv import load_dotenv
from requests.exceptions import Timeout, RequestException

load_dotenv()

BASE_URL = os.getenv('BASE_URL')

SECURITY_HEADERS_TO_CHECK = [
    ('Content-Security-Policy', False), # Защита от XSS и внедрения кода
    ('Strict-Transport-Security', False), # Принудительное HTTPS-соединение
    ('X-Content-Type-Options', False), # Защита от MIME-sniffing
    ('X-Frame-Options', False), # Защита от Clickjacking
    ('Referrer-Policy', False), # Управление информацией о переходе (Referrer)
    ('Permissions-Policy', False), # Управление доступом к функциям браузера (камера, микрофон)
    ('Content-Type', True), # Базовый заголовок: тип контента
    ('Server', True),  # Базовый заголовок: ПО сервера
]

@pytest.fixture(scope="module")
def security_response():
    url = f"{os.getenv('BASE_URL')}/login"
    try:
        return requests.get(url, timeout=10)
    except Exception as e:
        pytest.fail(f"Сайт недоступен: {e}")

@allure.epic('EPIC 1: Функциональное тестирование TryHackMe')
@allure.feature('Feature 1.7: Тестирование безопасности HTTP')
@allure.story('Story 1.7.1: Аудит заголовков безопасности (Security Headers)')
@pytest.mark.parametrize('header_name, expected_presence', SECURITY_HEADERS_TO_CHECK)
def test_security_headers_presence(header_name, expected_presence, security_response):
    headers = security_response.headers
    is_present = header_name in headers

    with allure.step(f'Проверка заголовка "{header_name}"'):
        if expected_presence:
            assert is_present, f'Ошибка: Базовый заголовок "{header_name}" отсутствует!'
            assert headers[header_name], f'Заголовок "{header_name}" пустой.'
        else:
            if not is_present:
                allure.dynamic.description(f"Заголовок {header_name} отсутствует. Это уязвимость.")
                pytest.xfail(f"Баг: Заголовок {header_name} отсутствует на сервере.")
            else:
                pytest.fail(f"Заголовок {header_name} появился. Нужно обновить статус теста.")