from playwright.sync_api import Page
from pages.components.login_form import LoginForm
from utils.config import BASE_URL


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.form = LoginForm(page)

    def navigate(self):
        self.page.goto(BASE_URL)

    def login(self, username: str, password: str):
        self.form.fill_username(username)
        self.form.fill_password(password)
        self.form.click_submit()
