from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from pathlib import Path
from dotenv import load_dotenv
import zipfile
import time
import asyncio
import os
import json



load_dotenv()

async def execute_command(cmd: str, update: Update, timeout: int = 300) -> str:
    """Выполняет shell-команду с таймаутом и возвращает результат"""
    try:
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout)
        output = f"STDOUT:\n{stdout.decode().strip()}" if stdout else ""
        output += f"\nSTDERR:\n{stderr.decode().strip()}" if stderr else ""
        return output.strip()
    except asyncio.TimeoutError:
        return f"❌ Таймаут ({timeout} сек)"
    except Exception as e:
        return f"⚠️ Ошибка: {str(e)}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Хей, я бот дипломного проекта для начинающего тестировщика!\n\nВот, что я могу тебе предложить:\n\n'
                                    '1)  Напиши /about , чтобы узнать обо мне и создателе.\n\n'
                                    '2)  Напиши /api , чтобы начать api тесты, которые помогают выявить ошибки и оценить общую работоспособность системы.\n\n'
                                    '3)  Напиши /ui , чтобы начать ui тесты, которые проверяют пользовательский интерфейс ПО, оценивает его визуальные элементы, функциональность, удобство использования и т.д.\n\n'
                                    '4)  Напиши /all_test, чтобы начать запуск всех api и ui тестов.\n\n'
                                    '5)  Напиши /allure_report, чтобы создать allure отчёт и сделать отправку архива.\n\n'
                                    '6)  Напиши /full_report, чтобы запустить все тесты и сгенерировать по ним отчёт.\n\n'
                                    )



async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    about_text = ('Здравствуй, дорогой пользователь!\n\nЯ создал бота для того, чтоб реализовать авто тесты с помощью функционала бота.\n\n'
                  'Бот умеет запускать авто тесты с упором на api и ui тесты, а также сгенерировать allure отчёт по совершённым тестам.\n\n'
                  'Меня зовут Талако Александр Тимофеевич!\n'
                  'Я начинающий тестировщик без опыта работы, но имеющий большое рвение и скрытый потенциал им стать.\n\n'
                  'Владею следующим:\n'
                  'TestRail, TestLink, Jmeter, Jira, JSON, XML, HTML, DevTools, SQL-запросы, Postman, Python, Pycharm, Git, Allure\n'
                  'Этот список будет дополняться :)\n\n'
                  'Также хочу отметить, что нравится мне область информационной безопасности и стать специалистом в этой области — это то, к чему я стремлюсь.\n\n'
                  'Бота зовут — @emnotem_bot\nМой телеграм аккаунт — @asperatus99')
    await update.message.reply_text(about_text)


async def api(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запуск тестов и сохранение результатов"""
    await update.message.reply_text("🔍 Запускаю тесты...")

    # 1. Находим корень и папку результатов в корне проекта
    root_dir = Path(__file__).parent.parent
    results_dir = root_dir / "allure-results"
    results_dir.mkdir(exist_ok=True)

    # 2. Очистка (чтобы в отчете по /api были ТОЛЬКО свежие API-результаты)
    for file in results_dir.glob("*"):
        try:
            if file.is_file():
                file.unlink()
        except Exception as e:
            print(f"Ошибка удаления файла {file}: {e}")

    # 3. Путь к самим тестам
    test_path = root_dir / "alex_talako" / "pom_site" / "test" / "api"

    # 4. Команда запуска (используем кавычки для Windows)
    command = f'pytest -s -v "{test_path}" --alluredir="{results_dir}"'

    # Выполняем команду
    result = await execute_command(command, update)

    # 5. Сводка
    short_result = "\n".join([line for line in result.split("\n") if "FAILED" in line or "ERROR" in line])
    await update.message.reply_text(
        f"📊 Результаты API тестов:\n{short_result[:3000]}" if short_result else "✅ API тесты прошли успешно!"
    )


async def ui(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запуск UI-тестов с гарантированной чистотой отчета и скриншотами"""
    await update.message.reply_text("🔍 Запускаю UI-тесты...")

    # 1. Находим корень проекта дважды двигаемся вверх
    root_dir = Path(__file__).parent.parent
    results_dir = root_dir / "allure-results"  # Папка в КОРНЕ проекта
    results_dir.mkdir(exist_ok=True)

    # 2. Очистка (чтобы в отчете по /ui были ТОЛЬКО свежие UI-результаты)
    for file in results_dir.glob("*"):
        try:
            if file.is_file():
                file.unlink()
        except Exception as e:
            print(f"Ошибка удаления файла {file}: {e}")

    # 3. Путь к самим тестам (теперь правильно: через alex_talako)
    test_path = root_dir / "alex_talako" / "pom_site" / "test" / "ui"

    # 4. Команда запуска (используем кавычки для Windows)
    # Используем --alluredir="${results_dir}" для указания пути к allure
    command = f'pytest -s -v "{test_path}" --alluredir="{results_dir}"'

    # Выполняем команду
    result = await execute_command(command, update)

    # 5. Отправляем скриншоты ошибок (если есть)
    await send_error_screenshots(update, context)

    # 6. Сводка (твоя логика)
    short_result = "\n".join([line for line in result.split("\n") if "FAILED" in line or "ERROR" in line])
    await update.message.reply_text(
        f"📊 Результаты UI тестов:\n{short_result[:3000]}" if short_result else "✅ UI тесты прошли успешно!"
    )


def parse_locust_output(output):
    metrics = {
        'RPS (Requests/Sec)': 'N/A',
        'Failures': 'N/A',
        'Average Response Time': 'N/A',
        'Total Requests': 'N/A'
    }

    # Ищем строку с итогами (Aggregated)
    for line in output.split('\n'):
        if "Aggregated" in line and "|" in line:
            # Разбиваем строку по вертикальной черте
            parts = [p.strip() for p in line.split('|')]
            # Стандартная таблица Locust:
            # Name | # reqs | # fails | Avg | Min | Max | Median | req/s
            if len(parts) >= 8:
                metrics['Total Requests'] = parts[1]
                metrics['Failures'] = parts[2]
                metrics['Average Response Time'] = f"{parts[3]}ms"
                metrics['RPS (Requests/Sec)'] = parts[7]
    return metrics


async def locust_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запуск нагрузки с отображением параметров и детальным отчетом"""

    # 1. Параметры теста
    users, spawn_rate, run_time = 10, 1, "1m"

    await update.message.reply_text(
        f"🚀 **Запуск нагрузочного теста**\n"
        f"--------------------------------\n"
        f"👥 Количество пользователей: `{users}`\n📈 Интенсивность появления пользователей: `{spawn_rate}/сек`\n⏱️ Время выполнения теста: `{run_time}`\n"
        f"⏳ Сбор данных начат...",
        parse_mode='Markdown'
    )

    # 2. Определение путей (Учитываем вложенность alex/talako)
    root_dir = Path(__file__).parent.parent
    results_dir = root_dir / "locust_results"
    results_dir.mkdir(exist_ok=True)

    # Формируем полный путь к скрипту
    locust_script = (root_dir / "alex_talako" / "pom_site" / "test" / "locust" / "load_test_main_page.py").resolve()

    # Пути для отчетов
    csv_prefix = results_dir / "run_stat"
    html_report = results_dir / "report.html"

    # Проверка на существование файла
    if not locust_script.exists():
        await update.message.reply_text(f"❌ Файл не найден! Проверь путь:\n`{locust_script}`", parse_mode='Markdown')
        return

    # 3. Формируем команду (Обязательно используем кавычки для путей в Windows)
    command = (
        f'locust -f "{locust_script}" --headless -u {users} -r {spawn_rate} '
        f'--run-time {run_time} --csv="{csv_prefix}" --html="{html_report}" --only-summary'
    )

    # 4. Выполнение
    result = await execute_command(command, update, timeout=150)

    # Вывод в консоль PyCharm для контроля
    print(f"DEBUG: Locust Result:\n{result}")

    # 5. Парсинг CSV (твоя логика)
    stats_file = f"{csv_prefix}_stats.csv"
    if os.path.exists(stats_file):
        with open(stats_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            main_page = next((l for l in lines if "/" in l and "GET" in l and "Aggregated" not in l), None)
            login_page = next((l for l in lines if "/login" in l), None)
            total = next((l for l in lines if "Aggregated" in l), None)

            def get_data(line):
                p = line.split(',')
                # Индексы: 2-Requests, 3-Failures, 9-RPS
                return {"req": p[2], "fail": p[3], "rps": round(float(p[9]), 2)}

            report_msg = "📊 **Результаты по страницам:**\n"
            if main_page:
                d = get_data(main_page)
                report_msg += f"\n🏠 **Главная страница:** {d['req']} запр. (Ошибок: {d['fail']}, RPS: {d['rps']})"
            if login_page:
                d = get_data(login_page)
                report_msg += f"\n🔑 **Страница Логин:** {d['req']} запр. (Ошибок: {d['fail']}, RPS: {d['rps']})"

            if total:
                t = get_data(total)
                report_msg += f"\n\n📈 **ИТОГО:**\nВсего запросов: `{t['req']}`\nОшибок: `{t['fail']}`\nСредний RPS: `{t['rps']}`"

            await update.message.reply_text(report_msg, parse_mode='Markdown')

    # 6. Отправка HTML-файла
    if html_report.exists():
        with open(html_report, 'rb') as doc:
            await update.message.reply_document(
                document=doc,
                filename="Locust_Full_Report.html",
                caption="📄 Полный интерактивный отчет"
            )

    # 7. Очистка временных CSV
    for f in results_dir.glob("run_stat_*.csv"):
        try:
            os.remove(f)
        except:
            pass


async def all_tests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запуск ВСЕХ тестов (API + UI) и сохранение результатов"""
    await update.message.reply_text("🔍 Запускаю все тесты (API и UI)...")

    # 1. Находим корень проекта и папку результатов в корне проекта
    root_dir = Path(__file__).parent.parent
    results_dir = root_dir / "allure-results"
    results_dir.mkdir(exist_ok=True)

    # 2. ОЧИСТКА (КРИТИЧНО для полного отчета, чтобы не было старых "хвостов")
    for file in results_dir.glob("*"):
        try:
            if file.is_file():
                file.unlink()
        except Exception as e:
            print(f"Ошибка удаления файла {file}: {e}")

    # 3. Путь ко всем тестам сразу (pytest сам найдет api и ui)
    test_suite_path = root_dir / "alex_talako" / "pom_site" / "test"

    # 4. Команда запуска (используем кавычки для Windows)
    command = f'pytest -s -v "{test_suite_path}" --alluredir="{results_dir}"'

    # Выполняем команду
    result = await execute_command(command, update)

    # 5. Отправляем скриншоты ошибок (если есть)
    await send_error_screenshots(update, context)

    # 6. Сводка (твоя логика)
    short_result = "\n".join([line for line in result.split("\n") if "FAILED" in line or "ERROR" in line])
    await update.message.reply_text(
        f"📊 Результаты всех тестов:\n{short_result[:3000]}" if short_result else "✅ Все тесты прошли успешно!"
    )


async def generate_allure_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Генерация отчета, текстовая сводка для телефона и отправка архива"""
    try:
        root_dir = Path(__file__).parent.parent
        results_dir = root_dir / "allure-results"
        report_dir = root_dir / "allure-report"

        if not results_dir.exists() or not any(results_dir.iterdir()):
            await update.message.reply_text("❌ Нет данных для отчета: папка allure-results пуста")
            return

        await update.message.reply_text("📈 Генерирую Allure-отчет...")
        report_dir.mkdir(exist_ok=True)

        command = f'allure generate "{results_dir}" --clean -o "{report_dir}"'
        await execute_command(command, update)

        # --- НОВЫЙ БЛОК: Сводка для телефона ---
        summary_file = report_dir / "widgets" / "summary.json"
        stats_text = ""
        if summary_file.exists():
            with open(summary_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                s = data['statistic']
                total = s['total']
                passed = s['passed']
                failed = s['failed'] + s['broken']
                skipped = s['skipped']
                pass_percent = round((passed / total) * 100, 1) if total > 0 else 0

                stats_text = (
                    f"📊 **Краткая сводка:**\n"
                    f"✅ Пройдено: `{passed}`\n"
                    f"❌ Упало: `{failed}`\n"
                    f"⏩ Пропущено: `{skipped}`\n"
                    f"🎯 Успешность: `{pass_percent}%`"
                )

        # --- Создание архива (твой код с небольшим фиксом пути) ---
        await update.message.reply_text("📦 Создаю архив...")
        timestamp = int(time.time())
        zip_name = f"allure_report_{timestamp}.zip"
        abs_zip_path = root_dir / zip_name

        with zipfile.ZipFile(abs_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(report_dir):
                for file in files:
                    file_path = Path(root) / file
                    arcname = os.path.relpath(file_path, report_dir)
                    zipf.write(file_path, arcname=f"AllureReport/{arcname}")

        # Отправка
        await update.message.reply_text("📤 Отправляю архив...")
        with open(abs_zip_path, 'rb') as zip_file:
            caption = f"{stats_text}\n\n📄 Полный отчет в архиве (для ПК)" if stats_text else "📊 Allure Report"
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=zip_file,
                filename=zip_name,
                caption=caption,
                parse_mode='Markdown'
            )

        os.remove(abs_zip_path)
        await update.message.reply_text("✅ Отчет готов!")

    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка: {str(e)}")

async def full_cycle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Полный цикл: тесты + отчет"""
    await all_tests(update, context)
    await generate_allure_report(update, context)

async def send_error_screenshots(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Находит и отправляет все скриншоты из папки screenshots"""
    screenshots_dir = Path(__file__).parent.parent / "screenshots"
    if screenshots_dir.exists():
        # Ищем все файлы .png в папке
        for photo_path in screenshots_dir.glob("*.png"):
            try:
                with open(photo_path, 'rb') as photo:
                    await context.bot.send_photo(
                        chat_id=update.effective_chat.id,
                        photo=photo,
                        caption=f"📸 Скриншот ошибки из теста: {photo_path.name}"
                    )
                # Удаляем файл после отправки, чтобы папка была чистой
                photo_path.unlink()
            except Exception as e:
                print(f"Ошибка при отправке скриншота: {e}")

def main():
    application = Application.builder().token(os.getenv("BOT_TOKEN")).build()

    handlers = [
        CommandHandler("start", start),
        CommandHandler("about", about),
        CommandHandler("api", api),
        CommandHandler("ui", ui),
        CommandHandler("locust_test", locust_test),
        CommandHandler("all_tests", all_tests),
        CommandHandler("allure_report", generate_allure_report),
        CommandHandler("full_report", full_cycle),
    ]

    for handler in handlers:
        application.add_handler(handler)

    print('Бот запущен')
    application.run_polling()


if __name__ == "__main__":
    main()
