from playwright.sync_api import Page
from pages.components.cart_manager import CartManager


class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.cart = CartManager(page)

    def purchase_item(self, name, lastname, postalcode):
        self.cart.checkout()
        self.cart.fill_information(name, lastname, postalcode)
        self.cart.confirm_purchase()
