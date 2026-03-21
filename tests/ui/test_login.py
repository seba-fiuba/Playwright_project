import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from data.login_credentials import invalid_credentials


## Happy path test
def test_valid_login(page: Page):
    login_page = LoginPage(page)

    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")


##Unhappy path test


@pytest.mark.parametrize("username, password, error_msg", invalid_credentials)
def test_invalid_login(page, username, password, error_msg):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(username, password)

    error_locator = page.locator("[data-test='error']")
    expect(error_locator).to_contain_text(error_msg)


def test_logeado(logged_in_page: Page):
    logged_in_page.goto("https://www.saucedemo.com/inventory.html")
    titulo = logged_in_page.get_by_text("Swag Labs")
    expect(titulo).to_be_visible()
