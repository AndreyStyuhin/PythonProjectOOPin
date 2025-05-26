#!/usr/bin/env python3
"""
Улучшенный скрипт для запуска тестов и генерации отчета о покрытии кода.
"""

import sys
import os
import subprocess
import shutil

def ensure_directory_exists(directory):
    """Создает директорию если она не существует."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"📁 Создана директория: {directory}")

def clean_previous_reports():
    """Очищает предыдущие отчеты coverage."""
    files_to_remove = ['.coverage', 'coverage.xml']
    dirs_to_remove = ['htmlcov']

    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)
            print(f"🗑️  Удален файл: {file}")

    for dir in dirs_to_remove:
        if os.path.exists(dir):
            shutil.rmtree(dir)
            print(f"🗑️  Удалена директория: {dir}")

def run_coverage_analysis():
    """Запускает полный анализ покрытия кода."""

    print("🧹 Очистка предыдущих отчетов...")
    clean_previous_reports()

    print("\n📊 Запуск тестов с измерением покрытия...")

    # Команда для запуска coverage
    cmd_run = [
        sys.executable, '-m', 'coverage', 'run',
        '--source=src',
        '--omit=*/tests/*,*/test_*,*/__pycache__/*,*/venv/*,*/env/*',
        '-m', 'unittest', 'discover', 'tests', '-v'
    ]

    print(f"Выполняется команда: {' '.join(cmd_run)}")

    try:
        # Запускаем тесты с coverage
        result = subprocess.run(cmd_run, cwd=os.getcwd(),
                              capture_output=True, text=True, timeout=60)

        print("📋 Вывод тестов:")
        print(result.stdout)

        if result.stderr:
            print("⚠️  Предупреждения/Ошибки:")
            print(result.stderr)

        if result.returncode != 0:
            print(f"❌ Тесты завершились с ошибкой (код: {result.returncode})")
            return False

        # Проверяем, что файл .coverage создался
        if not os.path.exists('.coverage'):
            print("❌ Файл .coverage не создался")
            return False

        print("✅ Тесты выполнены успешно, данные coverage собраны")

        # Генерируем консольный отчет
        print("\n📊 Генерация консольного отчета...")
        cmd_report = [sys.executable, '-m', 'coverage', 'report', '-m']

        report_result = subprocess.run(cmd_report, capture_output=True, text=True)

        if report_result.returncode == 0:
            print(report_result.stdout)

            # Извлекаем процент покрытия
            coverage_percent = extract_coverage_percentage(report_result.stdout)

            # Генерируем HTML отчет
            print("\n🌐 Генерация HTML отчета...")
            cmd_html = [sys.executable, '-m', 'coverage', 'html', '--directory=htmlcov']

            html_result = subprocess.run(cmd_html, capture_output=True, text=True)

            if html_result.returncode == 0:
                print("✅ HTML отчет создан успешно")

                # Проверяем создание файлов
                if os.path.exists('htmlcov') and os.path.exists('htmlcov/index.html'):
                    print(f"📁 HTML отчет доступен в: {os.path.abspath('htmlcov/index.html')}")
                else:
                    print("❌ HTML файлы не найдены")
                    return False
            else:
                print(f"❌ Ошибка создания HTML отчета: {html_result.stderr}")
                return False

            # Генерируем XML отчет
            print("\n📄 Генерация XML отчета...")
            cmd_xml = [sys.executable, '-m', 'coverage', 'xml']

            xml_result = subprocess.run(cmd_xml, capture_output=True, text=True)

            if xml_result.returncode == 0:
                print("✅ XML отчет создан успешно")
            else:
                print(f"⚠️  Предупреждение при создании XML отчета: {xml_result.stderr}")

            # Проверяем достижение целевого покрытия
            if coverage_percent >= 75:
                print(f"\n🎉 ОТЛИЧНО! Покрытие {coverage_percent}% превышает целевые 75%")
                return True
            else:
                print(f"\n⚠️  Покрытие {coverage_percent}% ниже целевых 75%")
                return False
        else:
            print(f"❌ Ошибка генерации отчета: {report_result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print("❌ Тайм-аут выполнения тестов")
        return False
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
        return False

def extract_coverage_percentage(report_output):
    """Извлекает процент покрытия из вывода coverage report."""
    lines = report_output.strip().split('\n')
    for line in lines:
        if 'TOTAL' in line:
            parts = line.split()
            if len(parts) >= 4:
                percentage_str = parts[-1].rstrip('%')
                try:
                    return float(percentage_str)
                except ValueError:
                    pass
    return 0.0

def check_environment():
    """Проверяет окружение и зависимости."""
    print("🔍 Проверка окружения...")

    # Проверяем Python версию
    print(f"🐍 Python версия: {sys.version}")

    # Проверяем coverage
    try:
        result = subprocess.run([sys.executable, '-m', 'coverage', '--version'],
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Coverage: {result.stdout.strip()}")
        else:
            print("❌ Coverage не работает корректно")
            return False
    except Exception:
        print("❌ Coverage не установлен. Установите: pip install coverage")
        return False

    # Проверяем структуру проекта
    required_dirs = ['src', 'tests']
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ Директория {dir_name} найдена")
        else:
            print(f"❌ Директория {dir_name} не найдена")
            return False

    # Проверяем наличие тестовых файлов
    test_files = [f for f in os.listdir('tests') if f.startswith('test_') and f.endswith('.py')]
    if test_files:
        print(f"✅ Найдены тестовые файлы: {', '.join(test_files)}")
    else:
        print("❌ Тестовые файлы не найдены")
        return False

    return True

def main():
    """Главная функция."""
    print("🚀 АНАЛИЗ ПОКРЫТИЯ КОДА ТЕСТАМИ")
    print("=" * 50)

    # Проверяем окружение
    if not check_environment():
        print("\n❌ Проверка окружения не пройдена")
        sys.exit(1)

    # Запускаем анализ покрытия
    success = run_coverage_analysis()

    print("\n" + "=" * 50)
    print("📋 ИТОГОВАЯ ИНФОРМАЦИЯ")
    print("=" * 50)

    if os.path.exists('htmlcov/index.html'):
        html_path = os.path.abspath('htmlcov/index.html')
        print(f"🌐 HTML отчет: file://{html_path}")

    if os.path.exists('coverage.xml'):
        xml_path = os.path.abspath('coverage.xml')
        print(f"📄 XML отчет: {xml_path}")

    print("\n📋 Команды для ручного запуска:")
    print("   coverage run --source=src -m unittest discover tests -v")
    print("   coverage report -m")
    print("   coverage html")

    if success:
        print("\n🎉 Анализ завершен успешно!")
        sys.exit(0)
    else:
        print("\n⚠️  Требуются улучшения")
        sys.exit(1)

if __name__ == "__main__":
    main()
