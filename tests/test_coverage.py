#!/usr/bin/env python3
"""
Скрипт для запуска тестов и генерации отчета о покрытии кода.
Цель: достичь покрытия тестами более 75%.
"""

import sys
import os
import subprocess
import unittest


def run_coverage_with_subprocess():
    """
    Запускает анализ покрытия кода через subprocess для избежания конфликтов импорта.
    """
    try:
        print("Запуск тестов с измерением покрытия...")

        # Запускаем coverage run
        result = subprocess.run([
            sys.executable, '-m', 'coverage', 'run',
            '--source=src',
            '--omit=*/tests/*,*/test_*,*/__pycache__/*',
            '-m', 'unittest', 'discover', 'tests', '-v'
        ], capture_output=True, text=True)

        print("STDOUT:")
        print(result.stdout)

        if result.stderr:
            print("STDERR:")
            print(result.stderr)

        if result.returncode != 0:
            print(f"❌ Тесты завершились с ошибкой (код: {result.returncode})")
            return False

        # Генерируем отчет
        print("\n" + "=" * 60)
        print("ОТЧЕТ О ПОКРЫТИИ КОДА ТЕСТАМИ")
        print("=" * 60)

        # Консольный отчет
        report_result = subprocess.run([
            sys.executable, '-m', 'coverage', 'report', '-m'
        ], capture_output=True, text=True)

        print(report_result.stdout)

        # Извлекаем процент покрытия из вывода
        lines = report_result.stdout.strip().split('\n')
        total_line = [line for line in lines if 'TOTAL' in line]

        if total_line:
            # Парсим строку TOTAL для получения процента
            parts = total_line[0].split()
            if len(parts) >= 4:
                coverage_percent = parts[-1].rstrip('%')
                try:
                    coverage_float = float(coverage_percent)
                    print(f"\nОбщее покрытие: {coverage_float}%")

                    if coverage_float >= 75:
                        print("✅ УСПЕХ: Покрытие тестами превышает 75%!")
                        return True
                    else:
                        print(f"❌ ВНИМАНИЕ: Покрытие тестами {coverage_float}% меньше требуемых 75%")
                        return False
                except ValueError:
                    print("❌ Не удалось определить процент покрытия")
                    return False

        # Генерируем HTML отчет
        subprocess.run([
            sys.executable, '-m', 'coverage', 'html'
        ])

        # Генерируем XML отчет
        subprocess.run([
            sys.executable, '-m', 'coverage', 'xml'
        ])

        return True

    except Exception as e:
        print(f"Ошибка при выполнении coverage: {e}")
        return False


def run_tests_directly():
    """
    Запускает тесты напрямую без coverage для проверки их работоспособности.
    """
    print("Запуск тестов без измерения покрытия...")

    try:
        # Добавляем текущую директорию в PYTHONPATH
        current_dir = os.getcwd()
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)

        # Загружаем и запускаем тесты
        loader = unittest.TestLoader()
        start_dir = 'tests'
        suite = loader.discover(start_dir, pattern='test_*.py')

        # Запускаем тесты
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)

        if result.wasSuccessful():
            print("✅ Все тесты прошли успешно!")
            return True
        else:
            print(f"❌ Тесты завершились с ошибками: {len(result.failures)} failures, {len(result.errors)} errors")
            return False

    except Exception as e:
        print(f"Ошибка при выполнении тестов: {e}")
        return False


def check_dependencies():
    """
    Проверяет наличие необходимых зависимостей.
    """
    try:
        result = subprocess.run([sys.executable, '-m', 'coverage', '--version'],
                                capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Coverage установлен: {result.stdout.strip()}")
            return True
        else:
            print("❌ Coverage не установлен или работает некорректно")
            return False
    except Exception:
        print("❌ Пакет 'coverage' не установлен.")
        print("Установите его командой: pip install coverage")
        return False


def main():
    """
    Главная функция для запуска анализа покрытия.
    """
    print("Запуск анализа покрытия кода тестами...")
    print("=" * 60)

    # Проверяем зависимости
    if not check_dependencies():
        sys.exit(1)

    # Проверяем структуру проекта
    if not os.path.exists('src'):
        print("❌ Папка 'src' не найдена.")
        sys.exit(1)

    if not os.path.exists('tests'):
        print("❌ Папка 'tests' не найдена.")
        sys.exit(1)

    # Сначала запускаем тесты без coverage для проверки
    print("\n1. Проверка работоспособности тестов...")
    if not run_tests_directly():
        print("❌ Тесты не проходят. Исправьте ошибки перед измерением покрытия.")
        sys.exit(1)

    # Запускаем анализ покрытия
    print("\n2. Измерение покрытия кода...")
    success = run_coverage_with_subprocess()

    print("\n" + "=" * 60)
    print("ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ")
    print("=" * 60)
    print("📁 HTML отчет сохранен в папке: htmlcov/")
    print("📄 XML отчет сохранен в файле: coverage.xml")
    print("💡 Откройте htmlcov/index.html в браузере для детального просмотра")

    print("\n📋 Команды для ручного запуска:")
    print("   coverage run --source=src -m unittest discover tests")
    print("   coverage report -m")
    print("   coverage html")

    if success:
        print("\n🎉 Анализ завершен успешно!")
        sys.exit(0)
    else:
        print("\n⚠️  Требуется улучшение покрытия тестами.")
        sys.exit(1)


if __name__ == "__main__":
    main()
