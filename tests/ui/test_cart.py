from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from playwright.sync_api import Page


def test_cart(logged_in_page: Page):
    inventory = InventoryPage(logged_in_page)
    logged_in_page.goto("https://www.saucedemo.com/inventory.html")
    inventory.header.navigate_to_cart()
    cart = CartPage(logged_in_page)
    cart.purchase_item("Carlos", "Vives", "C12345")
