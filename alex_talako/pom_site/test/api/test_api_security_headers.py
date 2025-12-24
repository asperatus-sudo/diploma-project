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


@allure.epic('EPIC 1: Функциональное тестирование TryHackMe')
@allure.feature('Feature 1.7: Тестирование безопасности HTTP')
@allure.story('Story 1.7.1: Аудит заголовков безопасности (Security Headers)')
@pytest.mark.parametrize('header_name, expected_presence', SECURITY_HEADERS_TO_CHECK)
def test_security_headers_presence(header_name, expected_presence):
    url = f'{BASE_URL}/login'
    session = requests.Session()

    with allure.step(f'Отправка GET запроса к {url}'):
        try:
            response = session.get(url, timeout=10)
        except (Timeout, RequestException) as e:
            pytest.fail(f"Сайт недоступен для проверки заголовков: {e}")

    time.sleep(2)

    headers = response.headers
    is_present = header_name in headers

    with allure.step(f'Проверка заголовка "{header_name}"'):
        if expected_presence:
            # Мы ожидаем заголовок (как Content-Type), и его нет — это ошибка
            assert is_present, f'Ошибка: Базовый заголовок "{header_name}" отсутствует!'
            assert headers[header_name], f'Заголовок "{header_name}" пустой.'
        else:
            # Мы знаем, что заголовка НЕТ, но он ДОЛЖЕН быть в хорошей ситуации
            if not is_present:
                allure.dynamic.description(f"Заголовок {header_name} отсутствует. Это уязвимость.")
                pytest.xfail(f"Баг: Заголовок {header_name} отсутствует на сервере.")
            else:
                # Если вдруг заголовок появился (баг исправили)
                pytest.fail(f"Заголовок {header_name} появился. Нужно обновить статус теста на True.")