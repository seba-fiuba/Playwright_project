from playwright.sync_api import Page, Locator
from pages.components.header import Header


class InventoryPage:
    """
    Representa la pantalla principal del catálogo de productos.
    Sirve como punto de entrada para acceder al Header, al menú lateral
    y a la grilla de artículos disponibles.
    """

    def __init__(self, page: Page):
        self.page = page
        self.header = Header(page)
        self.item_container: Locator = page.locator('[data-test="inventory-item"]')

    def action_button(self, product_name: str, btn_action: str):
        product = self.item_container.filter(has_text=product_name)
        product.get_by_role("button", name=btn_action).click()

    def obtain_button(self, product_name: str):
        product = self.item_container.filter(has_text=product_name)
        return product.get_by_role("button")

    def map_to_product(self, product_name: str):
        product = self.item_container.filter(has_text=product_name)
        product.locator('[data-test="item-4-title-link"]').click()
