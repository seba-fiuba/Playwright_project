import pytest
from playwright.sync_api import sync_playwright
from pages.components.login_form import LoginForm
from utils.config import BASE_URL


@pytest.fixture(scope="session")
def auth_context(browser):

    context = browser.new_context()
    page = context.new_page()

    form = LoginForm(page)
    page.goto(BASE_URL)
    form.fill_username("standard_user")
    form.fill_password("secret_sauce")
    form.click_submit()

    context.storage_state(path="data/auth_state.json")

    return "data/auth_state.json"


@pytest.fixture(scope="function")
def logged_in_page(browser, auth_context):
    context = browser.new_context(storage_state=auth_context)
    page = context.new_page()
    yield page
    context.close()
