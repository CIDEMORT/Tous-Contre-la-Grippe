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
    nom_usuel: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000)
):
    """
    Données météo pour analyse de la saisonnalité
    
    Graphique: Aires / Courbes multiples
    Format Chart.js: Line chart avec plusieurs datasets (températures)
    """
    query = "SELECT * FROM donnees_meteo WHERE 1=1"
    
    if nom_usuel:
        query += f" AND nom_usuel LIKE '%{nom_usuel}%'"
    
    query += f" LIMIT {limit}"
    
    results = db.execute(text(query)).fetchall()
    
    data = []
    for row in results:
        data.append({
            "nom_usuel": row[1],
            "temp_min_sous_abri": row[2],
            "temp_max_sous_abri": row[3],
            "moy_quotidienne_sous_abri": row[4],
            "temp_quotidienne_min_au_dessus_du_sol": row[5],
            "temp_moy_mensuelle": row[6],
            "temp_moy_saison": row[7]
        })
    
    # Format Chart.js (Multi-line chart avec area)
    chartjs_format = {
        "type": "line",
        "data": {
            "labels": [d["nom_usuel"] for d in data],
            "datasets": [
                {
                    "label": "Température min sous abri",
                    "data": [d["temp_min_sous_abri"] for d in data],
                    "borderColor": "rgba(54, 162, 235, 1)",
                    "backgroundColor": "rgba(54, 162, 235, 0.2)",
                    "fill": True,
                    "tension": 0.4
                },
                {
                    "label": "Température max sous abri",
                    "data": [d["temp_max_sous_abri"] for d in data],
                    "borderColor": "rgba(255, 99, 132, 1)",
                    "backgroundColor": "rgba(255, 99, 132, 0.2)",
                    "fill": True,
                    "tension": 0.4
                },
                {
                    "label": "Moyenne quotidienne",
                    "data": [d["moy_quotidienne_sous_abri"] for d in data],
                    "borderColor": "rgba(255, 206, 86, 1)",
                    "backgroundColor": "rgba(255, 206, 86, 0.2)",
                    "fill": False,
                    "tension": 0.4,
                    "borderWidth": 2
                },
                {
                    "label": "Moyenne mensuelle",
                    "data": [d["temp_moy_mensuelle"] for d in data],
                    "borderColor": "rgba(75, 192, 192, 1)",
                    "backgroundColor": "rgba(75, 192, 192, 0.2)",
                    "fill": False,
                    "tension": 0.4,
                    "borderDash": [5, 5]
                },
                {
                    "label": "Moyenne saisonnière",
                    "data": [d["temp_moy_saison"] for d in data],
                    "borderColor": "rgba(153, 102, 255, 1)",
                    "backgroundColor": "rgba(153, 102, 255, 0.2)",
                    "fill": False,
                    "tension": 0.4,
                    "borderDash": [10, 5]
                }
            ]
        },
        "options": {
            "responsive": True,
            "plugins": {
                "title": {
                    "display": True,
                    "text": "Analyse de la saisonnalité - Données météorologiques"
                },
                "legend": {
                    "display": True,
                    "position": "top"
                },
                "tooltip": {
                    "mode": "index",
                    "intersect": False
                }
            },
            "scales": {
                "y": {
                    "beginAtZero": False,
                    "title": {
                        "display": True,
                        "text": "Température (°C)"
                    }
                },
                "x": {
                    "title": {
                        "display": True,
                        "text": "Station météorologique"
                    }
                }
            },
            "interaction": {
                "mode": "nearest",
                "axis": "x",
                "intersect": False
            }
        }
    }
    
    return {
        "question": "Analyse de la saisonnalité via données météorologiques",
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