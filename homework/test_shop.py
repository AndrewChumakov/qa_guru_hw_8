"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def other_product():
    return Product("paper", 20, "This is a paper", 2000)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        assert product.check_quantity(1001) is False
        assert product.check_quantity(1000) is True

    def test_product_buy(self, product):
        product.buy(900)
        assert product.quantity == 100

    def test_product_buy_more_than_available(self, product):
        try:
            product.buy(1001)
        except ValueError:
            "Количества не хватает"


class TestCart:
    def test_cart_add_product(self, product, other_product, cart):
        cart.add_product(product)
        assert cart.products[product] == 1
        cart.add_product(other_product, 100)
        assert cart.products[other_product] == 100
        cart.add_product(product, 2)
        assert cart.products[product] == 3

    def test_cart_remove_product(self, product, cart):
        cart.add_product(product)
        cart.remove_product(product)
        assert product not in cart.products
        cart.add_product(product)
        cart.remove_product(product, 2)
        assert product not in cart.products
        cart.add_product(product, 2)
        cart.remove_product(product, 2)
        assert product not in cart.products
        cart.add_product(product, 100)
        cart.remove_product(product, 70)
        assert cart.products[product] == 30

    def test_cart_clear(self, cart, product):
        cart.add_product(product, 10)
        cart.clear()
        assert product not in cart.products

    def test_cart_get_total_price(self, cart, product, other_product):
        total_price = cart.get_total_price()
        assert total_price == 0
        cart.add_product(product, 5)
        cart.add_product(other_product, 15)
        total_price = cart.get_total_price()
        assert total_price == 800

    def test_cart_buy(self, cart, product):
        cart.add_product(product, 500)
        cart.buy()
        assert product.quantity == 500

    def test_cant_cart_buy(self, cart, product):
        cart.add_product(product, 1001)
        with pytest.raises(ValueError):
            cart.buy()
