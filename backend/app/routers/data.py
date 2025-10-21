from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.constants import THEMATIQUES
from app.config import get_settings
from typing import Optional

router = APIRouter()
settings = get_settings()

# ============================================
# Routes racine (info + santé)
# ============================================

@router.get("/", tags=["Root"])
async def root():
    """
    Informations sur l'API et les thématiques disponibles
    """
    return {
        "message": "Flu Vaccination API - Visualiseur de données",
        "version": settings.api_version,
        "status": "running",
        "thematiques": THEMATIQUES
    }

@router.get("/health", tags=["Health"])
async def health():
    """
    Endpoint de santé pour vérifier que l'API fonctionne
    """
    return {"status": "healthy"}


# ============================================
# Routes thématiques
# ============================================

@router.get("/logistique")
async def get_logistique_data(
    db: Session = Depends(get_db),
    filters: Optional[str] = Query(None, description="Filtres JSON (ex: {'region': 'grand-est'})"),
    limit: int = Query(100, ge=1, le=1000, description="Nombre de résultats"),
    offset: int = Query(0, ge=0, description="Décalage pour pagination")
):
    """
    Thématique LOGISTIQUE : Distribution vaccins, stocks, actes de vaccination
    
    Les filtres seront définis plus tard selon les données disponibles.
    """
    return {
        "thematique": "logistique",
        "filters": filters,
        "pagination": {
            "limit": limit,
            "offset": offset,
            "total": 0
        },
        "data": [],
        "message": "Structure prête - En attente des données CSV"
    }


@router.get("/geographique")
async def get_geographique_data(
    db: Session = Depends(get_db),
    filters: Optional[str] = Query(None, description="Filtres JSON"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """
    Thématique GÉOGRAPHIQUE : Accès aux soins (pharmacies, médecins, hôpitaux)
    
    Les filtres seront définis plus tard selon les données disponibles.
    """
    return {
        "thematique": "geographique",
        "filters": filters,
        "pagination": {
            "limit": limit,
            "offset": offset,
            "total": 0
        },
        "data": [],
        "message": "Structure prête - En attente des données CSV"
    }


@router.get("/saisonnalite")
async def get_saisonnalite_data(
    db: Session = Depends(get_db),
    filters: Optional[str] = Query(None, description="Filtres JSON"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """
    Thématique SAISONNALITÉ : Virus grippal hiver vs été
    
    Les filtres seront définis plus tard selon les données disponibles.
    """
    return {
        "thematique": "saisonnalite",
        "filters": filters,
        "pagination": {
            "limit": limit,
            "offset": offset,
            "total": 0
        },
        "data": [],
        "message": "Structure prête - En attente des données CSV"
    }


@router.get("/filters/available")
async def get_available_filters(
    db: Session = Depends(get_db),
    thematique: str = Query(..., description="Thématique: logistique, geographique, saisonnalite")
):
    """
    Retourne les filtres disponibles pour une thématique donnée.
    Sera rempli quand les données seront chargées.
    
    Utile pour générer dynamiquement le formulaire de recherche côté front.
    """
    return {
        "thematique": thematique,
        "filters_available": [],
        "message": "Filtres à définir selon les colonnes des CSV"
    }

@router.get("/admin/tables", tags=["Admin"])
async def list_tables(db: Session = Depends(get_db)):
    """
    Liste toutes les tables de la base de données (dev only)
    """
    from sqlalchemy import inspect, text  # ← Ajouter text ici
    
    inspector = inspect(db.bind)
    tables = inspector.get_table_names()
    
    result = {}
    for table in tables:
        columns = [col['name'] for col in inspector.get_columns(table)]
        # Compter les lignes - UTILISER text() pour SQLAlchemy 2.0
        count = db.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
        result[table] = {
            "columns": columns,
            "row_count": count
        }
    
    return {
        "total_tables": len(tables),
        "tables": result
    }