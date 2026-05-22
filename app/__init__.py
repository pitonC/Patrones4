"""Application factory.

Aquí vive la pieza "View/Controller" del patrón MVC (que en Flask se conoce
como MTV: Model–Template–View). El factory cablea los tres componentes:

* Model       -> `app.models` (SQLAlchemy)
* Template    -> `app/templates/*.html` (Jinja2)
* View (ctrl) -> `app.routes` (los blueprints reciben requests y deciden qué
                                modelo y template usar)
"""
from __future__ import annotations

import os
from pathlib import Path

from flask import Flask

from .extensions import db


def _is_vercel_runtime() -> bool:
    return os.environ.get("VERCEL") == "1" or bool(os.environ.get("VERCEL_ENV"))


def _normalize_database_url(url: str) -> str:
    if url.startswith("postgres://"):
        return "postgresql://" + url[len("postgres://") :]
    return url


def create_app(config: dict | None = None) -> Flask:
    is_vercel = _is_vercel_runtime()
    if is_vercel:
        writable_root = Path(os.environ.get("VERCEL_TMPDIR", "/tmp"))
        instance_path = writable_root / "patrones4_instance"
        upload_dir = writable_root / "patrones4_uploads"
        app = Flask(
            __name__,
            instance_relative_config=True,
            instance_path=str(instance_path),
        )
    else:
        app = Flask(__name__, instance_relative_config=True)
        upload_dir = Path(app.root_path) / "static" / "uploads"

    instance_dir = Path(app.instance_path)
    instance_dir.mkdir(parents=True, exist_ok=True)
    upload_dir.mkdir(parents=True, exist_ok=True)
    database_url = os.environ.get("DATABASE_URL")
    resolved_database_url = _normalize_database_url(database_url) if database_url else (
        f"sqlite:///{instance_dir / 'photo_editor.sqlite3'}"
    )

    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-secret-change-me"),
        SQLALCHEMY_DATABASE_URI=resolved_database_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        UPLOAD_FOLDER=str(upload_dir),
        MAX_CONTENT_LENGTH=16 * 1024 * 1024,
    )
    if config:
        app.config.update(config)

    db.init_app(app)

    from . import models  # noqa: F401 — registra los modelos en SQLAlchemy
    from .routes.main import bp as main_bp
    from .routes.api import bp as api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    with app.app_context():
        db.create_all()

    return app
