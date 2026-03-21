from playwright.sync_api import Page, Locator


class ProductDetailPage:
    def __init__(self, page: Page):
        self.page = page
        self.add_button: Locator = page.locator('[data-test="add-to-cart"]')
        self.remove_button: Locator = page.locator('[data-test="remove"]')
        self.back_button: Locator = page.locator('[data-test="back-to-products"]')

    def add_to_cart(self):
        self.add_button.click()

    def back_to_inventory(self):
        self.back_button.click()

    def obtain_button(self):
        return self.remove_button
