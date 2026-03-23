from playwright.sync_api import APIRequestContext, expect


def test_buscar_artista_spotify(spotify_api: APIRequestContext):
    response = spotify_api.get("/v1/search?q=bizarrap&type=artist")

    expect(response).to_be_ok()

    datos = response.json()

    primer_resultado = datos["artists"]["items"][0]

    assert primer_resultado["name"] == "Bizarrap"
    assert primer_resultado["type"] == "artist"

    print(f"\nPerfil de Bizarrap: {primer_resultado['external_urls']['spotify']}")
