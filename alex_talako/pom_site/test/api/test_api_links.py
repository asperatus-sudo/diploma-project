import pytest
import requests
import allure
from requests.exceptions import RequestException, Timeout

@allure.epic('EPIC 1: Функциональное тестирование TryHackMe')
@allure.feature('Feature 1.3: Навигация и пользовательский интерфейс')
@allure.story('Story 1.3.1: Проверка наличия всех ключевых элементов на главной странице')
@pytest.mark.parametrize("expected_status_code, link_url, label", [
    (200,"https://tryhackme.com/",""),
    (200,"https://tryhackme.com/hacktivities","Learn"),
    (200,"https://tryhackme.com/signup","Join for FREE"),
    (200,"https://tryhackme.com/path/outline/cybersecurity101","Cyber Security 101En"),
    (200,"https://tryhackme.com/path/outline/presecurity","Pre SecurityEnroll i"),
    (200,"https://tryhackme.com/pricing","Pricing"),
    (200,"https://tryhackme.com/path/outline/web","Web FundamentalsEnro"),
    (200,"https://tryhackme.com/path/outline/jrpenetrationtester","Jr Penetration Teste"),
    (200,"https://tryhackme.com/classrooms","Education"),
    (200,"https://tryhackme.com/path/outline/soclevel1","SOC Level 1Enroll in"),
    (200,"https://tryhackme.com/path/outline/webappredteaming","Web Application Red "),
    (200,"https://tryhackme.com/hacktivities","Learn"),
    (200,"https://tryhackme.com/",""),
    (200,"https://tryhackme.com/pricing","Pricing"),
    (200,"https://tryhackme.com/classrooms","Education"),
    (200,"https://tryhackme.com/path/outline/redteaming","Red TeamingEnroll in"),
    (200,"https://tryhackme.com/path/outline/soclevel2","SOC Level 2Enroll in"),
    (200,"https://tryhackme.com/path/outline/attackinganddefendingaws","Attacking and Defend"),
    (200,"https://tryhackme.com/path/outline/security-engineer-training","Security EngineerEnr"),
    (200,"https://tryhackme.com/path/outline/azuresecurity","Defending AzureEnrol"),
    (200,"https://tryhackme.com/path/outline/advancedendpointinvestigations","Advanced Endpoint In"),
    (200,"https://tryhackme.com/path/outline/webapppentesting","Web Application Pent"),
    (200,"https://tryhackme.com/classrooms","Learn More"),
    (200,"https://tryhackme.com/path/outline/pentesting","Offensive Pentesting"),
    (200,"https://tryhackme.com/business","For Business"),
    (200,"https://tryhackme.com/path/outline/3iwpu63u9r","Web Application Pent"),
    (200,"https://tryhackme.com/certification/security-analyst-level-1","Defensive Certificat"),
    (200,"https://tryhackme.com/path/outline/pentestplus","CompTIA Pentest+Enro"),
    (200,"https://tryhackme.com/path/outline/devsecops","DevSecOpsEnroll in P"),
    (200,"https://tryhackme.com/games/koth","Competitive Hacking"),
    (200,"https://tryhackme.com/hacktivities","Hands-on labs"),
    (200,"https://tryhackme.com/classrooms","For Education"),
    (200,"https://tryhackme.com/about","About Us"),
    (200,"https://tryhackme.com/glossary","Glossary"),
    (200,"https://tryhackme.com/legal/ai-terms-of-use","AI Terms of Use"),
    (200,"https://tryhackme.com/resources/newsroom","Newsroom"),
    (200,"https://tryhackme.com/resources/blog","Blog"),
    (200,"https://tryhackme.com/legal/privacy-policy","Privacy Policy"),
    (200,"https://tryhackme.com/legal/acceptable-use-policy","Acceptable Use Polic"),
    (200,"https://tryhackme.com/careers","Careers in Cyber"),
    (200,"https://tryhackme.com/legal/terms-of-use","Terms of Use"),
    (200,"https://tryhackme.com/contact","Contact Us"),
    (200,"https://tryhackme.com/affiliates","Affiliates"),
    (200,"https://tryhackme.com/legal/cookie-policy","Cookie Policy"),
    (200,"https://careers.tryhackme.com/","Work at TryHackMe"),
    (200,"https://store.tryhackme.com/","Swag Shop"),
    (200,"https://discord.com/invite/tryhackme",""),
    (400,"https://www.facebook.com/people/Tryhackme/100069557747714/",""),
    (200,"https://www.youtube.com/channel/UCRnWD3BsY5Co2MMETB7lHQw",""),
    (200,"https://www.linkedin.com/company/tryhackme/","999"),
    (200,"https://business.tryhackme.com/","Learn More"),
    (200,"https://www.studentbeans.com/en-gb/uk/beansid-connect/hosted/tryhackme","Student Discount"),
    pytest.param(200,"https://tryhackme.com/forum","Forum", marks=pytest.mark.xfail(reason= "Битый редирект на /not-found")),
    (200,"https://twitter.com/tryhackme",""),
    (200,"https://instagram.com/realtryhackme",""),
    (200,"https://www.pinterest.co.uk/RealTryHackMe/",""),

])

def test_links_api_get(expected_status_code, link_url, label):
    with allure.step(f'Подготовка запроса к ссылке: {link_url}'):
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        }

        session = requests.Session()

    with allure.step(f'Вызов метода GET: {link_url}'):
        try:
            response = session.get(link_url, headers=headers, timeout=10)
        except Timeout:
            pytest.fail(f"Превышено время ожидания при доступе к {link_url}")
        except RequestException as e:
            pytest.fail(f"Произошла ошибка запроса при доступе к {link_url}: {e}")

    with allure.step(f'Проверка конечного статус кода для: {link_url}'):
        assert response.status_code == expected_status_code, \
            f'Конечный статус код не равен {expected_status_code} для URL {link_url}. ' \
            f'Получен {response.status_code}. Конечный URL: {response.url}'

    if "tryhackme.com" in link_url:
        with allure.step('Проверка, что внутренняя ссылка не ведет на страницу ошибки'):
            assert "/not-found" not in response.url, \
                f"Внутренняя ссылка {link_url} перенаправила на страницу ошибки {response.url}"

