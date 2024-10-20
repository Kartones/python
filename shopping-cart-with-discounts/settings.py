from discounts import (BulkPurchasePriceDiscount, BuyNGetOneFreeDiscount)
from product import Product


# NOTE: All prices in euro cents (1.00€ = 100 "euro cents"), avoid using floating point numbers for currency

# Define here the product codes
PRODUCT_CODE_A = "PRODUCT CODE #1"
PRODUCT_CODE_B = "PRODUCT CODE #2"
PRODUCT_CODE_C = "PRODUCT CODE #3"


# Define here which products can be purchased
AVAILABLE_PRODUCTS = [
    Product(code=PRODUCT_CODE_A, friendly_name="Product A user-friendly name", price=500),
    Product(code=PRODUCT_CODE_B, friendly_name="Product B user-friendly name", price=1000),
    Product(code=PRODUCT_CODE_C, friendly_name="Product C user-friendly name", price=750),
]

# Define here which discounts are active
# Note that order matters, although each discount is independant from the others
DISCOUNTS = [
    BuyNGetOneFreeDiscount(product_code=PRODUCT_CODE_A, amount=2),
    BulkPurchasePriceDiscount(product_code=PRODUCT_CODE_B, amount=3, reduced_price=900),
    # This discount does nothing, but as the system needs at least one configured,
    # if don't want any discount active, or for testing, can use it
    # NoDiscount()
]

# ------------

AVAILABLE_PRODUCTS_MAP = {
    product.code: product for product in AVAILABLE_PRODUCTS
}
