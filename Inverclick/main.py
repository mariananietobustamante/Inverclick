from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from Controllers.Prefixcontroller import router as prefix_router
from Controllers.UsersController import router as users_router
from Controllers.UsersLoginController import router as users_login_router
from Controllers.UsersRoleController import router as users_role_router
from Repositories.database import verify_db_connection_and_schema

verify_db_connection_and_schema()

app = FastAPI(
    title="Inverclick API",
    description="API para el semillero de investigación Inverclick",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(prefix_router)
app.include_router(users_role_router)
app.include_router(users_login_router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema.setdefault("components", {}).setdefault("securitySchemes", {})["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
