import os

from alex_talako.pom_site.page.base_page import WebPage
from alex_talako.pom_site.page.elements import WebElement, ManyWebElements



class MainPage(WebPage):
    def __init__(self, web_driver, url=''):
        if not url:
            url = os.getenv('BASE_URL') or 'https://tryhackme.com/'


        super().__init__(web_driver, url)

    def wait_for_slide_update(self):
        """ Универсальное ожидание обновления контента слайдера после клика. """

        self.wait_page_loaded(timeout=5)


    btn_cookie = WebElement(xpath = '//*[@data-sentry-element="StyledAcceptAllButton"]')
    btn_email = WebElement(xpath = '//*[@aria-label="Email address"]')
    btn_join_near_email = WebElement(xpath = '//*[@data-testid="sc-banner"]//button')
    btn_dot_first = WebElement(xpath = '//*[@data-testid="dot-0" and @color="default"]')
    btn_dot_second = WebElement(xpath = '//*[@data-testid="dot-1" and @color="default"]')
    btn_dot_third = WebElement(xpath = '//*[@data-testid="dot-2" and @color="default"]')
    btn_dot_fourth = WebElement(xpath = '//*[@data-testid="dot-3" and @color="default"]')
    btn_dot_fifth = WebElement(xpath = '//*[@data-testid="dot-4" and @color="default"]')
    btn_dot_sixth = WebElement(xpath = '//*[@data-testid="dot-5" and @color="default"]')
    btn_exercises_in_lesson = WebElement(xpath = '//*[@aria-label="View media Exercises in every lesson"]')
    btn_beginner_friendly = WebElement(xpath = '//span[@aria-label="View media Beginner-friendly"]')
    btn_start_hacking_instantly = WebElement(xpath = '//*[@aria-label="View media Start hacking instantly"]')
    btn_real_world_networks = WebElement(xpath = '//*[@aria-label="View media Real-world networks"]')
    btn_dot_bottom_first = WebElement(xpath = '//*[@data-testid="dot-0" and @color="secondary"]')
    btn_dot_bottom_second = WebElement(xpath = '//*[@data-testid="dot-1" and @color="secondary"]')
    btn_dot_bottom_third = WebElement(xpath = '//*[@data-testid="dot-2" and @color="secondary"]')
    btn_cyber_train_for_team = WebElement(xpath = '(//*[@role="button"])[2]')
    btn_cyber_tarin_for_students = WebElement(xpath = '(//*[@role="button"])[3]')
    btn_bottom_join_for_free = WebElement(xpath='//*[@type="button" and @data-sentry-element="StyledButton"]')
    all_path_cards = ManyWebElements(xpath='//div[starts-with(@data-testid, "path-card-container-")]')

