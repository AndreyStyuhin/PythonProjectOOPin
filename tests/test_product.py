# test_product.py
import unittest
from src.product import Product
from src.category import Category


class TestProduct(unittest.TestCase):
    def setUp(self):
        # Сброс атрибутов класса перед каждым тестом
        Category.category_count = 0
        Category.product_count = 0

    def test_product_initialization(self):
        product = Product("Test Product", "Test Description", 100, 10)
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.description, "Test Description")
        self.assertEqual(product.price, 100)
        self.assertEqual(product.quantity, 10)

    def test_new_product(self):
        product1 = Product("Test Product 1", "Test Description 1", 100, 10)
        product2 = Product("Test Product 2", "Test Description 2", 200, 20)
        category = Category("Test Category", "Test Description", [product1, product2])
        new_product = Product.new_product({"name": "Test Product 1", "description": "Test Description 1", "price": 150, "quantity": 5}, category.products)
        self.assertEqual(new_product.name, "Test Product 1")
        self.assertEqual(new_product.description, "Test Description 1")
        self.assertEqual(new_product.price, 150)
        self.assertEqual(new_product.quantity, 15)
        self.assertEqual(Category.product_count, 2)

    def test_product_str(self):
        product = Product("Test Product", "Test Description", 99.99, 5)
        expected_str = "Test Product, 99 руб. Остаток: 5 шт."
        self.assertEqual(str(product), expected_str)

    def test_product_str_with_zero_price(self):
        product = Product("Test Product", "Test Description", 0.99, 5)
        expected_str = "Test Product, 0 руб. Остаток: 5 шт."
        self.assertEqual(str(product), expected_str)