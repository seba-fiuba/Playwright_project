# E-Commerce QA Automation Framework

Framework de automatizacion de pruebas E2E para la plataforma de demo [SauceDemo](https://www.saucedemo.com/), construido con Python, Playwright y Pytest.

## Objetivo

Validar flujos criticos del e-commerce de forma mantenible y escalable, aplicando buenas practicas de automatizacion.

## Stack Tecnologico

- Python 3.10+
- Playwright
- Pytest
- pytest-playwright

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
│   └── ui/
│       ├── test_cart.py
│       ├── test_login.py
│       └── test_product.py
└── utils/
```

## Requisitos

- Python 3.10 o superior
- pip

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