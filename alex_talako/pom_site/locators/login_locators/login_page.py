import os

from alex_talako.pom_site.page.base_page import WebPage
from alex_talako.pom_site.page.elements import WebElement


class LoginPage(WebPage):
    def __init__(self, web_driver, url=''):
        if not url:
            url = os.getenv('BASE_URL') or 'https://tryhackme.com/'


        super().__init__(web_driver, url)

    btn_cookie = WebElement(xpath='//*[@data-sentry-element="StyledAcceptAllButton"]')
    btn_header_log_in = WebElement(xpath='(//*[@data-link="outlined"])[2]')
    btn_username_or_email = WebElement(xpath='//input[@name="usernameOrEmail"]')
    btn_password = WebElement(xpath='//input[@name="password"]')
    btn_captcha = WebElement(xpath='//*[@class="recaptcha-checkbox-border"]')
    btn_log_in_account = WebElement(xpath='//button[text()="Log in"]')
    btn_send_magic_link = WebElement(xpath='//*[@data-sentry-element="StyledRegisterLink" and @href="/login/magic"]')
    btn_sign_up = WebElement(xpath='//*[@data-sentry-element="StyledRegisterLink" and @href="/signup"]')
    btn_close_proposition = WebElement(xpath='//button[@type="button" and @aria-label="Close Modal"]')
    btn_profile = WebElement(xpath='//button[@aria-label="Toggle avatar dropdown"]')
    btn_view_profile = WebElement(xpath='(//*[@type="avatar"])[1]')