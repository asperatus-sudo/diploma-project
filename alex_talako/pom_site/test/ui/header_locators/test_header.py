import allure
from alex_talako.pom_site.locators.header_locators.header_locators import MainPage


@allure.epic('EPIC 2: Функциональное тестирование TryHackMe')
@allure.feature('Feature 2.3: UI Хедер страницы (Header)')
@allure.story('Story 2.3.1: Проверка элементов навигации и кнопок входа')
def test_header(web_browser):


    driver = MainPage(web_browser)
    with allure.step("Принятие куки"):
        driver.btn_cookie.click()

    header_locators = [
        (driver.btn_header_hacktivities, 'Learn'),
        (driver.btn_header_practice, 'Practice'),
        (driver.btn_header_compete, 'Compete'),
        (driver.btn_header_education, 'Education'),
        (driver.btn_header_business, 'Business'),
        (driver.btn_header_pricing, 'Pricing'),
        (driver.btn_header_search, ''),
        (driver.btn_header_log_in, 'Log In'),
        (driver.btn_header_join_for_free, 'Join for FREE'),
    ]

    with allure.step("Проверка всех навигационных элементов хедера в цикле"):
        for locator, expected_text in header_locators:
            element_display_name = expected_text if expected_text else "Элемент без текста (поиск)"
            with allure.step(f"Проверка: '{element_display_name}'"):
                assert locator.wait_until_visible(timeout=10), f'Элемент "{element_display_name}" не прогрузился'

                if expected_text:
                    actual_text = web_browser.execute_script("return arguments[0].textContent;", locator.find()).strip()
                    assert expected_text in actual_text, \
                        f'Текст не совпал. Ожидался "{expected_text}", пришел "{actual_text}"'

                assert locator.is_clickable(), f'Элемент "{element_display_name}" заблокирован'


