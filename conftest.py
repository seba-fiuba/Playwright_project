import os
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Playwright, APIRequestContext
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


##----------------------API TEST------------------------

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")


@pytest.fixture
def spotify_api(playwright: Playwright) -> APIRequestContext:
    auth_context = playwright.request.new_context(
        base_url="https://accounts.spotify.com"
    )

    auth_response = auth_context.post(
        "/api/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        form={
            "grant_type": "client_credentials",
            "client_id": SPOTIFY_CLIENT_ID,
            "client_secret": SPOTIFY_CLIENT_SECRET,
        },
    )

    assert auth_response.ok, f"Error al pedir token: {auth_response.text()}"

    token = auth_response.json()["access_token"]
    auth_context.dispose()

    api_context = playwright.request.new_context(
        base_url="https://api.spotify.com",
        extra_http_headers={"Authorization": f"Bearer {token}"},
    )

    yield api_context

    api_context.dispose()
