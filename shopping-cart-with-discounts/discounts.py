from abc import (ABC, abstractmethod)
from typing import (Dict, List, Optional)

from product import Product


class Discounts():

    def __init__(self, discounts: List["BaseDiscount"], available_products: Dict[str, Product]) -> None:
        self.discounts = discounts
        self.available_products = available_products

        discounts_count = len(self.discounts) - 1
        for index, discount in enumerate(self.discounts):
            if index < discounts_count:
                discount.set_next(self.discounts[index+1])

    def calculate_total_discount(self, products: Dict[str, int]) -> int:
        if not self.discounts:
            raise RuntimeError("Need to have setup at least one discount")
        return self.discounts[0].execute(products, self.available_products)


class BaseDiscount(ABC):

    def __init__(self) -> None:
        self.next_discount = None  # type: Optional["BaseDiscount"]

    def set_next(self, discount: "BaseDiscount") -> None:
        self.next_discount = discount

    @abstractmethod
    def calculate_discount(self, products: Dict[str, int], available_products: Dict[str, Product]) -> int:
        pass

    def execute(self, products: Dict[str, int], available_products: Dict[str, Product]) -> int:
        discount = self.calculate_discount(products, available_products)
        if self.next_discount:
            return discount + self.next_discount.execute(products, available_products)
        else:
            return discount

# --- Available discount implementations: ---


class NoDiscount(BaseDiscount):
    """
    Dummy discount for when not wanting to have any real discount active, or for testing, etc.
    """

    def calculate_discount(self, products: Dict[str, int], available_products: Dict[str, Product]) -> int:
        return 0


class BuyNGetOneFreeDiscount(BaseDiscount):
    """
    Buy N units and one becomes free e.g. 2x1
    """

    def __init__(self, product_code: str, amount: int) -> None:
        super().__init__()
        self.product_code = product_code
        self.amount = amount

    def calculate_discount(self, products: Dict[str, int], available_products: Dict[str, Product]) -> int:
        discount = 0

        if self.product_code not in products.keys():
            return discount

        quantity = products[self.product_code]
        while quantity > 0 and quantity >= self.amount:
            quantity -= self.amount
            discount += available_products[self.product_code].price

        return discount


class BulkPurchasePriceDiscount(BaseDiscount):
    """
    Buy at least N units and have a reduced per unit price
    """

    def __init__(self, product_code: str, amount: int, reduced_price: int) -> None:
        super().__init__()
        self.product_code = product_code
        self.amount = amount
        self.reduced_price = reduced_price

    def calculate_discount(self, products: Dict[str, int], available_products: Dict[str, Product]) -> int:
        discount = 0

        if self.product_code not in products.keys():
            return discount

        quantity = products[self.product_code]
        if quantity >= self.amount:
            original_aggregated_price = available_products[self.product_code].price * quantity
            discount = original_aggregated_price - self.reduced_price * quantity

        return discount
