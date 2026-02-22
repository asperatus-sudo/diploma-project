import allure
from alex_talako.pom_site.locators.footer_locators.footer_locators import MainPage

@allure.epic('EPIC 2: Функциональное тестирование TryHackMe')
@allure.feature('Feature 2.2: UI Футер страницы (Footer)')
@allure.story('Story 2.2.1: Проверка навигационных ссылок и социальных иконок')
def test_footer(web_browser):


    driver = MainPage(web_browser)
    with allure.step("Принятие куки"):
        driver.btn_cookie.click()
    with allure.step("Скролл к футеру для обеспечения видимости элементов"):
        driver.btn_about_us.scroll_to_element()


    locators = [
        (driver.btn_hands_on_labs, 'Hands-on labs', "Кнопка 'Hands-on labs'"),
        (driver.btn_for_business, 'For Business', "Кнопка 'For Business'"),
        (driver.btn_for_education, 'For Education', "Кнопка 'For Education'"),
        (driver.btn_competitive_hacking, 'Competitive Hacking', "Кнопка 'Competitive Hacking'"),
        (driver.btn_defensive_certifications, 'Defensive Certifications', "Кнопка 'Defensive Certifications'"),
        (driver.btn_about_us, 'About Us', "Кнопка 'About Us'"),
        (driver.btn_newsroom, 'Newsroom', "Кнопка 'Newsroom'"),
        (driver.btn_blog, 'Blog', "Кнопка 'Blog'"),
        (driver.btn_glossary, 'Glossary', "Кнопка 'Glossary'"),
        (driver.btn_work_at_tryhackme, 'Work at TryHackMe', "Кнопка 'Work at TryHackMe'"),
        (driver.btn_careers_in_cyber, 'Careers in Cyber', "Кнопка 'Careers in Cyber'"),
        (driver.btn_privacy_policy, 'Privacy Policy', "Кнопка 'Privacy Policy'"),
        (driver.btn_terms_of_use, 'Terms of Use', "Кнопка 'Terms of Use'"),
        (driver.btn_ai_terms_of_use, 'AI Terms of Use', "Кнопка 'AI Terms of Use'"),
        (driver.btn_acceptable_use_policy, 'Acceptable Use Policy',"Кнопка 'Acceptable Use Policy'"),
        (driver.btn_cookie_policy,'Cookie Policy',"Кнопка 'Cookie Policy'"),
        (driver.btn_contact_us, 'Contact Us', "Кнопка 'Contact Us'"),
        (driver.btn_affiliates,'Affiliates', "Кнопка 'Affiliates'"),
        (driver.btn_forum, 'Forum', "Кнопка 'Forum'"),
        (driver.btn_students_discount, 'Student Discount',"Кнопка 'Student Discount'"),
        (driver.btn_swag_shop, 'Swag Shop', "Кнопка 'Swag Shop'"),
        (driver.btn_follow_us_on_x, '', "Иконка 'Follow us on X (Twitter)'"),
        (driver.btn_linkedin, '', "Иконка 'LinkedIn'"),
        (driver.btn_discord, '', "Иконка 'Discord'"),
        (driver.btn_follow_us_on_facebook, '', "Иконка 'Facebook'"),
        (driver.btn_follow_us_on_youtube, '', "Иконка 'YouTube'"),
        (driver.btn_follow_us_on_instagram, '', "Иконка 'Instagram'"),
        (driver.btn_follow_us_on_pinterest, '', "Иконка 'Pinterest'"),
    ]

    with allure.step("Проверка всех элементов футера в цикле"):
        for locator, expected_text, step_name in locators:
            with allure.step(f"Проверка: {step_name}"):
                assert locator.wait_until_visible(timeout=5), f'Элемент "{step_name}" не найден'
                web_browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", locator.find())

                if expected_text:
                    actual_text = web_browser.execute_script("return arguments[0].textContent;", locator.find()).strip()
                    assert expected_text in actual_text, \
                        f'Текст не совпал. Ожидался "{expected_text}", пришел "{actual_text}"'

                assert locator.is_clickable(), f'Элемент "{step_name}" заблокирован или перекрыт'