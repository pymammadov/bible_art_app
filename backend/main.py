from fastapi import FastAPI

from .db import initialize_db
from .routes import router

app = FastAPI(title="Bible Art API")


@app.on_event("startup")
def startup() -> None:
    initialize_db()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(router)
