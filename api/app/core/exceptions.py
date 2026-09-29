"""Format uniforme des erreurs : {"error": {"code", "message"}}."""

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

async def http_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    """Formate les HTTPException."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.status_code, "message": str(exc.detail)}}
    )

async def validation_handler(
    request: Request, exc: RequestValidationError     
) -> JSONResponse:
    """Formate les erreurs de validation (422)."""

    # garder seulement la première erreur
    premiere = exc.errors()[0]

    # retirer "body" / "query" pour garder le nom du champ
    champ = ".".join(str(p) for p in premiere["loc"][1:])
    message = f"{champ} : {premiere["msg"]}" if champ else premiere["msg"]

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"error": {"code": status.HTTP_422_UNPROCESSABLE_CONTENT, "message": message}}
    )

def enregistrer_handlers(app: FastAPI) -> None:
    """Branche les handlers sur l'app."""
    app.add_exception_handler(StarletteHTTPException, http_handler)
    app.add_exception_handler(RequestValidationError, validation_handler)