import allure
from selenium.webdriver.common.keys import Keys
from alex_talako.pom_site.locators.search_and_filter_locators.search_and_filter_page import SearchPage

@allure.epic('EPIC 2: Функциональное тестирование TryHackMe')
@allure.feature('Feature 2.6: UI Поиск и фильтрация контента')
@allure.story('Story 2.6.1: Поиск по ключевому слову и применение комплексных фильтров')
def test_search_kali_flow(web_browser):


    driver = SearchPage(web_browser)
    with allure.step('Принятие куки'):
        driver.btn_cookie.click()

    with allure.step("Ввод поискового запроса 'kali'"):
        driver.btn_search.click()
        driver.btn_search_input.send_keys('kali')
        driver.btn_search_input.send_keys(Keys.ENTER)
        driver.scroll_by_pixels(500)

    with allure.step('Определение и установка фильтров'):
        filter_steps = [
            (driver.btn_point_of_view, driver.btn_view_all, "POV: All"),
            (driver.btn_sort_by, driver.btn_sort_relevance, "Sort: Relevance"),
            (driver.btn_difficulty, driver.btn_difficulty_easy, "Diff: Easy"),
            (driver.btn_room_type, driver.btn_room_walkthroughs, "Type: Walkthroughs"),
            (driver.btn_sub_type, driver.btn_sub_all, "Sub: All")
        ]

        for opener, selector, name in filter_steps:
            with allure.step(f"Установка фильтра {name}"):
                assert opener.wait_until_visible, f'Фильтр {name} не виден'
                assert opener.is_clickable(), f'Фильтр {name} не кликабелен'
                opener.click()

                assert selector.wait_until_visible, f'Опция для {name} не появилась'
                selector.click()

    with allure.step('Валидация результата: поиск комнаты Kali Machine'):
        target_card = driver.btn_kali_machine_room.find(timeout=15)
        web_browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_card)
        assert driver.btn_kali_machine_room.wait_until_visible(timeout=10), \
            "Комната Kali Machine не появилась после фильтрации."

    with allure.step('Проверка названия комнаты'):
        actual_text = web_browser.execute_script("return arguments[0].textContent;", target_card).strip()
        expected_text = 'Kali Machine'
        assert expected_text in actual_text, f'Ожидался "{expected_text}", но в теге: "{actual_text}"'

    with allure.step('Проверка кликабельности комнаты'):
        assert driver.btn_kali_machine_room.is_clickable(), 'Комната Kali Machine не кликабельна'

        driver.btn_kali_machine_room.click()





