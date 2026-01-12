from fastapi import FastAPI

app = FastAPI()

from ..endpoints.clientes import clientes
from ..endpoints.health import router
from ..endpoints.score import score

app.include_router(clientes)
app.include_router(router)
app.include_router(score)
