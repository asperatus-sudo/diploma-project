from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from pathlib import Path
from dotenv import load_dotenv
import zipfile
import time
import asyncio
import os
import json
import glob
import logging
import sys

ROOT_DIR = Path(__file__).parent.parent
LOG_FILE_PATH = ROOT_DIR / "bot.log"


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(name)s - %(message)s',
    handlers=[
        logging.FileHandler("bot.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout) # Чтобы видеть логи в консоли PyCharm
    ]
)
logger = logging.getLogger("QA_NINJA_BOT")

logger.info("=== СИСТЕМА МОНИТОРИНГА КАЧЕСТВА ЗАПУЩЕНА ===")


load_dotenv()

async def execute_command(cmd: str, update: Update, timeout: int = 300) -> str:
    """Выполняет shell-команду с таймаутом и возвращает результат"""
    user = update.effective_user.username
    logger.info(f"AUDIT - USER: @{user} - EXEC_CMD: {cmd}")
    try:
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        logger.info(f"PROCESS_STARTED - PID: {proc.pid}")

        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout)

        if proc.returncode == 0:
            logger.info(f"PROCESS_SUCCESS - PID: {proc.pid}")
        else:
            logger.warning(f"PROCESS_FAILED - PID: {proc.pid} - EXIT_CODE: {proc.returncode}")

        output = f"STDOUT:\n{stdout.decode().strip()}" if stdout else ""
        output += f"\nSTDERR:\n{stderr.decode().strip()}" if stderr else ""
        return output.strip()
    except asyncio.TimeoutError:
        logger.error(f"TIMEOUT_ERROR - CMD: {cmd} - LIMIT: {timeout}s")
        return f"❌ Таймаут ({timeout} сек)"
    except Exception as e:
        logger.error(f"CRITICAL_EXCEPTION - CMD: {cmd} - MSG: {str(e)}", exc_info=True)
        return f"⚠️ Ошибка: {str(e)}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    logger.info(f"USER_ACCESS - USER: @{update.effective_user.username} - ACTION: STARTED_BOT")
    welcome_text = (
        f"Привет, {user_name}! Я бот дипломного проекта. Давай проверим систему на прочность:\n\n"
        
        "📊 <b>ТЕСТЫ:</b>\n"
        "🔹 <code>/api</code> — API тесты\n"
        "🔹 <code>/ui</code> — UI тесты\n"
        "🔹 <code>/locust_test</code> — Нагрузка\n"
        "🔹 <code>/full_report</code> — Полный цикл\n\n"

        "📦 <b>СЕРВИС:</b>\n"
        "• <code>/allure_report</code> — Отчет\n"
        "• <code>/clear</code> — Очистка\n"
        "• <code>/about</code> — Инфо"
    )
    await update.message.reply_text(welcome_text, parse_mode='HTML')



async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    about_text = (
        "🤖 <b>Telegram Bot for QA Automation</b>\n\n"
        "Программный комплекс, разработанный Александром Талако. "
        "Он объединяет инструменты тестирования в общую систему мониторинга качества.\n\n"
        "🛠 <b>Технологический фундамент:</b>\n"
        "• <b>Python 3.14 & Pytest</b>: Современная база для стабильной работы.\n"
        "• <b>API & Security</b>: Проверка бизнес-логики и аудит безопасности заголовков.\n"
        "• <b>UI Automation</b>: Selenium с использованием паттерна <b>Page Object Model</b>, "
        "что делает тесты читаемыми и легкими в поддержке.\n"
        "• <b>Performance</b>: Нагрузочное тестирование системы через Locust.\n"
        "• <b>CI/CD Integration</b>: Полная автоматизация запуска в облаке GitHub Actions.\n\n"
        "🎯 <b>Главная цель:</b>\n"
        "Создание надежного «регрессионного щита», который проверяет функциональность "
        "и защищенность системы при каждом обновлении кода.\n\n"
        "👨‍💻 <b>Автор</b>: @asperatus99 (Александр Талако)\n"
        "Развиваю навыки на стыке QA Automation и Cybersecurity."
    )
    await update.message.reply_text(about_text, parse_mode='HTML')


async def api(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запуск тестов и сохранение результатов"""
    logger.info(f"USER_ACTION - USER: @{update.effective_user.username} - CMD: /api")
    await update.message.reply_text("🔍 Запускаю тесты...")

    # 1. Находим корень и папку результатов в корне проекта
    root_dir = Path(__file__).parent.parent
    results_dir = root_dir / "allure-results"
    results_dir.mkdir(exist_ok=True)

    logger.info(f"FILESYSTEM - ACTION: CLEANING_DIRECTORY - PATH: {results_dir}")
    files_deleted = 0
    # 2. Очистка (чтобы в отчете по /api были ТОЛЬКО свежие API-результаты)
    for file in results_dir.glob("*"):
        try:
            if file.is_file():
                file.unlink()
                files_deleted += 1
        except Exception as e:
            logger.error(f"FILESYSTEM_ERROR - FILE: {file} - MSG: {e}")
            print(f"Ошибка удаления файла {file}: {e}")

    logger.info(f"FILESYSTEM - CLEANUP_COMPLETE - REMOVED: {files_deleted} files")

    # 3. Путь к самим тестам
    test_path = root_dir / "alex_talako" / "pom_site" / "test" / "api"

    # 4. Команда запуска (используем кавычки для Windows)
    command = f'pytest -s -v "{test_path}" --alluredir="{results_dir}"'

    # Выполняем команду
    result = await execute_command(command, update)

    # 5. Сводка
    short_result = "\n".join([line for line in result.split("\n") if "FAILED" in line or "ERROR" in line])
    if short_result:
        logger.warning(f"TEST_RESULTS - STATUS: FAILED - USER: @{update.effective_user.username}")
    else:
        logger.info(f"TEST_RESULTS - STATUS: SUCCESS - USER: @{update.effective_user.username}")
    await update.message.reply_text(
        f"📊 Результаты API тестов:\n{short_result[:3000]}" if short_result else "✅ API тесты прошли успешно!"
    )


async def ui(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запуск UI-тестов с гарантированной чистотой отчета и скриншотами"""
    logger.info(f"USER_ACTION - USER: @{update.effective_user.username} - CMD: /ui")
    await update.message.reply_text("🔍 Запускаю UI-тесты...")

    # 1. Находим корень проекта дважды двигаемся вверх
    root_dir = Path(__file__).parent.parent
    results_dir = root_dir / "allure-results"  # Папка в КОРНЕ проекта
    results_dir.mkdir(exist_ok=True)

    logger.info(f"FILESYSTEM - ACTION: CLEANING_DIRECTORY - PATH: {results_dir}")
    files_deleted = 0
    # 2. Очистка (чтобы в отчете по /ui были ТОЛЬКО свежие UI-результаты)
    for file in results_dir.glob("*"):
        try:
            if file.is_file():
                file.unlink()
                files_deleted += 1
        except Exception as e:
            logger.error(f"FILESYSTEM_ERROR - FILE: {file} - MSG: {e}")
            print(f"Ошибка удаления файла {file}: {e}")

    logger.info(f"FILESYSTEM - CLEANUP_COMPLETE - REMOVED: {files_deleted} files")

    # 3. Путь к самим тестам (теперь правильно: через alex_talako)
    test_path = root_dir / "alex_talako" / "pom_site" / "test" / "ui"

    # 4. Команда запуска (используем кавычки для Windows)
    # Используем --alluredir="${results_dir}" для указания пути к allure
    command = f'pytest -s -v "{test_path}" --alluredir="{results_dir}"'

    # Выполняем команду
    result = await execute_command(command, update)

    # 5. Отправляем скриншоты ошибок (если есть)
    logger.info("ARTIFACTS - ACTION: SENDING_ERROR_SCREENSHOTS")
    await send_error_screenshots(update, context)

    # 6. Сводка (твоя логика)
    short_result = "\n".join([line for line in result.split("\n") if "FAILED" in line or "ERROR" in line])
    if short_result:
        logger.warning(f"TEST_RESULTS - STATUS: UI_FAILED - USER: @{update.effective_user.username}")
    else:
        logger.info(f"TEST_RESULTS - STATUS: UI_SUCCESS - USER: @{update.effective_user.username}")
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
    logger.info(f"USER_ACTION - USER: @{update.effective_user.username} - CMD: /locust_test - PARAMS: users={users}, rate={spawn_rate}, time={run_time}")
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
        logger.error(f"FILESYSTEM_ERROR - LOCUST_SCRIPT_NOT_FOUND - PATH: {locust_script}")
        await update.message.reply_text(f"❌ Файл не найден! Проверь путь:\n`{locust_script}`", parse_mode='Markdown')
        return

    # 3. Формируем команду (Обязательно используем кавычки для путей в Windows)
    command = (
        f'locust -f "{locust_script}" --headless -u {users} -r {spawn_rate} '
        f'--run-time {run_time} --csv="{csv_prefix}" --html="{html_report}" --only-summary'
    )

    # 4. Выполнение
    result = await execute_command(command, update, timeout=150)
    logger.info("LOAD_TEST_EXECUTION_FINISHED")

    # Вывод в консоль PyCharm для контроля
    print(f"DEBUG: Locust Result:\n{result}")

    # 5. Парсинг CSV
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
    logger.info(f"USER_ACTION - USER: @{update.effective_user.username} - CMD: /all_tests")
    await update.message.reply_text("🔍 Запускаю все тесты (API и UI)...")

    # 1. Находим корень проекта и папку результатов в корне проекта
    root_dir = Path(__file__).parent.parent
    results_dir = root_dir / "allure-results"
    results_dir.mkdir(exist_ok=True)

    logger.info(f"FILESYSTEM - ACTION: ROTATING_ALL_RESULTS - PATH: {results_dir}")
    files_deleted = 0
    # 2. ОЧИСТКА (КРИТИЧНО для полного отчета, чтобы не было старых "хвостов")
    for file in results_dir.glob("*"):
        try:
            if file.is_file():
                file.unlink()
                files_deleted += 1
        except Exception as e:
            logger.error(f"FILESYSTEM_ERROR - FILE: {file} - MSG: {e}")
            print(f"Ошибка удаления файла {file}: {e}")

    logger.info(f"FILESYSTEM - CLEANUP_COMPLETE - REMOVED: {files_deleted} files")
    # 3. Путь ко всем тестам сразу (pytest сам найдет api и ui)
    test_suite_path = root_dir / "alex_talako" / "pom_site" / "test"

    # 4. Команда запуска (используем кавычки для Windows)
    command = f'pytest -s -v "{test_suite_path}" --alluredir="{results_dir}"'

    # Выполняем команду
    result = await execute_command(command, update)

    # 5. Отправляем скриншоты ошибок (если есть)
    await send_error_screenshots(update, context)

    # 6. Сводка
    await send_brief_report(update, context, str(results_dir))

    logger.info("ALL_TESTS_CYCLE_COMPLETE")

async def generate_allure_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Генерация отчета, текстовая сводка для телефона и отправка архива"""
    try:
        user = update.effective_user.username
        logger.info(f"REPORT_GEN - ACTION: START_ALLURE_GEN - USER: @{user}")
        root_dir = Path(__file__).parent.parent
        results_dir = root_dir / "allure-results"
        report_dir = root_dir / "allure-report"

        if not results_dir.exists() or not any(results_dir.iterdir()):
            logger.warning(f"REPORT_GEN - STATUS: NO_DATA - USER: @{user}")
            await update.message.reply_text("❌ Нет данных для отчета: папка allure-results пуста")
            return

        await update.message.reply_text("📈 Генерирую Allure-отчет...")
        report_dir.mkdir(exist_ok=True)

        command = f'allure generate "{results_dir}" --clean -o "{report_dir}"'
        await execute_command(command, update)

        # Сводка для телефона
        summary_file = report_dir / "widgets" / "summary.json"
        stats_text = ""
        if summary_file.exists():
            with open(summary_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                s = data['statistic']
                total = s['total']
                passed = s['passed']
                failed_real = s['failed'] + s['broken']
                xfails = s.get('skipped', 0)
                pass_percent = round((passed / total) * 100, 1) if total > 0 else 0

                stats_text = (
                    f"📊 **Краткая сводка:**\n"
                    f"✅ Пройдено: `{passed}`\n"
                    f"⚠️ Ожидаемые ошибки (xfail): `{xfails}`\n"
                    f"❌ Реальные сбои (failed): `{failed_real}`\n"
                    f"🎯 Успешность: `{pass_percent}%`"
                )

        # --- Создание архива (твой код с небольшим фиксом пути) ---
        await update.message.reply_text("📦 Создаю архив...")
        logger.info("REPORT_GEN - ACTION: CREATING_ZIP_ARCHIVE")
        timestamp = int(time.time())
        zip_name = f"allure_report_{timestamp}.zip"
        abs_zip_path = root_dir / zip_name

        with zipfile.ZipFile(abs_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            file_count = 0
            for root, _, files in os.walk(report_dir):
                for file in files:
                    file_path = Path(root) / file
                    arcname = os.path.relpath(file_path, report_dir)
                    zipf.write(file_path, arcname=f"AllureReport/{arcname}")
                    file_count += 1
            logger.info(f"REPORT_GEN - ARCHIVE_READY - FILES_ZIPPED: {file_count}")

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
        logger.info(f"REPORT_GEN - STATUS: SUCCESS - ARCHIVE_SENT_AND_DELETED")
        await update.message.reply_text("✅ Отчет готов!")

    except Exception as e:
        logger.error(f"REPORT_GEN_ERROR - MSG: {str(e)}", exc_info=True)
        await update.message.reply_text(f"⚠️ Ошибка: {str(e)}")

async def full_cycle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Полный цикл: тесты + отчет"""
    logger.info(f"USER_ACTION - USER: @{update.effective_user.username} - CMD: /full_report (TOTAL_SCAN)")
    await all_tests(update, context)
    await generate_allure_report(update, context)

async def send_brief_report(update, context, results_path="allure-results"):
    logger.info("REPORT_ANALYSIS - ACTION: PARSING_JSON_RESULTS")
    api_stats = {'passed': 0, 'failed': 0, 'xfail': 0}
    ui_stats = {'passed': 0, 'failed': 0, 'xfail': 0}

    result_files = glob.glob(f"{results_path}/*-result.json")

    for file_path in result_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            status = data.get('status')
            status_details = str(data.get('statusDetails', ''))
            # Ищем в fullName путь к тесту, чтобы понять API это или UI
            full_name = data.get('fullName', '').lower()

            # Определяем категорию
            if 'api' in full_name:
                category = api_stats
            else:
                category = ui_stats

            # Считаем статус
            if status == 'passed':
                category['passed'] += 1
            elif status == 'skipped' or 'xfail' in status_details.lower():
                category['xfail'] += 1
            elif status == 'failed':
                category['failed'] += 1

    # Формируем красивый текст
    report_text = (
        f"📊 <b>ОТЧЕТ ПО УРОВНЯМ</b>\n\n"
        f"🔹 <b>API:</b>\n"
        f"  ✅ Пройдено: <code>{api_stats['passed']}</code>\n"
        f"  ⚠️ Ожидаемые ошибки: <code>{api_stats['xfail']}</code>\n"
        f"  ❌ Ошибки: <code>{api_stats['failed']}</code>\n\n"
        f"🔸 <b>UI:</b>\n"
        f"  ✅ Пройдено: <code>{ui_stats['passed']}</code>\n"
        f"  ❌ Ошибки: <code>{ui_stats['failed']}</code>\n\n"
        f"<b>Статус:</b> Завершено"
    )

    logger.info("REPORT_ANALYSIS - STATUS: BRIEF_SENT_TO_USER")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=report_text, parse_mode='HTML')

async def send_error_screenshots(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Находит и отправляет все скриншоты из папки screenshots"""
    screenshots_dir = Path(__file__).parent.parent / "screenshots"
    if screenshots_dir.exists():
        logger.info(f"ARTIFACTS - ACTION: SCANNING_SCREENSHOTS - PATH: {screenshots_dir}")
        photo_count = 0
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
                photo_count += 1
            except Exception as e:
                logger.error(f"ARTIFACT_ERROR - FILE: {photo_path.name} - MSG: {e}")
                print(f"Ошибка при отправке скриншота: {e}")

        logger.info(f"ARTIFACTS - STATUS: COMPLETE - SENT_AND_CLEANED: {photo_count}")


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Глобальная очистка временных данных и отчетов"""
    user = update.effective_user.username
    logger.warning(f"SYSTEM_CLEANUP_INITIATED - USER: @{user}")

    await update.message.reply_text("🧹 Очищаю системные компоненты...")

    root_dir = Path(__file__).parent.parent
    folders = [
        root_dir / "allure-results",
        root_dir / "allure-report",
        root_dir / "locust_results",
        root_dir / "screenshots"
    ]

    files_deleted = 0
    for folder in folders:
        if folder.exists():
            for file in folder.glob("*"):
                try:
                    if file.is_file():
                        file.unlink()
                        files_deleted += 1
                except Exception as e:
                    logger.error(f"CLEANUP_ERROR - FILE: {file} - MSG: {e}")

    logger.info(f"SYSTEM_CLEANUP_COMPLETE - FILES_REMOVED: {files_deleted}")

    report_text = (
        f"✨ <b>Система очистки завершена</b>\n"
        f"───────────────────\n"
        f"Удалено объектов: <code>{files_deleted}</code>\n"
        f"Статус: <b>Готов для новых тестов</b>"
    )
    await update.message.reply_text(report_text, parse_mode='HTML')

def main():
    try:
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
            CommandHandler("clear", clear),
        ]

        for handler in handlers:
            application.add_handler(handler)

        logger.info("SYSTEM_READY - STATUS: POLLING_STARTED")
        print('Бот запущен')
        application.run_polling()

    except Exception as e:
        logger.critical(f"SYSTEM_CRASH - MSG: {str(e)}", exc_info=True)

    finally:
        logger.info("SYSTEM_SHUTDOWN - STATUS: OFFLINE")


if __name__ == "__main__":
    main()
