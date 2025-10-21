from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from typing import Optional
from app.models.response_models import DonneesMeteoResponse


router = APIRouter()

# ============================================
# SAISONNALITÉ - Routes spécifiques
# ============================================

@router.get("/donnees-meteo", response_model=DonneesMeteoResponse)
async def get_donnees_meteo(
    db: Session = Depends(get_db),
    nom_usuel: Optional[str] = Query(None, description="Station météo"),
    annee: Optional[int] = Query(None, description="Année"),
    mois: Optional[int] = Query(None, description="Mois (1-12)"),
    limit: int = Query(100, ge=1, le=1000)
):
    """
    Données météo + grippe pour analyse de la saisonnalité
    
    Graphique: Aires / Courbes multiples
    """
    from app.models.schemas import DonneesMeteo
    
    query = db.query(DonneesMeteo)
    
    if nom_usuel:
        query = query.filter(DonneesMeteo.NOM_USUEL.like(f"%{nom_usuel}%"))
    if annee:
        query = query.filter(DonneesMeteo.annees == annee)
    if mois:
        query = query.filter(DonneesMeteo.mois == mois)
    
    query = query.limit(limit)
    results = query.all()
    
    data = []
    for row in results:
        data.append({
            "NOM_USUEL": row.NOM_USUEL,
            "TNTXM": row.TNTXM,
            "TNSOL": row.TNSOL,
            "TMM": row.TMM,
            "annees": row.annees,
            "mois": row.mois,
            "taux_grippe": row.taux_grippe,
            "incidence_sg_hebdo": row.incidence_sg_hebdo
        })
    
    # Format Chart.js (Multi-line chart)
    chartjs_format = {
        "type": "line",
        "data": {
            "labels": [f"{d['annees']}-{d['mois']:02d}" for d in data],
            "datasets": [
                {
                    "label": "Température moyenne (TMM)",
                    "data": [d["TMM"] for d in data],
                    "borderColor": "rgba(255, 99, 132, 1)",
                    "backgroundColor": "rgba(255, 99, 132, 0.2)",
                    "yAxisID": "y",
                    "tension": 0.4
                },
                {
                    "label": "Taux grippe",
                    "data": [d["taux_grippe"] for d in data],
                    "borderColor": "rgba(54, 162, 235, 1)",
                    "backgroundColor": "rgba(54, 162, 235, 0.2)",
                    "yAxisID": "y1",
                    "tension": 0.4
                },
                {
                    "label": "Incidence hebdo",
                    "data": [d["incidence_sg_hebdo"] for d in data],
                    "borderColor": "rgba(75, 192, 192, 1)",
                    "backgroundColor": "rgba(75, 192, 192, 0.2)",
                    "yAxisID": "y1",
                    "tension": 0.4
                }
            ]
        },
        "options": {
            "responsive": True,
            "interaction": {
                "mode": "index",
                "intersect": False
            },
            "plugins": {
                "title": {
                    "display": True,
                    "text": "Corrélation Température / Grippe"
                }
            },
            "scales": {
                "y": {
                    "type": "linear",
                    "display": True,
                    "position": "left",
                    "title": {
                        "display": True,
                        "text": "Température (°C)"
                    }
                },
                "y1": {
                    "type": "linear",
                    "display": True,
                    "position": "right",
                    "title": {
                        "display": True,
                        "text": "Taux grippe / Incidence"
                    },
                    "grid": {
                        "drawOnChartArea": False
                    }
                }
            }
        }
    }
    
    return {
        "question": "Analyse de la saisonnalité - Corrélation température/grippe",
        "graphique": "Aires / Courbes",
        "data": data,
        "total": len(data),
        "chartjs": chartjs_format
    }


@router.get("/correlation-meteo-grippe")
async def get_correlation_meteo_grippe(
    db: Session = Depends(get_db)
):
    """
    Corrélation entre données météo et cas de grippe
    
    Endpoint bonus pour croiser données météo + passages urgences
    """
    # TODO: Jointure entre donnees_meteo et autre table quand les données seront là
    
    return {
        "question": "Corrélation température / cas de grippe",
        "graphique": "Scatter plot + Line chart",
        "data": [],
        "message": "À implémenter avec les données réelles"
    }