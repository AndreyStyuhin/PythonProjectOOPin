# product.py
class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        """
        Инициализация объекта Product

        :param name: название товара
        :param description: описание товара
        :param price: цена товара (с копейками)
        :param quantity: количество товара в наличии (в штуках)
        """
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    def __str__(self):
        return f"{self.name}, {int(self.__price)} руб. Остаток: {self.quantity} шт."

    @classmethod
    def new_product(cls, params: dict, products: list = None):
        """
        Создает новый экземпляр Product из словаря параметров.
        Если товар с таким же именем уже существует, обновляет его количество и выбирает максимальную цену.

        :param params: словарь с параметрами товара (name, description, price, quantity)
        :param products: список товаров, в которых нужно искать дубликаты (по имени)
        :return: новый или обновленный экземпляр Product
        """
        if products is None:
            products = []

        # Поиск товара с таким же именем
        for product in products:
            if product.name.lower() == params["name"].lower():
                # Обновление количества и выбор максимальной цены
                product.quantity += params["quantity"]
                product.price = max(product.price, params["price"])
                return product

        # Если дубликат не найден, создаем новый товар
        return cls(
            name=params["name"],
            description=params["description"],
            price=params["price"],
            quantity=params["quantity"]
        )

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if value <= 0:
            print(f"Некорректная цена: {value}. Цена товара должна быть больше нуля.")
            raise ValueError("Цена не может быть меньше или равна нулю")
        self.__price = value

    def __add__(self, other):
        if type(self) is not type(other):
            raise TypeError(f"Нельзя складывать товары разных типов: {type(self).__name__} и {type(other).__name__}")
        return self.price * self.quantity + other.price * other.quantity

    @classmethod
    def get_products_string(cls, search_str: object, params: object) -> None:
        pass


class Smartphone(Product):
    def __init__(self, name: str, description: str, price: float, quantity: int, 
                 efficiency: float, model: str, memory: int, color: str):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    def __init__(self, name: str, description: str, price: float, quantity: int, 
                 country: str, germination_period: str, color: str):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color