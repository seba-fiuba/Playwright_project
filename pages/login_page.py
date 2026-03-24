from playwright.sync_api import Page
from pages.components.login_form import LoginForm
from utils.config import BASE_URL


class LoginPage:
    """
    Representa la vista del login de usuario.
    Actúa como orquestador para realizar el login de usuario,
    delegando las interacciones con la UI al LoginForm
    """

    def __init__(self, page: Page):
        self.page = page
        self.form = LoginForm(page)

    def navigate(self):
        self.page.goto(BASE_URL)

    def login(self, username: str, password: str):
        self.form.fill_username(username)
        self.form.fill_password(password)
        self.form.click_submit()
