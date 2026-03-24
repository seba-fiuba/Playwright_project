# E-Commerce QA Automation Framework

Framework de automatizacion de pruebas E2E para la plataforma de demo [SauceDemo](https://www.saucedemo.com/), construido con Python, Playwright y Pytest.

## Objetivo

Validar flujos criticos del e-commerce de forma mantenible y escalable, aplicando buenas practicas de automatizacion.

## Stack Tecnologico

- Python 3.10+
- Playwright
- Pytest
- pytest-playwright
- python-dotenv

## Arquitectura

El proyecto sigue una arquitectura orientada a mantenibilidad:

- Page Object Model (POM): separa selectores y acciones de UI de la logica de los tests.
- Componentes reutilizables: encapsula secciones comunes de interfaz en `pages/components`.
- Fixtures en Pytest: centraliza setup de autenticacion y reutilizacion de contexto.

## Estructura del Proyecto

```text
.
├── conftest.py
├── requirements.txt
├── data/
│   ├── auth_state.json
│   ├── data_api.py
│   └── login_credentials.py
├── pages/
│   ├── cart_page.py
│   ├── inventory_page.py
│   ├── login_page.py
│   ├── product_detail_page.py
│   └── components/
│       ├── cart_manager.py
│       ├── header.py
│       └── login_form.py
├── tests/
│   ├── api/
│   │   └── test_spotify.py
│   └── ui/
│       ├── test_cart.py
│       ├── test_login.py
│       └── test_product.py
└── utils/
```

## Requisitos

- Python 3.10 o superior
- pip

## Configuración de Variables de Entorno (Spotify API)

El proyecto incluye una plantilla `.env.example` para evitar compartir secretos reales.

1. Copiar la plantilla:

```bash
cp .env.example .env
```

2. Completar las credenciales en `.env`:

```env
SPOTIFY_CLIENT_ID=tu_client_id
SPOTIFY_CLIENT_SECRET=tu_client_secret
SPOTIFY_USER_TOKEN=tu_user_token
```

Notas:

- El archivo `.env` ya está ignorado por git.
- `SPOTIFY_CLIENT_ID` y `SPOTIFY_CLIENT_SECRET` se usan en `conftest.py` mediante `load_dotenv()` y `os.getenv(...)` para obtener el token de cliente.
- `SPOTIFY_USER_TOKEN` se usa en `tests/api/test_spotify.py` para el test de creacion de playlists (`test_create_playlist`).

### 🔑 Obtención del Token de Usuario (Para tests de escritura - POST)

Para ejecutar los tests de creación o modificación (POST/PUT), Spotify requiere un **Authorization Code Flow** con permisos específicos. Para generar este token localmente, utilizamos Postman simulando el flujo completo de autenticación:

**Paso 1: Configurar la App en Spotify**
1. En el [Spotify Developer Dashboard](https://developer.spotify.com/dashboard), ve a la configuración (Settings) de tu App.
2. Agrega la siguiente URL en **Redirect URIs**: `https://oauth.pstmn.io/v1/callback` y guarda los cambios.

**Paso 2: Generar el Token con Postman**
1. Abre Postman, crea una nueva Request y ve a la pestaña **Authorization**.
2. Selecciona el tipo **OAuth 2.0** y configura los siguientes parámetros en "Configure New Token":
   - **Grant Type:** Authorization Code
   - **Callback URL:** `https://oauth.pstmn.io/v1/callback`
   - **Auth URL:** `https://accounts.spotify.com/authorize`
   - **Access Token URL:** `https://accounts.spotify.com/api/token`
   - **Client ID / Client Secret:** (Tus credenciales de la app)
   - **Scope:** `playlist-modify-public playlist-modify-private`
3. Haz clic en **"Get New Access Token"**, inicia sesión en la ventana emergente y acepta los permisos.
4. Postman capturará el token de usuario (Bearer). Cópialo y pégalo en tu archivo `.env` bajo la variable `SPOTIFY_USER_TOKEN`.

*Nota: Este token tiene una validez temporal. Si el test devuelve un error 401, simplemente regenera el token en Postman.*

## Instalacion

1. Clonar repositorio:

```bash
git clone https://github.com/tu-usuario/tu-repo.git
cd tu-repo
```

2. Crear entorno virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Instalar navegadores de Playwright:

```bash
playwright install
```

## Ejecucion de Pruebas

Ejecutar toda la suite:

```bash
pytest
```

Ejecutar solo UI:

```bash
pytest tests/ui
```

Ejecutar solo API:

```bash
pytest tests/api
```

Ejecutar un archivo puntual:

```bash
pytest tests/ui/test_login.py
```

Modo verbose:

```bash
pytest -v
```

## Fixtures Relevantes

- `auth_context` (scope session): autentica una vez y guarda estado en `data/auth_state.json`.
- `logged_in_page` (scope function): crea una pagina autenticada para cada test.

## Buenas Practicas Implementadas

- Separacion clara entre capa de pagina, componentes y casos de prueba.
- Reutilizacion de estado autenticado para mejorar performance.
- Estructura preparada para escalar con pruebas API y nuevos modulos.

## Roadmap

- Expandir pruebas API en `tests/api`.
- Integrar reportes avanzados (por ejemplo, HTML/Allure).
- Agregar pipeline CI con ejecucion automatica por pull request.
