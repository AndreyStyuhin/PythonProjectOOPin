# test_product.py
import unittest
from src.product import Product, Smartphone, LawnGrass
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

    def test_create_smartphone(self):
        smartphone = Smartphone(
            "Samsung Galaxy S23 Ultra",
            "256GB, Серый цвет, 200MP камера",
            180000.0,
            5,
            95.5,
            "S23 Ultra",
            256,
            "Серый"
        )
        self.assertEqual(smartphone.name, "Samsung Galaxy S23 Ultra")
        self.assertEqual(smartphone.description, "256GB, Серый цвет, 200MP камера")
        self.assertEqual(smartphone.price, 180000.0)
        self.assertEqual(smartphone.quantity, 5)
        self.assertEqual(smartphone.efficiency, 95.5)
        self.assertEqual(smartphone.model, "S23 Ultra")
        self.assertEqual(smartphone.memory, 256)
        self.assertEqual(smartphone.color, "Серый")

    def test_create_lawngrass(self):
        lawngrass = LawnGrass(
            "Газонная трава",
            "Элитная трава для газона",
            500.0,
            20,
            "Россия",
            "7 дней",
            "Зеленый"
        )
        self.assertEqual(lawngrass.name, "Газонная трава")
        self.assertEqual(lawngrass.description, "Элитная трава для газона")
        self.assertEqual(lawngrass.price, 500.0)
        self.assertEqual(lawngrass.quantity, 20)
        self.assertEqual(lawngrass.country, "Россия")
        self.assertEqual(lawngrass.germination_period, "7 дней")
        self.assertEqual(lawngrass.color, "Зеленый")