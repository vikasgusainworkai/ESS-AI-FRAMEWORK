import logging
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse

from ess_app.config import settings
from ess_app.users.router import router as users_router
from ess_app.users.store import DuplicateEmailError, UserNotFoundError

logging.basicConfig(level=settings.log_level)
logger = logging.getLogger("ess_app")

app = FastAPI(title=settings.app_name, version="0.2.0")
app.include_router(users_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    # One message per field; submitted values are not echoed back.
    details = []
    for err in exc.errors():
        loc = err["loc"]
        field = ".".join(str(p) for p in loc[1:]) or str(loc[0])
        if err["type"] == "json_invalid":
            field = "body"
        details.append({"field": field, "message": err["msg"].removeprefix("Value error, ")})
    return JSONResponse(status_code=422, content={"error": "validation_error", "details": details})


@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(request: Request, exc: UserNotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=404, content={"error": "user_not_found", "message": "User not found."}
    )


@app.exception_handler(DuplicateEmailError)
async def duplicate_email_handler(request: Request, exc: DuplicateEmailError) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={
            "error": "email_already_exists",
            "message": "A user with this email already exists.",
        },
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    # Log the detail server-side; never return stack traces or internals to the client.
    logger.exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(status_code=500, content={"error": "internal_error"})


USERS_PAGE = Path(__file__).parent / "static" / "users.html"


@app.get("/", include_in_schema=False)
def users_page() -> FileResponse:
    return FileResponse(USERS_PAGE, media_type="text/html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "environment": settings.environment}
