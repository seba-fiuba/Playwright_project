from pages.inventory_page import InventoryPage
from pages.product_detail_page import ProductDetailPage
from playwright.sync_api import Page, expect
from utils.config import BASE_URL, INVENTORY_PATH


def test_add_and_remove_to_cart(logged_in_page: Page):
    inventory_page = InventoryPage(logged_in_page)
    logged_in_page.goto(f"{BASE_URL}{INVENTORY_PATH}")
    inventory_page.action_button("Sauce Labs Backpack", "Add to  cart")
    button = inventory_page.obtain_button("Sauce Labs Backpack")
    expect(button).to_have_text("Remove")
    inventory_page.action_button("Sauce Labs Backpack", "Remove")
    expect(button).to_have_text("Add to cart")


def test_detail_product(logged_in_page: Page):
    inventory_page = InventoryPage(logged_in_page)
    detail_product = ProductDetailPage(logged_in_page)
    logged_in_page.goto(f"{BASE_URL}{INVENTORY_PATH}")
    inventory_page.map_to_product("Sauce Labs Backpack")
    expect(logged_in_page).to_have_url(f"{BASE_URL}inventory-item.html?id=4")
    detail_product.add_to_cart()
    button = detail_product.obtain_button()
    expect(button).to_be_visible()
