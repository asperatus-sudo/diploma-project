import pytest
import requests
import allure
import copy

BASE_URL = "https://tryhackme.com"

# Не забывать про куки
AUTH_HEADERS = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'Cookie': '_csrf=Crp4lO3dAc3fxi9Py_pcnaAF; _hjSessionUser_1950941=eyJpZCI6IjUzYmEzOWEwLTFkZjEtNWY5MS1hMzQ3LWQ3MDk4ZDY1MDExNyIsImNyZWF0ZWQiOjE3NjM5ODQ4OTc3MjQsImV4aXN0aW5nIjp0cnVlfQ==; ajs_anonymous_id=d5b8b804-9cc3-49b2-9111-191fe521cbdc; _ga=GA1.1.893520014.1763984899; ajs_user_id=687e46b8ad61437da3d8465f; hubspotutk=aeb59721d6eb4bfc527d839d0ca11943; __hssrc=1; intercom-device-id-pgpbhph6=8e7254ee-b540-4c9e-9c1c-f595ac910c67; cookieconsent_status=dismiss; _cioid=687e46b8ad61437da3d8465f; thm-aid=d5b8b804-9cc3-49b2-9111-191fe521cbdc; thm-amplitude-device-id=d5b8b804-9cc3-49b2-9111-191fe521cbdc; thm-amplitude-session-id=1763549969612; analytics_session_id=1763549969612; gbStickyBuckets__anonymousId||d5b8b804-9cc3-49b2-9111-191fe521cbdc={%22attributeName%22:%22anonymousId%22%2C%22attributeValue%22:%22d5b8b804-9cc3-49b2-9111-191fe521cbdc%22%2C%22assignments%22:{%22is-french-language__1%22:%220%22%2C%22new-homepage__0%22:%220%22%2C%22google-one-tap-auto-login__1%22:%220%22%2C%22linkedin-social-login__0%22:%220%22}}; g_state={"i_l":0,"i_ll":1765353915507,"i_b":"Db1t52i/HV9DwWIF0Iz65sFFxq68aAVFddTM9GAL84Q","i_t":1765055831920,"i_e":{"enable_itp_optimization":0}}; _hjSession_1950941=eyJpZCI6IjhhZTAyMjcwLWM2YzMtNGVkNS05ZDU2LTJiNzA0ZDcxYWNmNiIsImMiOjE3NjUzNzMxMjMwNzAsInMiOjEsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; _gcl_au=1.1.1014173419.1763984898.1876617802.1765373125.1765373137; logged-in-hint=687e46b8ad61437da3d8465f; connect.sid=s%3Ao0UK1UlkYuBppFQrYryuV22_Qo4bEuu_.SBvC6JY7a%2F4l0TJU7QUVCTvQswEdwE1sIL81uQZvJis; thm-ud=%7B%22id%22%3A%22687e46b8ad61437da3d8465f%22%2C%22experience%22%3A%22unset%22%2C%22isStudent%22%3Atrue%2C%22dateSignUp%22%3A%222025-07-21T13%3A55%3A04.339Z%22%2C%22email%22%3A%22talako00%40mail.ru%22%2C%22username%22%3A%22Asperatus.%22%2C%22country%22%3A%22by%22%2C%22howHeard%22%3A%22social_media%22%2C%22isPremium%22%3Afalse%7D; _hjHasCachedUserAttributes=true; gbStickyBuckets__id||687e46b8ad61437da3d8465f={%22attributeName%22:%22id%22%2C%22attributeValue%22:%22687e46b8ad61437da3d8465f%22%2C%22assignments%22:{%22signup-flash-sale__6%22:%220%22%2C%22improvement-offensive-security-intro__0%22:%220%22}}; analytics_session_id=1763549969612; __hstc=256179476.aeb59721d6eb4bfc527d839d0ca11943.1763984900371.1765353918330.1765373154778.63; _rdt_uuid=1763984898372.16495a5b-cbce-4f18-a720-15c098241782; _rdt_em=:e9aff251222f82b670e8d33ac5b56e59dbaa79bab3ee91d10af3f3b55a61ba6b,79bc4535cfc3a6ec920889d06b5550d13ed245aba131ccf9ccd522778340d136,606cd48ecb28f3488cf8bfbae33b2799303c1cb39529f0a762818aa8fabd3799,2f73d9e5538ad62759b57079dae50179e7c60eba0c496e016281bc6bf1c43d66,97e00b4fac5d76caf3ab96da689240cd6666bb297492296b7b2c7736961e3af8; analytics_session_id.last_access=1765373541980; __hssc=256179476.3.1765373154778; intercom-session-pgpbhph6=SDkrZEttbkM0STd4RS8rWVZhb1JyV2tMUWFEYzhBQW1UUHdZZExGVkJyTGJ0SVBiaCtPaTh1RWZsVy9tY1FmZXlqRHlOK0tDdE9vdC9uclgrQ3Z3RFNIdnhQaWppc3ltZm1zbmJSaDZVakU9LS1ZL0pyek12eW9KTHFpZ2w2N0Vxcnh3PT0=--6b6a1d90e049e9a6006c97f6cb9e7d63b3b9ac49; _ga_Z8D4WL3D4P=GS2.1.s1765373123$o76$g1$t1765373555$j22$l0$h0'
}


@allure.epic('Тестирование API TryHackMe')
@allure.feature('Профиль пользователя')
@allure.story('Доступ к деталям профиля аутентифицированного пользователя (статус 200)')
def test_auth_details():
    api_url = f'{BASE_URL}/api/v2/users/self'

    session = requests.Session()
    session.headers.update(copy.deepcopy(AUTH_HEADERS))

    with allure.step(f'Отправка GET запроса к {api_url}'):
        response = session.get(api_url)

    with allure.step('Проверка статус-кода HTTP 200 OK'):
        if response.status_code in [401, 403]:
            pytest.fail(
                f'Куки авторизации просрочены или невалидны. Их следует обновить. Получен статус {response.status_code}.')

        assert response.status_code == 200, \
            f'Ожидался статус-код 200, получен {response.status_code}.'

    with allure.step('Проверка наличия данных в теле ответа'):
        assert response.text, "Тело ответа не должно быть пустым для статуса 200"
        data = response.json()
        user_data = data.get('data').get('user')
        local_data = data.get('data').get('user').get('local')
        assert user_data.get('username') == 'Asperatus.', f"Неверный username, получен '{user_data.get('username')}'"
        assert user_data.get('email') == 'talako00@mail.ru', f"Неверный email, получен '{user_data.get('email')}'"
        assert isinstance(user_data.get('isPremium'), bool), 'isPremium должен быть булевым значением'
        assert local_data.get('country') == 'by', f"Неверная страна. Ожидалась 'by', получена '{local_data.get('country')}'"