import time
import allure
import pytest_check as check

from alex_talako.pom_site.locators.body_locators.body_locators import MainPage

@allure.epic('EPIC 2: Функциональное тестирование TryHackMe')
@allure.feature('Feature 2.1: UI Основное содержимое (Body)')
@allure.story('Story 2.1.1: Проверка контента и блоков обучающих путей')
def test_body(web_browser):


    driver = MainPage(web_browser)
    with allure.step('Принятие куки и проверка поля Email'):
        driver.btn_cookie.click()
        check.is_true(driver.btn_email.is_visible(), 'Поле ввода Email не отображается')
    with allure.step('Проверка статических кнопок'):
        static_elements = [
            (driver.btn_join_near_email, 'Join for FREE'),
            (driver.btn_exercises_in_lesson, 'Exercises in every lesson'),
            (driver.btn_beginner_friendly, 'Beginner-friendly'),
            (driver.btn_start_hacking_instantly, 'Start hacking instantly'),
            (driver.btn_real_world_networks, 'Real-world networks'),
            (driver.btn_cyber_train_for_team, 'Learn More'),
            (driver.btn_cyber_tarin_for_students, 'Learn More'),
            (driver.btn_bottom_join_for_free, 'Join for FREE')
        ]

        for element, expected_text in static_elements:
                with allure.step(f"Проверка: {expected_text}"):
                    web_browser.execute_script("arguments.scrollIntoView({block: 'center'});", element.find(timeout=20))
                    time.sleep(1)
                    target = element.find(timeout=10)
                    assert target is not None, f"Элемент '{expected_text}' не найден в DOM"
                    web_browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", target)
                    assert element.wait_until_visible(timeout=5), f"Элемент '{expected_text}' не виден"
                    actual_text = web_browser.execute_script("return arguments[0].textContent;", target).strip()
                    check.is_true(expected_text in actual_text, f"Текст не совпал: {actual_text}")

        with allure.step('Проверка навигационных точек (Dots)'):
            dots = [
                driver.btn_dot_first, driver.btn_dot_second, driver.btn_dot_third,
                driver.btn_dot_fourth, driver.btn_dot_fifth, driver.btn_dot_sixth,
                driver.btn_dot_bottom_first, driver.btn_dot_bottom_second, driver.btn_dot_bottom_third
            ]
            for dot in dots:
                check.is_true(dot.is_visible(), 'Точка навигации не видна')
                check.is_true(dot.is_clickable(), 'Точка навигации не кликабельна')

        with allure.step('Динамическая проверка 16 обучающих путей'):
            expected_paths = [
                'Cyber Security 101', 'Web Application Red Teaming', 'SOC Level 1',
                'Pre Security', 'Jr Penetration Tester', 'Red Teaming',
                'SOC Level 2', 'Security Engineer', 'DevSecOps',
                'Defending Azure', 'Advanced Endpoint Investigations', 'Attacking and Defending AWS',
                'Offensive Pentesting', 'Web Fundamentals', 'Web Application Pentesting', 'CompTIA Pentest+'
            ]

            assert driver.all_path_cards.wait_until_visible(timeout=15), "Карточки путей не прогрузились"
            all_cards = driver.all_path_cards.find()
            if all_cards:
                web_browser.execute_script("arguments[0].scrollIntoView();", all_cards[0])
                driver.all_path_cards.wait_until_visible(timeout=5)
                actual_texts = [web_browser.execute_script("return arguments[0].textContent;", el) for el in all_cards]
                clean_texts = [t.replace('\n', ' ').strip() for t in actual_texts]

                for path in expected_paths:
                    found = any(path in text for text in clean_texts)
                    check.is_true(found, f"Путь '{path}' не найден")