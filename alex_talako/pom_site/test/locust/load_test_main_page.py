from locust import HttpUser, task, between, events

class TryHackMeUser(HttpUser):
    # Время ожидания между запросами
    wait_time = between(1, 3)  # Пользователи ждут от 1 до 3 секунд между задачами

    host = "https://tryhackme.com"

    @task(3)
    def load_main_page(self):
        self.client.get("/")

    @task(1)
    def load_login_page(self):
        self.client.get("/login")

# Обработчик события для вывода результатов в консоль для отладки
@events.request.add_listener
def my_request_handler(request_type, name, response_time, response_length, response,
                       context, exception, start_time, url, **kwargs):
    if exception:
        print(f"Request to {name} failed with exception: {exception}")
    else:
        print(f"Request to {name} successful: {response_time}ms")

# locust -f alex_talako/pom_site/test/locust/load_test_main_page.py --headless -u 10 -r 1 --run-time 1m --html=locust_results/report.html для запуска теста