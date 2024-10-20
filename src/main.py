from functools import partial
import sqlite3

from dishka import make_async_container
from dishka.integrations.litestar import setup_dishka
from litestar import Litestar
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.plugins import SwaggerRenderPlugin

from src.ioc import AppProvider
from src.config import AppConfig
from src.presentation.web_api import HTTPPostController


def apply_migrations(app: Litestar, config: AppConfig) -> None:
    with sqlite3.connect(config.db_url, isolation_level=None) as conn, open(
        config.db_schema
    ) as sql_file:
        conn.executescript(sql_file.read())
        conn.commit()


def create_app() -> Litestar:
    config = AppConfig()
    app = Litestar(
        route_handlers=[HTTPPostController],
        on_startup=[partial(apply_migrations, config=config)],
        debug=True,
        openapi_config=OpenAPIConfig(
            title="App service",
            version="1.0.0",
            description="This is an example API",
            path="/docs",
            render_plugins=[SwaggerRenderPlugin()],
        ),
    )
    container = make_async_container(AppProvider(), context={AppConfig: config})
    setup_dishka(container=container, app=app)
    return app


def get_app() -> Litestar:
    return create_app()
