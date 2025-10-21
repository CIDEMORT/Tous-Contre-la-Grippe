from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.constants import THEMATIQUES
from app.config import get_settings
from typing import Optional
from sqlalchemy import text
from app.models.response_models import AdminTablesResponse


router = APIRouter()
settings = get_settings()

# ============================================
# Routes thématiques génériques (anciennes)
# ============================================

@router.get("/logistique")
async def get_logistique_data(
    db: Session = Depends(get_db),
    filters: Optional[str] = Query(None, description="Filtres JSON"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """
    Thématique LOGISTIQUE : Distribution vaccins, stocks, actes de vaccination
    
    Route générique - Utilisez plutôt /api/logistique/actes-doses-region
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
        "message": "Utilisez les routes spécifiques: /api/logistique/actes-doses-region"
    }


@router.get("/geographique")
async def get_geographique_data(
    db: Session = Depends(get_db),
    filters: Optional[str] = Query(None, description="Filtres JSON"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """
    Thématique GÉOGRAPHIQUE : Accès aux soins
    
    Route générique - Utilisez plutôt les routes sous /api/geographie/
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
        "message": "Utilisez les routes spécifiques: /api/geographie/accessibilite-pharmacies"
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
    
    Route générique - Utilisez plutôt /api/saisonnalite/donnees-meteo
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
        "message": "Utilisez les routes spécifiques: /api/saisonnalite/donnees-meteo"
    }


@router.get("/filters/available")
async def get_available_filters(
    db: Session = Depends(get_db),
    thematique: str = Query(..., description="Thématique: logistique, geographique, saisonnalite")
):
    """
    Retourne les filtres disponibles pour une thématique donnée.
    """
    return {
        "thematique": thematique,
        "filters_available": [],
        "message": "Filtres à définir selon les colonnes des CSV"
    }


@router.get("/admin/tables", response_model=AdminTablesResponse, tags=["Admin"])
async def list_tables(db: Session = Depends(get_db)):
    """
    Liste toutes les tables de la base de données (dev only)
    """
    from sqlalchemy import inspect, text
    
    inspector = inspect(db.bind)
    tables = inspector.get_table_names()
    
    result = {}
    for table in tables:
        columns = [col['name'] for col in inspector.get_columns(table)]
        count = db.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
        result[table] = {
            "columns": columns,
            "row_count": count
        }
    
    return {
        "total_tables": len(tables),
        "tables": result
    }