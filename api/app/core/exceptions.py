from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

async def http_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"erreur": {"code": exc.status_code, "message": str(exc.detail)}}
    )

async def validation_handler(
    request: Request, exc: RequestValidationError     
) -> JSONResponse:
    premiere = exc.errors()[0]
    champ = ".".join(str(p) for p in premiere["loc"][1:])
    message = f"{champ} : {premiere["msg"]}" if champ else premiere["msg"]

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"erreur": {"code": status.HTTP_422_UNPROCESSABLE_CONTENT, "message": message}}
    )

def enregistrer_handlers(app: FastAPI) -> None:
    app.add_exception_handler(StarletteHTTPException, http_handler)
    app.add_exception_handler(RequestValidationError, validation_handler)