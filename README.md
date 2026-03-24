# QA Automation Framework: UI (SauceDemo) & API (Spotify)

Framework de automatización de pruebas integrales construido con Python, Playwright y Pytest. Este proyecto sirve como portfolio técnico, demostrando la capacidad de validar flujos críticos de E-commerce (UI) y gestionar integraciones complejas de servicios web (API REST) con manejo avanzado de autenticación OAuth 2.0.

## Objetivo

Desarrollar una suite de pruebas mantenible y escalable que aplique buenas prácticas de QA Automation, cubriendo tanto la interfaz gráfica (Page Object Model) como la capa de servicios (Endpoints, Status Codes, y flujos de autorización).

## Stack Tecnologico

- Python 3.10+
- Playwright
- Pytest
- pytest-playwright
- python-dotenv

## Arquitectura

El proyecto sigue una arquitectura orientada a mantenibilidad, dividida en dos capas:

**UI Testing (E-Commerce)**
- **Page Object Model (POM):** separa selectores y acciones de UI de la lógica de los tests.
- **Componentes reutilizables:** encapsula secciones comunes de interfaz en `pages/components`.

**API Testing (Spotify)**
- **Validación de Contratos:** Pruebas de integración validando métodos HTTP (GET, POST) y Status Codes (200, 201).
- **Gestión de Autenticación Avanzada:** Manejo de flujos OAuth 2.0 separando tokens de aplicación (Client Credentials) y tokens de usuario (Authorization Code) inyectados de forma segura mediante `.env`.
- **Fixtures en Pytest:** centraliza el setup de autenticación y reutilización de contextos (`APIRequestContext`) para ambas capas.

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
- pip (Gestor de paquetes de Python)
- Git
- Cuenta en [Spotify para Desarrolladores](https://developer.spotify.com/) (Para obtener las credenciales de la API)

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

- `auth_context` (scope session): autentica una vez y guarda estado en `data/auth_state.json` (UI).
- `logged_in_page` (scope function): crea una página autenticada para cada test (UI).
- **Contexto API:** Creación de contextos de petición HTTP aislados inyectando headers de autorización (Tokens Bearer) dinámicamente.

## Buenas Prácticas Implementadas

- Separación clara entre capa de página (POM), componentes y casos de prueba.
- Reutilización de estado autenticado para mejorar performance en pruebas UI.
- **Testing Integrado:** Inclusión de capa API funcional con validación de Status Codes, payload y manejo avanzado de OAuth 2.0.
- **Seguridad:** Ocultamiento estricto de credenciales y tokens de usuario mediante variables de entorno (`.env`).

## Roadmap

- [ ] **Request Chaining:** Encadenar peticiones API (ej: Crear Playlist -> Capturar ID -> Agregar canciones).
- [ ] **Testing Híbrido (E2E):** Generar data de prueba transaccional vía API de forma ultra rápida y validar su correcta visualización en la UI.
- [ ] Integrar reportes avanzados (por ejemplo, HTML/Allure).
- [ ] Agregar pipeline CI/CD (GitHub Actions) con ejecución automática por pull request.
