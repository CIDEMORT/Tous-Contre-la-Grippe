from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import get_settings
from app.database import engine, Base
from app.services.data_loader import load_all_csv_data
from app.routers import data, geographie, logistique, saisonnalite
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes génériques
app.include_router(data.router, prefix="/api", tags=["Données génériques"])

# Routes spécifiques par thématique
app.include_router(geographie.router, prefix="/api/geographie", tags=["Géographie"])
app.include_router(logistique.router, prefix="/api/logistique", tags=["Logistique"])
app.include_router(saisonnalite.router, prefix="/api/saisonnalite", tags=["Saisonnalité"])