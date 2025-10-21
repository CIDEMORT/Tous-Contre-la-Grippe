from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import get_settings
from app.database import engine, Base
from app.services.data_loader import load_all_csv_data
from app.routers import data
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Démarrage de l'application...")
    print("📊 Création des tables...")
    Base.metadata.create_all(bind=engine)
    
    print("📁 Chargement des données CSV...")
    load_all_csv_data()
    
    print("✅ Application prête !")
    yield
    
    print("👋 Arrêt de l'application...")

app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description=settings.api_description,
    lifespan=lifespan
)

# CORS - Configuration permissive pour le hackathon
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Accepte tous les origins (hackathon only!)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(data.router, prefix="/api", tags=["Données"])