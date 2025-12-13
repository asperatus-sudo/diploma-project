import allure
from alex_talako.pom_site.locators.header_locators.header_locators import MainPage


@allure.description("""Этот тест проверяет элементы хэдера на странице""")
@allure.feature("Основное содержимое страницы") # Перевод метаданных Allure
@allure.story("Видимость, текст и кликабельность элементов навигации")
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
            with allure.step(f"Проверка элемента: '{element_display_name}'"):
                assert locator.is_visible(), f'Элемент "{expected_text}" отсутствует на экране'
                actual_text = locator.get_text().strip()
                if expected_text:
                    assert actual_text == expected_text, f'Неверный текст. Ожидаемый текст "{expected_text}". Актуальный текст "{actual_text}"'
                assert locator.is_clickable(), f'Элемент "{expected_text}" не кликабелен'


