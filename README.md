Diploma Project: THM Testing Framework & SENTINEL Orchestrator
Стек технологий:

Language: Python 3.12+ (AsyncIO, Requests).
UI Framework: Selenium WebDriver + Page Object Model (POM).
Infrastructure: GitHub Actions + Ubuntu-latest + Xvfb (Virtual Display).
Reporting: Allure Report + Telegram API Integration. 

Реализованный функционал:

Hybrid Testing: Автоматизация API (REST) и UI-сценариев в одном пайплайне.
Environment Security: Управление конфиденциальными данными (Cookies, Tokens) через GitHub Secrets и os.getenv.
Headless Rendering: Стабильное выполнение UI-тестов в Docker/CI контейнерах с использованием Xvfb для отрисовки динамического React-контента. 
Async Orchestration (SENTINEL): Асинхронный бот-менеджер для мониторинга запусков и мгновенной доставки логов/отчетов. 🤖
Handling Dynamic Content: Реализованы алгоритмы адаптивных ожиданий и JS-скроллов для тестирования Lazy Loading элементов.
