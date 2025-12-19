from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from pathlib import Path
from dotenv import load_dotenv
import zipfile
import time
import asyncio
import os
import re


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

    # Подготовка директории для результатов
    results_dir = Path("./allure-results")
    results_dir.mkdir(exist_ok=True)

    # Очистка предыдущих результатов
    for file in results_dir.glob("*"):
        file.unlink()

    # Запуск pytest
    result = await execute_command(
        "pytest -s -v pom_site/test/api/ --alluredir=./allure-results",
        update
    )

    # Проверка наличия результатов тестов
    # if not any(results_dir.iterdir()):
    #     await update.message.reply_text("⚠️ Внимание: allure-results пуст. Возможно, тесты не запустились.")
    #     return

    # Отправка сокращенного отчета
    short_result = "\n".join([line for line in result.split("\n") if "FAILED" in line or "ERROR" in line])
    await update.message.reply_text(
        f"📊 Результаты тестов:\n{short_result[:3000]}" if short_result else "✅ Все тесты прошли успешно!"
    )


async def ui(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запуск тестов и сохранение результатов"""
    await update.message.reply_text("🔍 Запускаю тесты...")

    # Находим папку alex_talako, где лежит бот
    base_path = Path(__file__).parent
    # Склеиваем путь к папке с UI тестами
    test_path = base_path / "pom_site" / "test" / "ui"

    # Команда теперь использует АБСОЛЮТНЫЙ путь
    command = f"pytest -s -v {test_path} --alluredir=./allure-results"

    # Визуальный контроль в консоли PyCharm
    print(f"DEBUG: Запускаю тесты из папки: {test_path}")
    # Подготовка директории для результатов
    results_dir = Path("./allure-results")
    results_dir.mkdir(exist_ok=True)

    # Очистка предыдущих результатов
    for file in results_dir.glob("*"):
        file.unlink()

    # Запуск pytest
    result = await execute_command(
        "pytest -s -v pom_site/test/ui/ --alluredir=./allure-results",
        update
    )

    # Проверка наличия результатов тестов
    # if not any(results_dir.iterdir()):
    #     await update.message.reply_text("⚠️ Внимание: allure-results пуст. Возможно, тесты не запустились.")
    #     return
    await send_error_screenshots(update, context)

    # Отправка сокращенного отчета
    short_result = "\n".join([line for line in result.split("\n") if "FAILED" in line or "ERROR" in line])
    await update.message.reply_text(
        f"📊 Результаты тестов:\n{short_result[:3000]}" if short_result else "✅ Все тесты прошли успешно!"
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
    """Запуск тестов и сохранение результатов"""
    await update.message.reply_text("🔍 Запускаю тесты...")

    # Подготовка директории для результатов
    results_dir = Path("./allure-results")
    results_dir.mkdir(exist_ok=True)

    # Очистка предыдущих результатов
    for file in results_dir.glob("*"):
        file.unlink()

    # Запуск pytest
    result = await execute_command(
        "pytest -s -v pom_site/test --alluredir=./allure-results",
        update
    )

    # Проверка наличия результатов тестов
    # if not any(results_dir.iterdir()):
    #     await update.message.reply_text("⚠️ Внимание: allure-results пуст. Возможно, тесты не запустились.")
    #     return

    await send_error_screenshots(update, context)

    # Отправка сокращенного отчета
    short_result = "\n".join([line for line in result.split("\n") if "FAILED" in line or "ERROR" in line])
    await update.message.reply_text(
        f"📊 Результаты тестов:\n{short_result[:3000]}" if short_result else "✅ Все тесты прошли успешно!"
    )



async def generate_allure_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Генерация отчета и отправка архива"""
    try:
        # Проверка наличия результатов тестов
        results_dir = Path("./allure-results")
        if not results_dir.exists() or not any(results_dir.iterdir()):
            await update.message.reply_text("❌ Нет данных для отчета: папка allure-results пуста или отсутствует")
            return

        # Генерация отчета
        await update.message.reply_text("📈 Генерирую Allure-отчет...")
        report_dir = Path("./allure-report")
        report_dir.mkdir(exist_ok=True)

        gen_result = await execute_command(
            "allure generate ./allure-results --clean -o ./allure-report",
            update
        )

        # Проверка наличия сгенерированного отчета
        report_index = report_dir / "index.html"
        if not report_index.exists():
            await update.message.reply_text("❌ Ошибка генерации: index.html не найден в allure-report")
            return

        # Создание архива
        await update.message.reply_text("📦 Создаю архив...")
        timestamp = int(time.time())
        zip_name = f"allure_report_{timestamp}.zip"

        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Добавляем allure-report
            for root, _, files in os.walk(report_dir):
                for file in files:
                    file_path = Path(root) / file
                    arcname = os.path.join("allure-report", os.path.relpath(file_path, report_dir))
                    zipf.write(file_path, arcname=arcname)

            # Добавляем allure-results
            for root, _, files in os.walk(results_dir):
                for file in files:
                    file_path = Path(root) / file
                    arcname = os.path.join("allure-results", os.path.relpath(file_path, results_dir))
                    zipf.write(file_path, arcname=arcname)

        # Отправка архива
        await update.message.reply_text("📤 Отправляю архив...")
        with open(zip_name, 'rb') as zip_file:
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=zip_file,
                filename=zip_name,
                caption="📊 Allure Report (включая исходные данные)"
            )

        # Очистка временных файлов
        os.remove(zip_name)
        await update.message.reply_text("✅ Отчет успешно отправлен!")

    except Exception as e:
        await update.message.reply_text(f"⚠️ Критическая ошибка: {str(e)}")


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
