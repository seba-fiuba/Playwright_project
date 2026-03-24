import pytest
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from playwright.sync_api import Page
from utils.config import BASE_URL, INVENTORY_PATH

pytestmark = pytest.mark.ui


def test_cart(logged_in_page: Page):
    """Verifica el flujo completo (E2E) desde agregar el producto al carrito hasta finalizar la compra"""
    inventory = InventoryPage(logged_in_page)
    logged_in_page.goto(f"{BASE_URL}{INVENTORY_PATH}")
    inventory.header.navigate_to_cart()
    cart = CartPage(logged_in_page)
    cart.purchase_item("Carlos", "Vives", "C12345")
