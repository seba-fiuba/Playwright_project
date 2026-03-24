from playwright.sync_api import Page, Locator


class LoginForm:
    """Componentes del Login y las interacciones con los mismos"""

    def __init__(self, page: Page):
        self.page = page
        self.username_input: Locator = page.locator('[data-test="username"]')
        self.password_input: Locator = page.locator('[data-test="password"]')
        self.login_button: Locator = page.locator('[data-test="login-button"]')

    def fill_username(self, username: str):
        self.username_input.fill(username)

    def fill_password(self, password: str):
        self.password_input.fill(password)

    def click_submit(self):
        self.login_button.click()
