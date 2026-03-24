from playwright.sync_api import Page, Locator, expect


class CartManager:
    """Componentes del carrito de compras y las distintas interacciones con estos"""

    def __init__(self, page: Page):
        self.page = page
        self.checkout_button: Locator = page.locator('[data-test="checkout"]')
        self.name_input: Locator = page.locator('[data-test="firstName"]')
        self.lastname_input: Locator = page.locator('[data-test="lastName"]')
        self.zip_input: Locator = page.locator('[data-test="postalCode"]')
        self.continue_button: Locator = page.locator('[data-test="continue"]')
        self.finish_button: Locator = page.locator('[data-test="finish"]')
        self.complete_order: Locator = page.locator('[data-test="complete-header"]')

    def checkout(self):
        self.checkout_button.click()

    def fill_information(self, name: str, lastname: str, postalcode: str):
        self.name_input.fill(name)
        self.lastname_input.fill(lastname)
        self.zip_input.fill(postalcode)
        self.continue_button.click()

    def confirm_purchase(self):
        self.finish_button.click()
        expect(self.complete_order).to_be_visible()
