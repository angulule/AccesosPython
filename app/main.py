import os

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.modules.modulo.interfaces.modulo_api import router as modulo_router
from app.modules.pantalla.interfaces.pantalla_api import router as pantalla_router
from app.modules.permiso.interfaces.permiso_api import router as permiso_router
from app.modules.rol.interfaces.rol_api import router as rol_router
from app.modules.auth.interfaces.auth_api import router as auth_router
from app.modules.permiso_usuario.interfaces.permiso_usuario_api import router as permiso_usuario_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # if settings.ENVIRONMENT == "DEV":
    #     init_db()
    yield
    
app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
    swagger_ui_parameters={
        "persistAuthorization": True
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router, prefix="/api")
app.include_router(modulo_router, prefix="/api")
app.include_router(pantalla_router, prefix="/api")
app.include_router(permiso_router, prefix="/api")
app.include_router(rol_router, prefix="/api")
app.include_router(permiso_usuario_router, prefix="/api")