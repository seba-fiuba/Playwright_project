import pytest
import allure
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from playwright.sync_api import Page
from utils.config import BASE_URL, INVENTORY_PATH

pytestmark = pytest.mark.ui


@allure.epic("Plataforma E-commerce")
@allure.feature("Compra de producto")
@allure.story("Compra exitosa")
def test_cart(logged_in_page: Page):
    """Verifica el flujo completo (E2E) desde agregar el producto al carrito hasta finalizar la compra"""
    with allure.step("Iniciar sesion y agregar producto al carrito"):

        inventory = InventoryPage(logged_in_page)
        logged_in_page.goto(f"{BASE_URL}{INVENTORY_PATH}")
    with allure.step("Confirmar compra"):
        inventory.header.navigate_to_cart()
        cart = CartPage(logged_in_page)
        cart.purchase_item("Carlos", "Vives", "C12345")
