import allure
from alex_talako.pom_site.locators.not_found_locators.not_found_page import NotFoundPage


@allure.feature("Обработка ошибок")
@allure.story("Визуальная проверка страницы 404")
def test_not_found_page(web_browser):


    driver = NotFoundPage(web_browser)
    driver.btn_cookie.click()

    with allure.step("Проверка наличия заголовка ошибки"):
        assert driver.error_title.is_visible(), "Заголовок ошибки не найден"


    with allure.step("Проверка текста ошибки"):
        assert driver.error_description.is_visible(), "Описание ошибки отсутствует"

    with allure.step("Проверка кнопки возврата"):
        assert driver.btn_back_to_dashboard.is_visible(), "Кнопка 'Back to Dashboard' отсутствует"
        assert driver.btn_back_to_dashboard.is_clickable(), "Кнопка 'Back to Dashboard' не кликабельна"
        actual_text = driver.btn_back_to_dashboard.get_text().strip()
        expected_text = "Back to Dashboard"
        assert actual_text == expected_text, f'Текст {expected_text} не найден. Получен текст {actual_text}'