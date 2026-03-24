from playwright.sync_api import Page, Locator


class Header:
    """Componente del header del sitio que se comparte en todas las páginas"""

    def __init__(self, page: Page):
        self.page = page
        self.cart_button: Locator = page.locator('[data-test="shopping-cart-link"]')

    def navigate_to_cart(self):
        self.cart_button.click()
