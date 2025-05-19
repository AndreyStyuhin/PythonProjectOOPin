# test_category.py
import unittest
from src.product import Product
from src.category import Category


class TestCategory(unittest.TestCase):
    def setUp(self):
        # Сброс атрибутов класса перед каждым тестом
        Category.category_count = 0
        Category.product_count = 0

    def test_category_initialization(self):
        category = Category("Test Category", "Test Description")
        self.assertEqual(category.name, "Test Category")
        self.assertEqual(category.description, "Test Description")
        self.assertEqual(category.products, [])

    def test_category_count(self):
        Category("Category 1", "Description 1")
        self.assertEqual(Category.category_count, 1)
        Category("Category 2", "Description 2")
        self.assertEqual(Category.category_count, 2)

    def test_product_count(self):
        product1 = Product("Product 1", "Description 1", 100, 10)
        product2 = Product("Product 2", "Description 2", 200, 20)

        Category("Category 1", "Description 1", [product1])
        self.assertEqual(Category.product_count, 1)

        Category("Category 2", "Description 2", [product2])
        self.assertEqual(Category.product_count, 2)

    def test_add_product(self):
        category = Category("Test Category", "Test Description")
        product = Product("Test Product", "Test Description", 100, 10)
        category.add_product(product)
        self.assertIn(product, category.products)
        self.assertEqual(Category.product_count, 1)

    def test_category_str(self):
        product1 = Product("Product 1", "Description 1", 100, 5)
        product2 = Product("Product 2", "Description 2", 200, 10)
        category = Category("Test Category", "Test Description", [product1, product2])

        expected_str = "Test Category, количество продуктов: 15 шт."
        self.assertEqual(str(category), expected_str)

    def test_category_str_empty(self):
        category = Category("Test Category", "Test Description")
        expected_str = "Test Category, количество продуктов: 0 шт."
        self.assertEqual(str(category), expected_str)

    def test_products_info(self):
        product1 = Product("Product 1", "Description 1", 100, 5)
        product2 = Product("Product 2", "Description 2", 200, 10)
        category = Category("Test Category", "Test Description", [product1, product2])

        expected_info = [
            "Product 1, 100 руб. Остаток: 5 шт.",
            "Product 2, 200 руб. Остаток: 10 шт."
        ]
        self.assertEqual(category.products_info, expected_info)

    def test_products_info_empty(self):
        category = Category("Test Category", "Test Description")
        self.assertEqual(category.products_info, [])