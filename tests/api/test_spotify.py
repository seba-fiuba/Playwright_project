import pytest
import os
from playwright.sync_api import Playwright, APIRequestContext, expect
from data.data_api import VALID_ARTIST


@pytest.mark.api
@pytest.mark.parametrize("artist_name", VALID_ARTIST)
def test_search_valid_spotify_artist(spotify_api: APIRequestContext, artist_name):
    response = spotify_api.get(f"/v1/search?q={artist_name}&type=artist")

    expect(response).to_be_ok()

    data = response.json()

    first_result = data["artists"]["items"][0]

    assert first_result["name"] == artist_name
    assert first_result["type"] == "artist"

    print(f"\nPerfil de Bizarrap: {first_result['external_urls']['spotify']}")


@pytest.mark.api
def test_unauthorized_request(playwright: Playwright):
    api_context = playwright.request.new_context(base_url="https://api.spotify.com")

    response = api_context.get("/v1/search?q=rock&type=artist")

    assert response.status == 401

    error_json = response.json()

    assert error_json["error"]["status"] == 401
    assert error_json["error"]["message"] == "No token provided"

    api_context.dispose()


@pytest.mark.api
def test_create_playlist(spotify_user_context):
    playlist_body = {
        "name": "Playlist portfolio",
        "description": "Creada 100%",
        "public": False,
    }

    response = spotify_user_context.post("/v1/me/playlists", data=playlist_body)

    assert response.status == 201, "El status code no fue 201 created"

    data = response.json()
    assert data["name"] == "Playlist portfolio"
    assert data["type"] == "playlist", "El objeto creado no es una playlist"
    print(f"PLAYLIST ID: {data['id']}")
