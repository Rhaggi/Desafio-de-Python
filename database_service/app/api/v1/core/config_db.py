from fastapi import FastAPI

app_db = FastAPI()

from database_service.app.api.v1.endpoints.db_health import router_db
from database_service.app.api.v1.endpoints.db_clients import db_clients

app_db.include_router(router_db)
app_db.include_router(db_clients)
