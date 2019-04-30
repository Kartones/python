import pytest
from random import shuffle

from checkout import Checkout
from discounts import Discounts
import settings


"""
Run with `python3 -m pytest` and optionally add ` -s` to display the print statements.

To run type checking, for example `mypy .` will work.
Note that will complain about this test file, but shouldn't about other files.
"""


test_data = [
    ([settings.PRODUCT_CODE_A, settings.PRODUCT_CODE_B, settings.PRODUCT_CODE_C], "22.50€"),
    ([settings.PRODUCT_CODE_A, settings.PRODUCT_CODE_B, settings.PRODUCT_CODE_A], "15.00€"),
    ([
        settings.PRODUCT_CODE_B, settings.PRODUCT_CODE_B, settings.PRODUCT_CODE_B, settings.PRODUCT_CODE_A,
        settings.PRODUCT_CODE_B
     ], "41.00€"),
    ([
        settings.PRODUCT_CODE_A, settings.PRODUCT_CODE_B, settings.PRODUCT_CODE_A, settings.PRODUCT_CODE_A,
        settings.PRODUCT_CODE_C, settings.PRODUCT_CODE_B, settings.PRODUCT_CODE_B
     ], "44.50€"),
]


def checkout_instance(products):
    discounts = Discounts(settings.DISCOUNTS, settings.AVAILABLE_PRODUCTS_MAP)
    checkout = Checkout(discounts)
    for product in products:
        checkout.add_product(product)

    return checkout


@pytest.mark.parametrize("products,expected_total", test_data)
def test_total_price_correctly_applies_discounts(products, expected_total):
    checkout = checkout_instance(products)

    print("\nCart contents:")
    print(checkout.contents)
    print("Total:", checkout.total)

    assert checkout.total == expected_total


@pytest.mark.parametrize("products,expected_total", test_data)
def test_add_product_order_doesnt_affects_total_price(products, expected_total):
    shuffle(products)

    checkout = checkout_instance(products)

    assert checkout.total == expected_total
