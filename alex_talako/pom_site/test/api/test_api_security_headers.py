import pytest
import requests
import allure
import time
from requests.exceptions import Timeout, RequestException

BASE_URL = "https://tryhackme.com"

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


@allure.epic('Тестирование безопасности')
@allure.feature('HTTP Заголовки')
@allure.story('Проверка наличия или отсутствия ключевых заголовков безопасности')
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

    with allure.step(f'Проверка наличия заголовка "{header_name}" (Ожидание: {expected_presence})'):
        if expected_presence:
            assert is_present, f'Ошибка. Ожидали наличие заголовка "{header_name}", но он отсутствует'
            assert headers[header_name], f'Заголовок "{header_name}" существует, но имеет пустое значение.'
        else:
            if is_present:
                pytest.fail(
                    f'Баг исправлен. Заголовок "{header_name}" теперь существует, но мы ожидали его отсутствия.')
            else:
                pytest.skip(f'Имеется наличие бага. Заголовок "{header_name}" отсутствует, как и ожидалось.')