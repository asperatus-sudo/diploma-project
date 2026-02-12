import os


from alex_talako.pom_site.page.base_page import WebPage
from alex_talako.pom_site.page.elements import WebElement


class SearchPage(WebPage):
    def __init__(self, web_driver, url=''):
        if not url:
            url = os.getenv('BASE_URL') or 'https://tryhackme.com/'


        super().__init__(web_driver, url)

    btn_cookie = WebElement(xpath='//*[@data-sentry-element="StyledAcceptAllButton"]')
    btn_search = WebElement(xpath='//button[@data-testid="search-btn"]')
    btn_search_input = WebElement(xpath='//*[@data-testid="search-input"]')
    btn_point_of_view = WebElement(xpath='//*[@data-testid="select-type"]')
    btn_view_all = WebElement(xpath='(//*[@aria-disabled="false"])[1]')
    btn_view_purple = WebElement(xpath='(//*[@aria-disabled="false"])[2]')
    btn_view_red = WebElement(xpath='(//*[@aria-disabled="false"])[3]')
    btn_view_blue = WebElement(xpath='(//*[@aria-disabled="false"])[4]')
    btn_sort_by = WebElement(xpath='//*[@data-testid="select-sort-by"]')
    btn_sort_relevance = WebElement(xpath='(//*[@aria-disabled="false"])[1]')
    btn_sort_most_popular = WebElement(xpath='(//*[@aria-disabled="false"])[2]')
    btn_sort_newest = WebElement(xpath='(//*[@aria-disabled="false"])[3]')
    btn_sort_most_users = WebElement(xpath='(//*[@aria-disabled="false"])[4]')
    btn_difficulty = WebElement(xpath='//*[@data-testid="select-difficulty"]')
    btn_difficulty_all = WebElement(xpath='(//*[@aria-disabled="false"])[1]')
    btn_difficulty_info = WebElement(xpath='(//*[@aria-disabled="false"])[2]')
    btn_difficulty_easy = WebElement(xpath='(//*[@aria-disabled="false"])[3]')
    btn_difficulty_medium = WebElement(xpath='(//*[@aria-disabled="false"])[4]')
    btn_difficulty_hard = WebElement(xpath='(//*[@aria-disabled="false"])[5]')
    btn_difficulty_insane = WebElement(xpath='(//*[@aria-disabled="false"])[6]')
    btn_room_type = WebElement(xpath='//*[@data-testid="select-room-type"]')
    btn_room_all = WebElement(xpath='(//*[@aria-disabled="false"])[1]')
    btn_room_challenges = WebElement(xpath='(//*[@aria-disabled="false"])[2]')
    btn_room_walkthroughs = WebElement(xpath='(//*[@aria-disabled="false"])[3]')
    btn_sub_type = WebElement(xpath='//*[@data-testid="select-subscription-type"]')
    btn_sub_all = WebElement(xpath='(//*[@aria-disabled="false"])[1]')
    btn_sub_subscription_only = WebElement(xpath='(//*[@aria-disabled="false"])[2]')
    btn_sub_free_only = WebElement(xpath='(//*[@aria-disabled="false"])[3]')
    btn_sub_cloud_add_on = WebElement(xpath='(//*[@aria-disabled="false"])[4]')
    btn_kali_machine_room = WebElement(xpath='//*[@href="/room/kali"]//h2')