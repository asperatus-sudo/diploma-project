import os


from alex_talako.pom_site.page.base_page import WebPage
from alex_talako.pom_site.page.elements import WebElement


class NotFoundPage(WebPage):
    def __init__(self, web_driver, url=''):
        if not url:
            url = (os.getenv('BASE_URL') or 'https://tryhackme.com/') + '/page_not_found_test'


        super().__init__(web_driver, url)

    btn_cookie = WebElement(xpath='//*[@data-sentry-element="StyledAcceptAllButton"]')
    error_title = WebElement(xpath="//*[@data-sentry-element='ErrorTitle']")
    error_description = WebElement(xpath="//*[@data-sentry-element='ErrorDescription']")
    btn_back_to_dashboard = WebElement(xpath="//*[@data-sentry-element='CtaWrapper']")



