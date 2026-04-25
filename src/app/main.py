from __future__ import annotations

from sanic import Sanic
from sanic.exceptions import SanicException
from sanic.response import html, json

from app.config import settings
from app.db import SessionLocal, engine
from app.routes import api
from app.ui import INDEX_HTML


def create_app() -> Sanic:
    try:
        return Sanic.get_app("test_pythonmid")
    except SanicException:
        pass

    app = Sanic("test_pythonmid")
    app.blueprint(api)

    @app.middleware("request")
    async def inject_session(request):
        request.ctx.session = SessionLocal()

    @app.middleware("response")
    async def close_session(request, _response):
        session = getattr(request.ctx, "session", None)
        if session is not None:
            await session.close()

    @app.exception(Exception)
    async def handle_unexpected_error(_request, exc):
        if isinstance(exc, SanicException):
            return json({"error": str(exc)}, status=exc.status_code)
        app.logger.exception("Unhandled error", exc_info=exc)
        return json({"error": "Internal server error"}, status=500)

    @app.get("/health")
    async def health(_request):
        return json({"status": "ok"})

    @app.get("/")
    async def index(_request):
        return html(INDEX_HTML)

    @app.before_server_stop
    async def close_engine(_app, _loop):
        await engine.dispose()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host=settings.host, port=settings.port, debug=settings.debug, access_log=True)
