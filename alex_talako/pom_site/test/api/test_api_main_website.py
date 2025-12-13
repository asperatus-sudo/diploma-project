import pytest
import requests
import allure
from requests.exceptions import Timeout, RequestException

BASE_URL = "https://tryhackme.com"


@allure.epic('Доступность сайта')
@allure.feature('Главная страница')
@allure.story('Проверка работы главной страницы сайта')
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
        assert "TryHackMe" in response.text, "Ключевое слово 'TryHackMe' не найдено. Сайт не загрузился корректно."