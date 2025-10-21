from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List

class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./flu_vaccination.db"
    
    # CSV Data Path
    csv_data_path: str = "./data/raw"
    
    # API Info
    api_title: str = "Flu Vaccination API"
    api_version: str = "1.0.0"
    api_description: str = """
    API pour l'optimisation de la stratégie vaccinale contre la grippe.
    
    ## Fonctionnalités
    * **Vaccination** - Données de couverture vaccinale et distribution
    * **Urgences** - Passages aux urgences et actes SOS Médecins
    * **IAS** - Indicateur Avancé Sanitaire
    """
    
    # CORS - Ajout de "*" pour accepter tous les origins en prod (ou spécifie ton front)
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "https://*.onrender.com",  # Pour ton front sur Render
        "*"  # Accepte tous (pour le hackathon, à retirer en prod réelle)
    ]
    
    # Environment
    environment: str = "development"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()