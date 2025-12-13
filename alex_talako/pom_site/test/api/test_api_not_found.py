import pytest
import requests
import allure
import urllib.parse

BASE_URL = "https://tryhackme.com"


@allure.epic('Апи тесты')
@allure.feature('Негативные тесты публичных страниц и API')
@allure.story('Проверка обработки ошибок для несуществующих URL')
@pytest.mark.parametrize('invalid_endpoint_path, expected_status_code', [
    ("/api/dest", 200),
    ("/asdasdgagqewr", 200),
    ("/trum-purum", 200),
    ("/          ", 200),
    ("/id-100", 200),
    ("/!&)", 200),
])
def test_api_combined_not_found(invalid_endpoint_path, expected_status_code):
    full_url = f"{BASE_URL}{invalid_endpoint_path}"

    with allure.step(f'Подготовка тестовых данных и сессии для {full_url}'):
        headers = {
            'accept': 'text/html, application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'
        }
        session = requests.Session()

    with allure.step(f'Вызов метода GET: {full_url}'):
        response = session.get(full_url, headers=headers)

    with allure.step(f'Проверка статус кода: {expected_status_code}'):
        assert response.status_code == expected_status_code, \
            f'Статус код не равен {expected_status_code}. Получен {response.status_code}'

    with allure.step('Гибкая проверка конечного URL с учетом декодирования'):
        final_url = response.url

        # urllib.parse.unquote переведет %20 обратно в пробел, а %21 обратно в !
        final_url_decoded = urllib.parse.unquote(final_url)

        if "/api/" in invalid_endpoint_path:
            expected_final_url = BASE_URL + "/not-found"
            assert final_url_decoded == expected_final_url, \
                f"Ожидался редирект на {expected_final_url} для API, но получен {final_url_decoded}"
        else:
            # исходный full_url для сравнения с декодированным фактическим URL
            assert final_url_decoded == full_url, \
                f"Ожидалось остаться на {full_url}, но произошел неожиданный редирект на {final_url_decoded}"