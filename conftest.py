import os
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Playwright, APIRequestContext
from pages.components.login_form import LoginForm
from utils.config import BASE_URL


@pytest.fixture(scope="session")
def auth_context(browser, pytestconfig):

    context = browser.new_context()
    page = context.new_page()

    form = LoginForm(page)
    page.goto(BASE_URL)
    form.fill_username("standard_user")
    form.fill_password("secret_sauce")
    form.click_submit()

    auth_file = pytestconfig.rootpath / "data" / "auth_state.json"
    auth_file.parent.mkdir(parents=True, exist_ok=True)
    context.storage_state(path=auth_file)

    return auth_file


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


@pytest.fixture(scope="session")
def spotify_api(playwright: Playwright) -> APIRequestContext:
    if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
        pytest.skip("Faltan credenciales de Spotify. Se saltea el test.")

    spotify_auth_context = playwright.request.new_context(
        base_url="https://accounts.spotify.com"
    )

    auth_response = spotify_auth_context.post(
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
    spotify_auth_context.dispose()

    api_context = playwright.request.new_context(
        base_url="https://api.spotify.com",
        extra_http_headers={"Authorization": f"Bearer {token}"},
    )

    yield api_context

    api_context.dispose()


@pytest.fixture(scope="session")
def spotify_user_context(playwright: Playwright):
    user_token = os.getenv("SPOTIFY_USER_TOKEN")
    assert user_token is not None, "Falta configurar SPOTIFY_USER_TOKEN"

    context = playwright.request.new_context(
        base_url="https://api.spotify.com",
        extra_http_headers={
            "Authorization": f"Bearer {user_token}",
            "Content-Type": "application/json",
        },
    )

    yield context

    context.dispose()
