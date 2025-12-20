import allure
from selenium.webdriver.common.keys import Keys
from alex_talako.pom_site.locators.search_and_filter_locators.search_and_filter_page import SearchPage

@allure.epic('EPIC 2: Функциональное тестирование TryHackMe')
@allure.feature('Feature 2.6: UI Поиск и фильтрация контента')
@allure.story('Story 2.6.1: Поиск по ключевому слову и применение комплексных фильтров')
def test_search_kali_flow(web_browser):


    driver = SearchPage(web_browser)
    with allure.step("Принятие куки"):
        driver.btn_cookie.click()

    with allure.step("Выбор поиска на главной странице"):
        driver.btn_search.click()

    with allure.step("Ввод поискового запроса 'kali'"):
        driver.btn_search_input.send_keys("kali")
        driver.btn_search_input.send_keys(Keys.ENTER)
        driver.scroll_by_pixels(500)
    with allure.step("Определение фильтров"):
        with allure.step("Установка фильтра Point of view: All"):
            driver.btn_point_of_view.click()
            driver.btn_view_all.click()

    with allure.step("Установка фильтра сортировки по популярности: Relevance"):
        driver.btn_sort_by.click()
        driver.btn_sort_relevance.click()

    with allure.step("Установка фильтра сложности: Easy"):
        driver.btn_difficulty.click()
        driver.btn_difficulty_easy.click()

    with allure.step("Установка фильтра типа комнаты: Walkthroughs "):
        driver.btn_room_type.click()
        driver.btn_room_walkthroughs.click()

    with allure.step("Установка фильтра типа подписки: All"):
        driver.btn_sub_type.click()
        driver.btn_sub_all.click()

    with allure.step("Валидация результата: поиск комнаты Kali Machine"):
        assert driver.btn_kali_machine_room.is_visible(), "Комната Kali Machine отсутствует из-за некорректно установленных фильтров"

    with allure.step("Проверка кликабельности комнаты"):
        assert driver.btn_kali_machine_room.is_clickable(), "Комната Kali Machine не кликабельна"

    with allure.step("Проверка названия комнаты"):
        actual_text = driver.btn_kali_machine_room.get_text().strip()
        expected_text = "Kali Machine"
        assert actual_text == expected_text, f'Текст {expected_text} не найден. Получен текст {actual_text}'



