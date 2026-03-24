import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from data.login_credentials import invalid_credentials
from utils.config import BASE_URL, INVENTORY_PATH

pytestmark = pytest.mark.ui


def test_valid_login(page: Page):
    """Verifica el Happy path de autenticación con credenciales válidas"""
    login_page = LoginPage(page)

    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")
    expect(page).to_have_url(f"{BASE_URL}{INVENTORY_PATH}")


@pytest.mark.parametrize("username, password, error_msg", invalid_credentials)
def test_invalid_login(page, username, password, error_msg):
    """Verifica el rechazo de login y el mensaje de error para credenciales inválidas"""
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(username, password)

    error_locator = page.locator("[data-test='error']")
    expect(error_locator).to_contain_text(error_msg)
