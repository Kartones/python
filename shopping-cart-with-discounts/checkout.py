from typing import List

from discounts import Discounts
import settings
from shopping_cart import ShoppingCart


class Checkout():

    def __init__(self, discounts: Discounts) -> None:
        self.shopping_cart = ShoppingCart(discounts)

    def add_product(self, product_code: str) -> None:
        self.shopping_cart.add_product(product_code)

    def empty(self) -> None:
        self.shopping_cart.empty()

    @property
    def total(self) -> str:
        return "{:.2f}€".format(self.shopping_cart.total_amount / 100)

    @property
    def contents(self) -> str:
        return "\n".join([
            "{} x{}".format(product_name, quantity) for product_name, quantity in self.shopping_cart.contents.items()
        ])
