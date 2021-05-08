from discounts import (BulkPurchasePriceDiscount, BuyNGetOneFreeDiscount)
from product import Product


# NOTE: All prices in euro cents

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
# NOTE: order matters, discounts are applied according to this list order
# NOTE: If applying multiple discounts to the same product, results might not be correct ones.
#       e.g. BuyNGetOneFreeDiscount & BulkPurchasePriceDiscount to the same product, if amount is same in both
#       would cause bulk purchase one to count the free item as if were paid.
#       This could be solved by making discounts exclusive: e.g. each discount reports if applied and if so, we stop
#       checking further discounts.
DISCOUNTS = [
    BuyNGetOneFreeDiscount(product_code=PRODUCT_CODE_A, amount=2),
    BulkPurchasePriceDiscount(product_code=PRODUCT_CODE_B, amount=3, reduced_price=900),
    # This discount does nothing, but as the system needs at least one configured,
    # if don't want any discount active then use this
    # NoDiscount()
]

# ------------

AVAILABLE_PRODUCTS_MAP = {
    product.code: product for product in AVAILABLE_PRODUCTS
}
