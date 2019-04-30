from collections import defaultdict
from typing import Dict

from discounts import Discounts
import settings


class ShoppingCart():

    def __init__(self, discounts: Discounts):
        self.discounts = discounts
        self.cart = defaultdict(int)  # type: Dict[str, int]

    def add_product(self, product_code: str, quantity: int = 1) -> None:
        if product_code not in settings.AVAILABLE_PRODUCTS_MAP.keys():
            raise ValueError("Product code '{}' not available".format(product_code))

        self.cart[product_code] += quantity

    def empty(self) -> None:
        self.cart = defaultdict(int)  # type: Dict[str, int]

    @property
    def contents(self) -> Dict[str, int]:
        return {
            settings.AVAILABLE_PRODUCTS_MAP[product_code].friendly_name: quantity
            for product_code, quantity in self.cart.items()
        }

    @property
    def total_amount_without_discounts(self) -> int:
        # NOTE: sum([]) = 0 , so empty cart scenario covered
        return sum([
            settings.AVAILABLE_PRODUCTS_MAP[product_code].price * quantity
            for product_code, quantity in self.cart.items()
        ])

    @property
    def total_amount(self) -> int:
        discounted_cart = self.total_amount_without_discounts - self.discounts.calculate_total_discount(self.cart)
        return discounted_cart
