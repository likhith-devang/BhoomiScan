from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.config import get_settings
from app.database import Base, engine
from app.db_migrate import ensure_schema
from app.models import Analysis, Document, DocumentComparison, FinalReport, LedgerRecord, PropertyCase, User  # noqa: F401
from app.routers.analysis import router as analysis_router
from app.routers.auth import router as auth_router
from app.routers.property_cases import router as property_cases_router
from app.routers.reports import router as reports_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    settings.STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    if not getattr(app.state, "skip_db_init", False):
        Base.metadata.create_all(bind=engine)
        ensure_schema(engine)
    yield


app = FastAPI(
    title="BhoomiScan",
    description="Your AIvocate. We help you check property papers before you buy.",
    version="0.1.0",
    lifespan=lifespan,
)

settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _error_payload(message: str, status_code: int) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"detail": message})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    messages = []
    for error in exc.errors():
        loc = error.get("loc", [])
        msg = error.get("msg", "Invalid request.")
        if "Value error, " in msg:
            msg = msg.replace("Value error, ", "")
        if "confirm_password" in loc or "passwords_match" in str(error.get("type", "")):
            messages.append("Passwords do not match.")
        else:
            messages.append(msg)
    return _error_payload(messages[0] if messages else "Invalid request.", 422)


@app.exception_handler(ValidationError)
async def pydantic_exception_handler(_: Request, exc: ValidationError) -> JSONResponse:
    first = exc.errors()[0]["msg"] if exc.errors() else "Invalid request."
    return _error_payload(first.replace("Value error, ", ""), 422)


app.include_router(auth_router)
app.include_router(property_cases_router)
app.include_router(analysis_router)
app.include_router(reports_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "product": "BhoomiScan"}
