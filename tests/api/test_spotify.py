import pytest
import os
from playwright.sync_api import Playwright, APIRequestContext, expect
from data.data_api import VALID_ARTIST, SPOTIFY_URIS


@pytest.mark.api
@pytest.mark.parametrize("artist_name", VALID_ARTIST)
def test_search_valid_spotify_artist(spotify_api: APIRequestContext, artist_name):
    """
    Objetivo: Validar que el endpoint de búsqueda retorna el artista correcto.

    Pre:
        - Client Credentials Token válido inyectado en el contexto.
    Pasos:
        1. Realizar petición GET a /search con el nombre del artista.
    Pos:
        - Status Code 200 (OK).
        - La respuesta contiene un objeto 'artists' con al menos un resultado.
        - El nombre del primer resultado coincide con el parámetro de búsqueda.
    """

    response = spotify_api.get(f"/v1/search?q={artist_name}&type=artist")

    expect(response).to_be_ok()

    data = response.json()

    first_result = data["artists"]["items"][0]

    assert first_result["name"] == artist_name
    assert first_result["type"] == "artist"


@pytest.mark.api
def test_unauthorized_request(playwright: Playwright):
    """
    Objetivo: Validar que, al no usar los tokens requeridos, la API devuelva un error 401.

    Pre:
        - Contexto de API sin encabezado de Autorización.
    Pasos:
        1. Realizar petición GET al endpoint de búsqueda.
    Pos:
        - Status code 401 por acceso no autorizado.
        - La respuesta devuelve el status y el mensaje de error correspondiente.
    """
    api_context = playwright.request.new_context(base_url="https://api.spotify.com")

    response = api_context.get("/v1/search?q=rock&type=artist")

    assert response.status == 401

    error_json = response.json()

    assert error_json["error"]["status"] == 401
    assert error_json["error"]["message"] == "No token provided"

    api_context.dispose()


@pytest.mark.api
def test_create_playlist(spotify_user_context):
    """
    Objetivo: Validar que el endpoint que permite crear una playlist y el endpoint que permite agregar canciones a una playlist.

    Pre:
        - User Credentials Token válido inyectado en el contexto.
    Pasos:
        1. Realizar petición POST
    Pos:
        - Status Code 201 (OK) en ambos endpoints.
        - La respuesta de crear la playlist contiene un objeto 'playlist' con la información de la playlist creada.
        - La respuesta de agregar canciones la plylist contiene el snapshot_id que confirma que se agregaron las canciones.
    """
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
    playlist_id = data["id"]

    song_body = {"uris": SPOTIFY_URIS, "position": 0}

    response_playlist = spotify_user_context.post(
        f"https://api.spotify.com/v1/playlists/{playlist_id}/items", data=song_body
    )
    data_playlist = response_playlist.json()
    assert response_playlist.status == 201, "La canción no se agrego a la playlist"
    assert "snapshot_id" in data_playlist, "No se escribio el snapshor id"
