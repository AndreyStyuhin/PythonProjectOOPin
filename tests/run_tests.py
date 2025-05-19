import unittest
import sys
from io import StringIO
import datetime

# Импортируем тестовые классы
from tests.test_product import TestProduct
from tests.test_category import TestCategory

# Создаем тестовый загрузчик
loader = unittest.TestLoader()

# Создаем тестовый набор
test_suite = unittest.TestSuite()

# Добавляем тесты в набор
test_suite.addTest(loader.loadTestsFromTestCase(TestProduct))
test_suite.addTest(loader.loadTestsFromTestCase(TestCategory))

# Перенаправляем вывод в StringIO
output = StringIO()
runner = unittest.TextTestRunner(stream=output, verbosity=2)

# Запускаем тесты
result = runner.run(test_suite)

# Формируем отчет
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
report = f"""
=== Отчет о прохождении тестов ===
Дата и время: {timestamp}

Всего тестов: {result.testsRun}
Успешно: {result.testsRun - len(result.failures) - len(result.errors)}
Ошибок: {len(result.errors)}
Неудач: {len(result.failures)}

=== Детали ===
{output.getvalue()}
"""

# Сохраняем отчет в файл
with open("test_report.txt", "w", encoding="utf-8") as f:
    f.write(report)

print(f"Отчет сохранен в файл test_report.txt")

# Возвращаем код выхода в зависимости от результата тестов
sys.exit(not result.wasSuccessful())
