import allure
import pytest_check as check

from alex_talako.pom_site.locators.body_locators.body_locators import MainPage

@allure.description("""Этот тест проверяет остальные локаторы на странице, кроме хэдера и футера""")
@allure.feature("Основное содержимое страницы")
@allure.story("Видимость и кликабельность блоков и статических элементов")
def test_body(web_browser):


    driver = MainPage(web_browser)
    with allure.step("Принятие куки"):
        driver.btn_cookie.click()

    @allure.step("Вспомогательная функция для проверки группы локаторов")
    def check_locators_group(locators_list):

        for locator, expected_text in locators_list:
            element_display_name = expected_text.replace('\n', ' ') if expected_text else "Элемент без текста"
            with allure.step(f"Проверка элемента: '{element_display_name}'"):

                check.is_true(locator.is_visible(), f'Элемент "{expected_text}" отсутствует на экране')

                actual_text = locator.get_text().strip()
                if expected_text:
                    check.equal(actual_text, expected_text,f'Неверный текст. Ожидаемый текст "{expected_text}". Актуальный текст "{actual_text}"')

                check.is_true(locator.is_clickable(), f'Элемент "{expected_text}" не кликабелен')


    locators_initial = [
        (driver.btn_email, ''),
        (driver.btn_join_near_email, 'Join for FREE'),
        (driver.btn_web_application_red_teaming, 'Web Application Red Teaming\nEnroll in Path'),
        (driver.btn_container_cyber_security, 'Cyber Security 101\nEnroll in Path'),
        (driver.btn_soc_level_one, 'SOC Level 1\nEnroll in Path'),
        (driver.btn_dot_first, ''), (driver.btn_dot_second, ''),
        (driver.btn_dot_third, ''), (driver.btn_dot_fourth, ''),
        (driver.btn_dot_fifth, ''),
        (driver.btn_exercises_in_lesson, 'Exercises in every lesson'),
        (driver.btn_beginner_friendly, 'Beginner-friendly'),
        (driver.btn_start_hacking_instantly, 'Start hacking instantly'),
        (driver.btn_real_world_networks, 'Real-world networks'),
        (driver.btn_dot_bottom_first, ''),
        (driver.btn_dot_bottom_second, ''),
        (driver.btn_dot_bottom_third, ''),
        (driver.btn_cyber_train_for_team, 'Learn More'),
        (driver.btn_cyber_tarin_for_students, 'Learn More'),
        (driver.btn_bottom_join_for_free, 'Join for FREE'),
    ]
    with allure.step("Проверка статических элементов и первого блока"):
        check_locators_group(locators_initial)

    with allure.step("Переключение на второй блок"):
        driver.btn_dot_second.click()
        driver.wait_for_slide_update()

        locators_after_click_dot_1 = [
            (driver.btn_pre_security, 'Pre Security\nEnroll in Path'),
            (driver.btn_jr_penetration_tester, 'Jr Penetration Tester\nEnroll in Path'),
            (driver.btn_red_teaming, 'Red Teaming\nEnroll in Path'),
        ]
        check_locators_group(locators_after_click_dot_1)


    with allure.step("Переключение на третий блок"):
        driver.btn_dot_third.click()
        driver.wait_for_slide_update()

        locators_after_click_dot_2 = [
            (driver.btn_soc_level_two, 'SOC Level 2\nEnroll in Path'),
            (driver.btn_security_engineer, 'Security Engineer\nEnroll in Path'),
            (driver.btn_dev_sec_ops, 'DevSecOps\nEnroll in Path'),
        ]
        check_locators_group(locators_after_click_dot_2)


    with allure.step("Переключение на четвертый блок"):
        driver.btn_dot_fourth.click()
        driver.wait_for_slide_update()

        locators_after_click_dot_3 = [
            (driver.btn_defending_azure, 'Defending Azure\nEnroll in Path'),
            (driver.btn_advanced_endpoint, 'Advanced Endpoint Investigations\nEnroll in Path'),
            (driver.btn_att_def_aws, 'Attacking and Defending AWS\nEnroll in Path'),
        ]
        check_locators_group(locators_after_click_dot_3)


    with allure.step("Переключение на пятый блок"):
        driver.btn_dot_fifth.click()
        driver.wait_for_slide_update()

        locators_after_click_dot_4 = [
            (driver.btn_offensive_pentest, 'Offensive Pentesting\nEnroll in Path'),
            (driver.btn_web_fundamentals, 'Web Fundamentals\nEnroll in Path'),
            (driver.btn_web_application, 'Web Application Pentesting\nEnroll in Path'),
        ]
        check_locators_group(locators_after_click_dot_4)


    with allure.step("Переключение на шестой блок и финальная проверка элемента CompTIA"):
        driver.btn_dot_sixth.click()
        driver.wait_for_slide_update()

        actual_text_comp_tia = driver.btn_comp_tia.get_text().strip()
        expected_text_comp_tia = 'CompTIA Pentest+\nEnroll in Path'

        check.equal(actual_text_comp_tia, expected_text_comp_tia, 'Элемент содержит неверный текст')
        check.is_true(driver.btn_comp_tia.is_visible(), f'Элемент "{expected_text_comp_tia}" отсутствует на экране')
        check.is_true(driver.btn_comp_tia.is_clickable(), f'Элемент "{expected_text_comp_tia}" не кликабелен')

