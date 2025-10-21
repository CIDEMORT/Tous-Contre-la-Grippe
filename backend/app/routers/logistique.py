from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from typing import Optional

from app.models.response_models import (
    ActesDosesRegionResponse,
    NombrePharmaciesPeriodeResponse,
    ActesDosesRegionResponse
)

router = APIRouter()

# ============================================
# LOGISTIQUE - Routes spécifiques
# ============================================

@router.get("/actes-doses-region", response_model=ActesDosesRegionResponse)
async def get_actes_doses_region(
    db: Session = Depends(get_db),
    region: Optional[str] = Query(None, description="Filtrer par région")
):
    """
    Comparaison actes de vaccination vs doses distribuées par région
    
    Graphique: Barres groupées
    """
    from app.models.schemas import ActesDosesRegion
    
    query = db.query(ActesDosesRegion)
    
    if region:
        query = query.filter(ActesDosesRegion.region.like(f"%{region}%"))
    
    results = query.all()
    
    data = []
    for row in results:
        data.append({
            "region": row.region,
            "acte_vgp": row.acte_vgp,
            "doses_j07e1": row.doses_j07e1
        })
    
    # Format Chart.js (Barres groupées)
    chartjs_format = {
        "type": "bar",
        "data": {
            "labels": [d["region"] for d in data],
            "datasets": [
                {
                    "label": "Actes de vaccination",
                    "data": [d["acte_vgp"] for d in data],
                    "backgroundColor": "rgba(54, 162, 235, 0.7)",
                    "borderColor": "rgba(54, 162, 235, 1)",
                    "borderWidth": 1
                },
                {
                    "label": "Doses distribuées",
                    "data": [d["doses_j07e1"] for d in data],
                    "backgroundColor": "rgba(255, 99, 132, 0.7)",
                    "borderColor": "rgba(255, 99, 132, 1)",
                    "borderWidth": 1
                }
            ]
        },
        "options": {
            "responsive": True,
            "plugins": {
                "title": {
                    "display": True,
                    "text": "Actes vs Doses par région"
                },
                "legend": {
                    "position": "top"
                }
            },
            "scales": {
                "y": {
                    "beginAtZero": True,
                    "title": {
                        "display": True,
                        "text": "Nombre"
                    }
                }
            }
        }
    }
    
    return {
        "question": "Comparaison actes de vaccination vs doses distribuées",
        "graphique": "Barres groupées",
        "data": data,
        "total": len(data),
        "chartjs": chartjs_format
    }


@router.get("/nombre-pharmacies-periode", response_model=NombrePharmaciesPeriodeResponse)
async def get_nombre_pharmacies_periode(
    db: Session = Depends(get_db),
    date_debut: Optional[str] = Query(None, description="Date de début (YYYY-MM-DD)"),
    date_fin: Optional[str] = Query(None, description="Date de fin (YYYY-MM-DD)"),
    variable_pharmacie: Optional[str] = Query(None, description="Variable spécifique")
):
    """
    Nombre de pharmacie sur une période/campagne de vaccination
    
    Graphique: Line chart (évolution temporelle)
    """
    query = "SELECT * FROM nombre_pharmacies_periode WHERE 1=1"
    
    if date_debut:
        query += f" AND date >= '{date_debut}'"
    if date_fin:
        query += f" AND date <= '{date_fin}'"
    if variable_pharmacie:
        query += f" AND variable_pharmacie = '{variable_pharmacie}'"
    
    query += " ORDER BY date ASC"
    
    results = db.execute(text(query)).fetchall()
    
    data = []
    for row in results:
        data.append({
            "date": str(row[1]),
            "variable_pharmacie": row[2],
            "valeur": row[3]
        })
    
    # Format Chart.js (Line chart)
    chartjs_format = {
        "type": "line",
        "data": {
            "labels": [d["date"] for d in data],
            "datasets": [{
                "label": "Nombre de pharmacies",
                "data": [d["valeur"] for d in data],
                "borderColor": "rgba(75, 192, 192, 1)",
                "backgroundColor": "rgba(75, 192, 192, 0.2)",
                "tension": 0.4,
                "fill": True
            }]
        },
        "options": {
            "responsive": True,
            "plugins": {
                "title": {
                    "display": True,
                    "text": "Évolution du nombre de pharmacies"
                }
            },
            "scales": {
                "y": {
                    "beginAtZero": True
                },
                "x": {
                    "type": "time",
                    "time": {
                        "unit": "day"
                    }
                }
            }
        }
    }
    
    return {
        "question": "Nombre de pharmacie sur une période/campagne de vaccination",
        "graphique": "Line chart",
        "data": data,
        "total": len(data),
        "chartjs": chartjs_format
    }