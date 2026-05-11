import pytest
import requests
import allure
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv('BASE_URL')

PUBLIC_HEADERS = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'referer': 'tryhackme.com',
}

@allure.epic('EPIC 1: Функциональное тестирование TryHackMe')
@allure.feature('Feature 1.6: Детализация публичной комнаты API')
@allure.story('Story 1.6.1: Проверка данных комнаты "Pickle Rick" для неавторизованного пользователя')
def test_get_room_details_public():
    room_code = 'picklerick'
    base_api_url = f'{BASE_URL}/api/v2/rooms/details'
    params = {'roomCode': room_code}

    print(f'\nТестируемый URL: {base_api_url} с параметром {params}')
    with allure.step(f'Отправка GET запроса к {base_api_url} с параметром {params}'):
        response = requests.get(base_api_url, headers=PUBLIC_HEADERS, params=params)

    with allure.step('Проверка статус-кода HTTP 200 OK'):
        assert response.status_code == 200, \
            f'Ожидался статус-код 200, получен {response.status_code}. Тело ответа:\n{response.text[:500]}'

    with allure.step('Декодирование ответа JSON'):
        try:
            data = response.json()
            print('Ответ успешно декодирован как JSON')
        except requests.exceptions.JSONDecodeError as e:
            pytest.fail(f'Не удалось декодировать ответ как JSON. Ошибка: {e}\n{response.text[:500]}')
            return

    room_data = data.get('data', {})
    with allure.step('Проверка наличия вложенного ключа "data"'):
        assert room_data is not None, "В ответе API отсутствует вложенный ключ 'data'"

    room_title = room_data.get('title', {})
    expected_titles = ['Pickle Rick']
    with allure.step(f'Проверка названия комнаты: {room_title}'):
        assert room_title in expected_titles, f"Неверное название комнаты. Ожидалось одно из {expected_titles}, получено '{room_title}'"

    with allure.step('Проверка сложности комнаты (easy)'):
        assert 'difficulty' in room_data, "Отсутствует ключ 'difficulty'"
        assert room_data.get('difficulty') == 'easy', 'Неверная сложность комнаты'

    with allure.step('Проверка типов данных основных атрибутов'):
        assert isinstance(room_data.get('code', {}), str), 'Код комнаты должен быть строкой'
        assert isinstance(room_data.get('users', {}), int), 'Количество пользователей должно быть целым числом'
        assert isinstance(room_data.get('freeToUse', {}), bool), 'Флаг freeToUse должен быть булевым значением'

    with allure.step('Проверка статуса публичности комнаты'):
        assert room_data.get('public', {}) is True, 'Комната должна быть публичной'

    with allure.step('Проверка типа IP-адреса (private)'):
        assert room_data.get('ipType', {}) == {}, 'Ожидался ipType: {}'
