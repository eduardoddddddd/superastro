"""FastAPI application — SuperAstro backend."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from api.routes import natal, transits, horary, cities

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app = FastAPI(
    title="SuperAstro API",
    description="API de astrología — cartas natales, tránsitos y horaria",
    version="1.0.0",
)

# CORS para desarrollo local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas de API
app.include_router(natal.router, prefix="/api/natal", tags=["Carta Natal"])
app.include_router(transits.router, prefix="/api/transits", tags=["Tránsitos"])
app.include_router(horary.router, prefix="/api/horary", tags=["Horaria"])
app.include_router(cities.router, prefix="/api/cities", tags=["Ciudades"])

# Archivos estáticos del frontend
app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIR, "assets")), name="assets")


@app.get("/", response_class=FileResponse)
async def root():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


@app.get("/{page}", response_class=FileResponse)
async def serve_page(page: str):
    path = os.path.join(FRONTEND_DIR, f"{page}.html")
    if os.path.exists(path):
        return FileResponse(path)
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))
